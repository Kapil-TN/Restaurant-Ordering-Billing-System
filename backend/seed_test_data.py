import random
from datetime import datetime, timedelta
from app import create_app, db
from app.admin.placeholder_models import User, MenuItem, Order, OrderItem, Bill

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    users = [User(email=f"customer{i}@example.com") for i in range(1, 6)]
    db.session.add_all(users)
    db.session.commit()

    item_names = ["Paneer Butter Masala", "Veg Biryani", "Masala Dosa",
                  "Cold Coffee", "Chicken Tikka", "Gulab Jamun"]
    items = [MenuItem(name=name) for name in item_names]
    db.session.add_all(items)
    db.session.commit()

    for day_offset in range(35, -1, -1):
        order_date = datetime.now() - timedelta(days=day_offset)

        for _ in range(random.randint(1, 5)):
            order = Order(
                customer_id=random.choice(users).id,
                order_type=random.choice(["dine-in", "takeaway"]),
                status="billed",
                placed_at=order_date,
            )
            db.session.add(order)
            db.session.flush()

            order_total = 0
            for _ in range(random.randint(1, 3)):
                item = random.choice(items)
                quantity = random.randint(1, 4)
                unit_price = round(random.uniform(80, 350), 2)
                subtotal = round(unit_price * quantity, 2)
                order_total += subtotal

                db.session.add(OrderItem(
                    order_id=order.id,
                    menu_item_id=item.id,
                    quantity=quantity,
                    unit_price=unit_price,
                    subtotal=subtotal,
                ))

            tax = round(order_total * 0.05, 2)
            db.session.add(Bill(
                order_id=order.id,
                total_amount=order_total,
                tax_amount=tax,
                discount=0,
                grand_total=round(order_total + tax, 2),
                payment_mode=random.choice(["cash", "card", "upi"]),
                billed_at=order_date,
                status="paid",
            ))

    db.session.commit()
    print("Seed complete: 5 users, 6 menu items, ~36 days of orders/bills.")
