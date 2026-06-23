import pytest
from datetime import datetime, timedelta
from app import create_app, db
from app.admin.placeholder_models import User, MenuItem, Order, OrderItem, Bill


@pytest.fixture
def app():
    app = create_app(test_config={
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'TESTING': True,
    })

    with app.app_context():
        db.create_all()
        _seed_known_data()
        yield app
        db.session.remove()
        db.drop_all()


def _seed_known_data():
    user = User(email="testcustomer@example.com")
    db.session.add(user)
    db.session.commit()

    item = MenuItem(name="Test Item")
    db.session.add(item)
    db.session.commit()

    today = datetime.now()
    yesterday = today - timedelta(days=1)

    order_today = Order(customer_id=user.id, order_type="dine-in",
                         status="billed", placed_at=today)
    db.session.add(order_today)
    db.session.flush()

    db.session.add(OrderItem(order_id=order_today.id, menu_item_id=item.id,
                              quantity=2, unit_price=100, subtotal=200))
    db.session.add(Bill(order_id=order_today.id, total_amount=200, tax_amount=10,
                         discount=0, grand_total=210, payment_mode="cash",
                         billed_at=today, status="paid"))

    order_yesterday = Order(customer_id=user.id, order_type="takeaway",
                             status="billed", placed_at=yesterday)
    db.session.add(order_yesterday)
    db.session.flush()

    db.session.add(OrderItem(order_id=order_yesterday.id, menu_item_id=item.id,
                              quantity=1, unit_price=100, subtotal=100))
    db.session.add(Bill(order_id=order_yesterday.id, total_amount=100, tax_amount=0,
                         discount=0, grand_total=100, payment_mode="upi",
                         billed_at=yesterday, status="paid"))

    db.session.commit()
