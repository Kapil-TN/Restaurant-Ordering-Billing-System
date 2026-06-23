from app import create_app
from app.admin import analytics

app = create_app()

with app.app_context():
    today = analytics.get_today_revenue()
    yesterday = analytics.get_yesterday_revenue()

    print("Total revenue:", analytics.get_total_revenue())
    print("Today's revenue:", today)
    print("Yesterday's revenue:", yesterday)
    print("Revenue change %:", analytics.get_revenue_difference_percentage(today, yesterday))
    print("Best sellers:", analytics.get_best_selling_items())
    print("Order type distribution:", analytics.get_order_type_distribution())
    print("Total orders:", analytics.get_total_orders_count())
    print("Total customers:", analytics.get_total_customers_count())
    print("Pending orders:", analytics.get_pending_orders_count())
    print("Revenue trend (last 5 days):", analytics.get_revenue_trend_30_days()[-5:])
