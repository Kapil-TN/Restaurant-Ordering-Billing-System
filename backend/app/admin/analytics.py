from datetime import date, timedelta
from sqlalchemy import func
from app import db
from app.admin.placeholder_models import Order, OrderItem, Bill, MenuItem, User


ONLY_COUNT_PAID_BILLS = True
PENDING_ORDER_STATUSES = ['placed', 'preparing', 'served']


def _base_bill_query():
    query = Bill.query
    if ONLY_COUNT_PAID_BILLS:
        query = query.filter(Bill.status == 'paid')
    return query


def get_total_revenue():
    total = _base_bill_query().with_entities(func.sum(Bill.grand_total)).scalar()
    return round(total or 0, 2)


def get_today_revenue():
    today = date.today()
    total = (
        _base_bill_query()
        .filter(func.date(Bill.billed_at) == today)
        .with_entities(func.sum(Bill.grand_total))
        .scalar()
    )
    return round(total or 0, 2)


def get_yesterday_revenue():
    yesterday = date.today() - timedelta(days=1)
    total = (
        _base_bill_query()
        .filter(func.date(Bill.billed_at) == yesterday)
        .with_entities(func.sum(Bill.grand_total))
        .scalar()
    )
    return round(total or 0, 2)


def get_revenue_difference_percentage(today_revenue, yesterday_revenue):
    if yesterday_revenue == 0:
        return 100.0 if today_revenue > 0 else 0.0
    difference = today_revenue - yesterday_revenue
    percentage = (difference / yesterday_revenue) * 100
    return round(percentage, 2)


def get_best_selling_items(limit=5):
    results = (
        db.session.query(
            MenuItem.name,
            func.sum(OrderItem.quantity).label('total_quantity')
        )
        .join(MenuItem, OrderItem.menu_item_id == MenuItem.id)
        .group_by(MenuItem.id, MenuItem.name)
        .order_by(func.sum(OrderItem.quantity).desc())
        .limit(limit)
        .all()
    )
    return [
        {"name": row.name, "quantity_sold": int(row.total_quantity)}
        for row in results
    ]


def get_order_type_distribution():
    results = (
        db.session.query(
            Order.order_type,
            func.count(Order.id).label('count')
        )
        .group_by(Order.order_type)
        .all()
    )
    return [
        {"order_type": row.order_type, "count": row.count}
        for row in results
    ]


def get_revenue_trend_30_days():
    today = date.today()
    start_date = today - timedelta(days=29)

    results = (
        _base_bill_query()
        .filter(func.date(Bill.billed_at) >= start_date)
        .with_entities(
            func.date(Bill.billed_at).label('bill_date'),
            func.sum(Bill.grand_total).label('total')
        )
        .group_by(func.date(Bill.billed_at))
        .all()
    )

    revenue_by_date = {str(row.bill_date): row.total for row in results}

    trend = []
    for i in range(30):
        day = start_date + timedelta(days=i)
        day_str = day.isoformat()
        trend.append({
            "date": day_str,
            "revenue": round(revenue_by_date.get(day_str, 0) or 0, 2)
        })

    return trend


def get_total_orders_count():
    return Order.query.count()


def get_total_customers_count():
    return User.query.count()


def get_pending_orders_count():
    return Order.query.filter(Order.status.in_(PENDING_ORDER_STATUSES)).count()
