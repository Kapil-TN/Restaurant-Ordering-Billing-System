from app.admin import analytics


def test_total_revenue(app):
    assert analytics.get_total_revenue() == 310.0


def test_today_revenue(app):
    assert analytics.get_today_revenue() == 210.0


def test_yesterday_revenue(app):
    assert analytics.get_yesterday_revenue() == 100.0


def test_revenue_change_percentage_normal_case():
    result = analytics.get_revenue_difference_percentage(210, 100)
    assert result == 110.0


def test_revenue_change_percentage_handles_zero_yesterday():
    result = analytics.get_revenue_difference_percentage(50, 0)
    assert result == 100.0


def test_best_selling_items_includes_seeded_item(app):
    results = analytics.get_best_selling_items()
    names = [item["name"] for item in results]
    assert "Test Item" in names


def test_order_type_distribution_has_both_types(app):
    results = analytics.get_order_type_distribution()
    types = [r["order_type"] for r in results]
    assert "dine-in" in types
    assert "takeaway" in types


def test_total_orders_count(app):
    assert analytics.get_total_orders_count() == 2


def test_total_customers_count(app):
    assert analytics.get_total_customers_count() == 1


def test_revenue_trend_returns_30_days(app):
    trend = analytics.get_revenue_trend_30_days()
    assert len(trend) == 30
