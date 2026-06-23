from flask import Blueprint, jsonify, request
from app.admin.cache import cache_response
from app.admin.analytics import (
    get_total_revenue,
    get_today_revenue,
    get_yesterday_revenue,
    get_revenue_difference_percentage,
    get_best_selling_items,
    get_order_type_distribution,
    get_revenue_trend_30_days,
    get_total_orders_count,
    get_total_customers_count,
    get_pending_orders_count,
)

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/dashboard', methods=['GET'])
@cache_response(cache_key="dashboard_summary", expiry_seconds=600)
def get_dashboard_summary():
    dashboard_data = {
        "total_orders": get_total_orders_count(),
        "total_customers": get_total_customers_count(),
        "pending_orders": get_pending_orders_count(),
    }
    return jsonify(dashboard_data), 200


@admin_bp.route('/analytics', methods=['GET'])
@cache_response(cache_key="analytics_data", expiry_seconds=600)
def get_analytics():
    today_revenue = get_today_revenue()
    yesterday_revenue = get_yesterday_revenue()

    analytics_data = {
        "revenue": {
            "total_revenue": get_total_revenue(),
            "today_revenue": today_revenue,
            "yesterday_revenue": yesterday_revenue,
            "revenue_change_percentage": get_revenue_difference_percentage(
                today_revenue, yesterday_revenue
            ),
        },
        "best_sellers": get_best_selling_items(),
        "order_type_distribution": get_order_type_distribution(),
        "revenue_trend": get_revenue_trend_30_days(),
    }
    return jsonify(analytics_data), 200


@admin_bp.route('/test-task', methods=['POST'])
def trigger_test_task():
    from app.admin.tasks import dummy_task
    result = dummy_task.delay()
    return jsonify({"task_id": result.id, "message": "Task queued!"}), 202


@admin_bp.route('/test-task/status/<task_id>', methods=['GET'])
def check_task_status(task_id):
    from app.celery_app import celery_app
    result = celery_app.AsyncResult(task_id)
    return jsonify({
        "status": result.status,
        "result": result.result if result.ready() else None
    }), 200


@admin_bp.route('/export', methods=['POST'])
def trigger_export():
    from app.admin.tasks import generate_csv_export

    data = request.get_json()
    customer_id = data.get('customer_id')
    customer_email = data.get('customer_email')

    if not customer_id or not customer_email:
        return jsonify({"error": "customer_id and customer_email are required"}), 400

    result = generate_csv_export.delay(customer_id, customer_email)

    return jsonify({
        "task_id": result.id,
        "message": "Export started. You'll receive an email when it's ready."
    }), 202


@admin_bp.route('/export/status/<task_id>', methods=['GET'])
def check_export_status(task_id):
    from app.celery_app import celery_app
    result = celery_app.AsyncResult(task_id)
    return jsonify({
        "status": result.status,
        "result": result.result if result.ready() else None
    }), 200
