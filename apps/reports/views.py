from django.shortcuts import render
from django.db import connection


def format_currency(value):
    return "R$ {:,.2f}".format(value).replace(",", "X").replace(".", ",").replace("X", ".")


def get_all_order_totals():
    with connection.cursor() as cursor:
        cursor.execute("""
            WITH RefundSums AS (
                SELECT order_id, SUM(total_refund_amount) AS total_refund_amount_sum
                FROM order_returns
                GROUP BY order_id
            )
            SELECT 
                COUNT(DISTINCT o.id) AS total_orders, 
                COALESCE(SUM(o.final_price - COALESCE(rs.total_refund_amount_sum, 0)), 0) AS total_value,
                COUNT(DISTINCT CASE WHEN o.current_status IN ('DELIVERED', 'PARTIAL_DELIVERED', 'PARTIAL_RETURN', 'PROCESSING_RETURN') THEN o.id END) AS delivered_orders,
                COALESCE(SUM(CASE WHEN o.current_status IN ('DELIVERED', 'PARTIAL_DELIVERED', 'PARTIAL_RETURN', 'PROCESSING_RETURN') THEN o.final_price - COALESCE(rs.total_refund_amount_sum, 0) END), 0) AS delivered_value,
                COUNT(DISTINCT CASE WHEN o.current_status IN ('ON_ROUTE') THEN o.id END) AS on_route_orders,
                COALESCE(SUM(CASE WHEN o.current_status IN ('ON_ROUTE') THEN o.final_price - COALESCE(rs.total_refund_amount_sum, 0) END), 0) AS on_route_value,
                COUNT(DISTINCT CASE WHEN o.current_status IN ('IN_SEPARATION') THEN o.id END) AS in_separation_orders,
                COALESCE(SUM(CASE WHEN o.current_status IN ('IN_SEPARATION') THEN o.final_price - COALESCE(rs.total_refund_amount_sum, 0) END), 0) AS in_separation_value,
                COUNT(DISTINCT CASE WHEN o.current_status IN ('AWAITING_COLLECTION', 'WAITING_FOR_SELLER', 'PROCESSING_PAYMENT') THEN o.id END) AS open_orders,
                COALESCE(SUM(CASE WHEN o.current_status IN ('AWAITING_COLLECTION', 'WAITING_FOR_SELLER', 'PROCESSING_PAYMENT') THEN o.final_price - COALESCE(rs.total_refund_amount_sum, 0) END), 0) AS open_value,
                COUNT(DISTINCT CASE WHEN o.current_status IN ('CANCELED', 'TOTAL_RETURN', 'PAYMENT_REFUSED', 'MISPLACED') THEN o.id END) AS canceled_orders,
                COALESCE(SUM(CASE WHEN o.current_status IN ('CANCELED', 'TOTAL_RETURN', 'PAYMENT_REFUSED', 'MISPLACED') THEN o.final_price END), 0) AS canceled_value
            FROM orders o
            LEFT JOIN RefundSums rs ON o.id = rs.order_id
            WHERE (o.created_at AT TIME ZONE 'UTC' AT TIME ZONE 'America/Sao_Paulo')::DATE = CURRENT_DATE
        """)
        results = cursor.fetchone()
    formatted_values = [results[i] if i % 2 == 0 else format_currency(
        results[i]) for i in range(len(results))]
    return formatted_values


def daily_view(request):
    (total_orders, total_value,
     delivered_orders, delivered_value,
     on_route_orders, on_route_value,
     in_separation_orders, in_separation_value,
     open_orders, open_value,
     canceled_orders, canceled_value) = get_all_order_totals()
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT s.name, COUNT(DISTINCT o.id) AS total_orders
            FROM orders o
            JOIN order_products op ON o.id = op.order_id
            JOIN branches b ON op.branch_id = b.id
            JOIN sellers s ON b.seller_id = s.id
            WHERE op.deleted = FALSE
              AND (o.created_at AT TIME ZONE 'UTC' AT TIME ZONE 'America/Sao_Paulo')::DATE = CURRENT_DATE
              AND o.current_status IN ('DELIVERED', 'PARTIAL_DELIVERED', 'PARTIAL_RETURN', 'PROCESSING_RETURN', 
                                       'WAITING_FOR_SELLER', 'IN_SEPARATION', 'AWAITING_COLLECTION', 'ON_ROUTE')
            GROUP BY s.name
            HAVING COUNT(DISTINCT o.id) > 0
            ORDER BY total_orders DESC
        """)
        results = cursor.fetchall()
    sellers = [row[0] for row in results]
    orders = [row[1] for row in results]
    return render(request, "report-daily.html", {
        "sellers": sellers,
        "orders": orders,
        "total_orders": total_orders,
        "total_value": total_value,
        "total_orders_delivered": delivered_orders,
        "total_value_delivered": delivered_value,
        "total_orders_on_route": on_route_orders,
        "total_value_on_route": on_route_value,
        "total_orders_in_separation": in_separation_orders,
        "total_value_in_separation": in_separation_value,
        "total_orders_open": open_orders,
        "total_value_open": open_value,
        "total_orders_canceled": canceled_orders,
        "total_value_canceled": canceled_value
    })


def home_view(request):
    print("Carregando o home.html")
    return render(request, "home.html", {})


def default_view(request):
    return render(request, "report-default.html", {})
