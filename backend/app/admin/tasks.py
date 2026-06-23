import time
from datetime import datetime, timedelta
from app.celery_app import celery_app
from app.admin.email_utils import send_email
from app.admin.export import write_csv_file


@celery_app.task(name='admin.dummy_task')
def dummy_task():
    print("Dummy task started... working for 5 seconds")
    time.sleep(5)
    print("Dummy task finished!")
    return "Dummy task completed successfully"


def _get_busiest_day():
    from sqlalchemy import func
    from app import db
    from app.admin.placeholder_models import Order

    result = (
        db.session.query(
            func.date(Order.placed_at).label('day'),
            func.count(Order.id).label('order_count')
        )
        .group_by(func.date(Order.placed_at))
        .order_by(func.count(Order.id).desc())
        .first()
    )
    return str(result.day) if result else "N/A"


@celery_app.task(name='admin.send_monthly_report')
def send_monthly_report():
    from app import create_app
    from app.admin import analytics

    app = create_app()
    with app.app_context():
        report = {
            "total_revenue": analytics.get_total_revenue(),
            "top_3_items": [item["name"] for item in analytics.get_best_selling_items(limit=3)],
            "busiest_day": _get_busiest_day(),
            "total_orders": analytics.get_total_orders_count(),
        }

        admin_email = "admin@restaurant.com"

        send_email(
            to_address=admin_email,
            subject=f"Monthly Revenue Report — {datetime.now().strftime('%B %Y')}",
            body=(
                f"Total Revenue: Rs.{report['total_revenue']}\n"
                f"Top 3 Items: {', '.join(report['top_3_items'])}\n"
                f"Busiest Day: {report['busiest_day']}\n"
                f"Total Orders: {report['total_orders']}"
            ),
        )

    print(f"[MONTHLY REPORT] Sent: {report}")
    return report


@celery_app.task(name='admin.send_reengagement_emails')
def send_reengagement_emails():
    from app import create_app, db
    from app.admin.placeholder_models import User, Order
    from sqlalchemy import func

    app = create_app()
    with app.app_context():
        cutoff = datetime.now() - timedelta(days=7)

        last_order_subquery = (
            db.session.query(
                Order.customer_id,
                func.max(Order.placed_at).label('last_order_date')
            )
            .group_by(Order.customer_id)
            .subquery()
        )

        inactive_customers = (
            db.session.query(User)
            .join(last_order_subquery, User.id == last_order_subquery.c.customer_id)
            .filter(last_order_subquery.c.last_order_date < cutoff)
            .all()
        )

        for customer in inactive_customers:
            send_email(
                to_address=customer.email,
                subject="We miss you! Come back for a meal",
                body="It's been a week since your last order. Check out what's new on our menu!",
            )

    print(f"[REMINDER] Sent to {len(inactive_customers)} inactive customers")
    return f"Sent reminders to {len(inactive_customers)} customers"


@celery_app.task(name='admin.generate_csv_export')
def generate_csv_export(customer_id, customer_email):
    from app import create_app, db
    from app.admin.placeholder_models import Order, OrderItem, Bill, MenuItem

    app = create_app()
    with app.app_context():
        orders = Order.query.filter_by(customer_id=customer_id).all()

        rows = []
        for order in orders:
            bill = Bill.query.filter_by(order_id=order.id).first()
            items = (
                db.session.query(MenuItem.name, OrderItem.quantity)
                .join(OrderItem, OrderItem.menu_item_id == MenuItem.id)
                .filter(OrderItem.order_id == order.id)
                .all()
            )
            items_str = ", ".join(f"{name} x{qty}" for name, qty in items)

            rows.append({
                "order_id": order.id,
                "order_date": order.placed_at.strftime("%Y-%m-%d"),
                "order_type": order.order_type,
                "items": items_str,
                "grand_total": bill.grand_total if bill else 0,
                "payment_mode": bill.payment_mode if bill else "N/A",
                "status": bill.status if bill else "unpaid",
            })

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"order_history_{customer_id}_{timestamp}.csv"
        filepath = write_csv_file(rows, filename)

        send_email(
            to_address=customer_email,
            subject="Your Order History Export is Ready",
            body=f"Hi, your order history CSV is attached. It contains {len(rows)} orders.",
            attachment_path=filepath,
        )

    print(f"[EXPORT] Done! File saved at {filepath}")
    return {"filepath": filepath, "row_count": len(rows)}
