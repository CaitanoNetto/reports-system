import pandas as pd
from django.shortcuts import render
from django.db import connection
from datetime import datetime, timedelta
from decimal import Decimal

SHEET_URL_META = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRP-tqqPOb2b50FXI0k_o0nd0dhhRk5otqCZflN42C_PJ321U7askszFuFTJ1rYL43m9eqJIyaEfHSE/pub?output=csv"
SHEET_URL_FERIADOS = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRkC6Me4aCxwyOqNwJpKoEmEA5O_9a40Hr4bbnMFkCK7L66OUPjs2No9bb-VUsR_QfUFlx5md7nhzk2/pub?output=csv"


def format_currency(value):
    return "R$ {:,.2f}".format(value).replace(",", "X").replace(".", ",").replace("X", ".")


def fetch_meta():
    try:
        df = pd.read_csv(SHEET_URL_META, dtype={'Data': str})
        current_month = datetime.now().strftime("%Y%m")

        df_filtered = df[df["Data"] == current_month]

        if df_filtered.empty:
            print(f"No meta found for the month {current_month}")
            return Decimal("0")

        total_meta = df_filtered["Meta"].apply(
            lambda x: Decimal(x.replace("R$", "").replace(
                ".", "").replace(",", ".").strip())
        ).sum()

        total_meta = Decimal(total_meta) if total_meta else Decimal("1")

        return total_meta

    except pd.errors.ParserError:
        print("Error: Failed to parse CSV. Ensure the spreadsheet is formatted correctly.")
        return None

    except Exception as e:
        print(f"Error loading spreadsheet: {e}")
        return None


def get_working_days():
    df = pd.read_csv(SHEET_URL_FERIADOS, dtype={'Data': str})

    df["Data"] = pd.to_datetime(df["Data"], format='%m/%d/%Y')

    today = datetime.today()
    year, month = today.year, today.month

    first_day = datetime(year, month, 1)
    last_day = (first_day.replace(month=month + 1) -
                timedelta(days=1)) if month < 12 else datetime(year, 12, 31)

    all_days = pd.date_range(start=first_day, end=last_day)

    holidays = df[(df["Data"].dt.year == year) & (
        df["Data"].dt.month == month)]["Data"].tolist()

    working_days = [day for day in all_days if day.weekday()
                    < 5 and day not in holidays]

    return len(working_days)


def get_elapsed_working_days():
    df = pd.read_csv(SHEET_URL_FERIADOS, dtype={'Data': str})

    df["Data"] = pd.to_datetime(df["Data"], format='%m/%d/%Y')

    today = datetime.today()
    year, month, day = today.year, today.month, today.day

    first_day = datetime(year, month, 1)
    today_date = datetime(year, month, day)

    all_days = pd.date_range(start=first_day, end=today_date)

    holidays = df[(df["Data"].dt.year == year) & (
        df["Data"].dt.month == month)]["Data"].tolist()

    elapsed_working_days = [day for day in all_days if day.weekday()
                            < 5 and day not in holidays]

    return len(elapsed_working_days)


def get_monthly_order_totals():
    with connection.cursor() as cursor:
        cursor.execute("""
            WITH RefundSums AS (
                SELECT order_id, SUM(total_refund_amount) AS total_refund_amount_sum
                FROM order_returns
                GROUP BY order_id
            )
            SELECT 
                COALESCE(SUM(CASE WHEN o.current_status NOT IN ('CANCELED', 'TOTAL_RETURN', 'PAYMENT_REFUSED', 'MISPLACED') 
                                  THEN o.final_price - COALESCE(rs.total_refund_amount_sum, 0) END), 0) AS monthly_total_value,
                COALESCE(SUM(CASE WHEN o.current_status IN ('DELIVERED', 'PARTIAL_DELIVERED', 'PARTIAL_RETURN', 'PROCESSING_RETURN') 
                                  THEN o.final_price - COALESCE(rs.total_refund_amount_sum, 0) END), 0) AS monthly_delivered_value
            FROM orders o
            LEFT JOIN RefundSums rs ON o.id = rs.order_id
            WHERE EXTRACT(YEAR FROM o.created_at AT TIME ZONE 'UTC' AT TIME ZONE 'America/Sao_Paulo') = EXTRACT(YEAR FROM CURRENT_DATE)
              AND EXTRACT(MONTH FROM o.created_at AT TIME ZONE 'UTC' AT TIME ZONE 'America/Sao_Paulo') = EXTRACT(MONTH FROM CURRENT_DATE)
        """)

        results = cursor.fetchone()

    return Decimal(results[0]), Decimal(results[1])


def get_monthly_accumulated():
    with connection.cursor() as cursor:
        cursor.execute("""
            WITH RefundSums AS (
                SELECT order_id, SUM(total_refund_amount) AS total_refund_amount_sum
                FROM order_returns
                GROUP BY order_id
            ),
            DailyTotals AS (
                SELECT 
                    DATE(o.created_at AT TIME ZONE 'UTC' AT TIME ZONE 'America/Sao_Paulo') AS order_date,
                    COALESCE(SUM(CASE 
                        WHEN o.current_status NOT IN ('CANCELED', 'TOTAL_RETURN', 'PAYMENT_REFUSED', 'MISPLACED') 
                        THEN o.final_price - COALESCE(rs.total_refund_amount_sum, 0) 
                    END), 0) AS daily_total_value
                FROM orders o
                LEFT JOIN RefundSums rs ON o.id = rs.order_id
                WHERE EXTRACT(YEAR FROM o.created_at AT TIME ZONE 'UTC' AT TIME ZONE 'America/Sao_Paulo') = EXTRACT(YEAR FROM CURRENT_DATE)
                  AND EXTRACT(MONTH FROM o.created_at AT TIME ZONE 'UTC' AT TIME ZONE 'America/Sao_Paulo') = EXTRACT(MONTH FROM CURRENT_DATE)
                GROUP BY order_date
                ORDER BY order_date
            )
            SELECT 
                order_date, 
                SUM(daily_total_value) OVER (ORDER BY order_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS accumulated_value
            FROM DailyTotals;
        """)

        results = cursor.fetchall()

    return [{"date": row[0].strftime("%d/%m"), "value": float(row[1])} for row in results]


def get_daily_order_totals():
    with connection.cursor() as cursor:
        cursor.execute("""
            WITH RefundSums AS (
                SELECT order_id, SUM(total_refund_amount) AS total_refund_amount_sum
                FROM order_returns
                GROUP BY order_id
            )
            SELECT 
                COUNT(DISTINCT CASE WHEN o.current_status NOT IN ('CANCELED', 'TOTAL_RETURN', 'PAYMENT_REFUSED', 'MISPLACED') THEN o.id END) AS daily_total_orders, 
                COALESCE(SUM(CASE WHEN o.current_status NOT IN ('CANCELED', 'TOTAL_RETURN', 'PAYMENT_REFUSED', 'MISPLACED') THEN o.final_price - COALESCE(rs.total_refund_amount_sum, 0) END), 0) AS daily_total_value,
                COUNT(DISTINCT CASE WHEN o.current_status IN ('DELIVERED', 'PARTIAL_DELIVERED', 'PARTIAL_RETURN', 'PROCESSING_RETURN') THEN o.id END) AS daily_delivered_orders,
                COALESCE(SUM(CASE WHEN o.current_status IN ('DELIVERED', 'PARTIAL_DELIVERED', 'PARTIAL_RETURN', 'PROCESSING_RETURN') THEN o.final_price - COALESCE(rs.total_refund_amount_sum, 0) END), 0) AS daily_delivered_value,
                COUNT(DISTINCT CASE WHEN o.current_status IN ('ON_ROUTE') THEN o.id END) AS daily_on_route_orders,
                COALESCE(SUM(CASE WHEN o.current_status IN ('ON_ROUTE') THEN o.final_price - COALESCE(rs.total_refund_amount_sum, 0) END), 0) AS daily_on_route_value,
                COUNT(DISTINCT CASE WHEN o.current_status IN ('IN_SEPARATION') THEN o.id END) AS daily_in_separation_orders,
                COALESCE(SUM(CASE WHEN o.current_status IN ('IN_SEPARATION') THEN o.final_price - COALESCE(rs.total_refund_amount_sum, 0) END), 0) AS daily_in_separation_value,
                COUNT(DISTINCT CASE WHEN o.current_status IN ('AWAITING_COLLECTION', 'WAITING_FOR_SELLER', 'PROCESSING_PAYMENT') THEN o.id END) AS daily_open_orders,
                COALESCE(SUM(CASE WHEN o.current_status IN ('AWAITING_COLLECTION', 'WAITING_FOR_SELLER', 'PROCESSING_PAYMENT') THEN o.final_price - COALESCE(rs.total_refund_amount_sum, 0) END), 0) AS daily_open_value,
                COUNT(DISTINCT CASE WHEN o.current_status IN ('CANCELED', 'TOTAL_RETURN', 'PAYMENT_REFUSED', 'MISPLACED') THEN o.id END) AS daily_canceled_orders,
                COALESCE(SUM(CASE WHEN o.current_status IN ('CANCELED', 'TOTAL_RETURN', 'PAYMENT_REFUSED', 'MISPLACED') THEN o.final_price END), 0) AS daily_canceled_value
            FROM orders o
            LEFT JOIN RefundSums rs ON o.id = rs.order_id
            WHERE (o.created_at AT TIME ZONE 'UTC' AT TIME ZONE 'America/Sao_Paulo')::DATE = CURRENT_DATE
        """)

        results = cursor.fetchone()

    formatted_values = [results[i] if i % 2 == 0 else format_currency(
        results[i]) for i in range(len(results))]
    return formatted_values


def get_seller_orders():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT s.name AS seller, 
                COUNT(DISTINCT o.id) AS total_orders
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

    return sellers, orders


def daily_view(request):

    # Sellers
    sellers, orders = get_seller_orders()

    # Dias
    working_days = get_working_days()
    elapsed_working_days = get_elapsed_working_days()

    # Valores Diários
    (daily_total_orders, daily_total_value,
     daily_delivered_orders, daily_delivered_value,
     daily_on_route_orders, daily_on_route_value,
     daily_in_separation_orders, daily_in_separation_value,
     daily_open_orders, daily_open_value,
     daily_canceled_orders, daily_canceled_value) = get_daily_order_totals()

    # Valores Mensais
    (monthly_total_value, monthly_delivered_value) = get_monthly_order_totals()
    monthly_accumulated_values = get_monthly_accumulated()

    # Meta
    total_meta = fetch_meta()

    initial_daily_meta_value = total_meta / \
        Decimal(working_days) if working_days > 0 else Decimal(0)

    new_daily_meta_value = abs(monthly_total_value - total_meta) / (Decimal(
        working_days) - Decimal(elapsed_working_days)) if working_days > 0 else Decimal(0)

    variation_daily_meta = ((new_daily_meta_value -
                            initial_daily_meta_value) / initial_daily_meta_value) * 100

    # Projeção do mês
    if elapsed_working_days > 0:
        daily_average_value = monthly_total_value / \
            Decimal(elapsed_working_days)
    else:
        daily_average_value = Decimal(0)

    remaining_working_days = working_days - elapsed_working_days

    monthly_projection = monthly_total_value + \
        (daily_average_value * Decimal(remaining_working_days))

    # Porcentagens
    delivered_value_clean = Decimal(str(daily_delivered_value).replace(
        "R$", "").replace(".", "").replace(",", ".").strip())

    if total_meta > 0:
        monthly_meta_percentage = (monthly_total_value / total_meta) * 100
    else:
        monthly_meta_percentage = 0

    if initial_daily_meta_value > Decimal("0"):
        daily_meta_percentage = (
            delivered_value_clean / initial_daily_meta_value) * Decimal("100")
    else:
        daily_meta_percentage = Decimal("0")

    # print("{:.2f}%".format(daily_meta_percentage))

    return render(request, "report-daily.html", {
        "sellers": sellers,
        "orders": orders,

        "working_days": working_days,
        "elapsed_working_days": elapsed_working_days,

        "daily_total_orders": daily_total_orders,
        "daily_total_value": daily_total_value,
        "daily_orders_delivered": daily_delivered_orders,
        "daily_value_delivered": daily_delivered_value,
        "daily_orders_on_route": daily_on_route_orders,
        "daily_value_on_route": daily_on_route_value,
        "daily_orders_in_separation": daily_in_separation_orders,
        "daily_value_in_separation": daily_in_separation_value,
        "daily_orders_open": daily_open_orders,
        "daily_value_open": daily_open_value,
        "daily_orders_canceled": daily_canceled_orders,
        "daily_value_canceled": daily_canceled_value,

        "monthly_total_value": format_currency(monthly_total_value),
        "monthly_delivered_value": format_currency(monthly_delivered_value),
        "monthly_accumulated_values": monthly_accumulated_values,

        "total_meta": format_currency(total_meta) if total_meta else "Meta not available",
        "initial_daily_meta_value": format_currency(initial_daily_meta_value),
        "new_daily_meta_value": format_currency(new_daily_meta_value),
        "variation_daily_meta": variation_daily_meta,

        "monthly_projection": format_currency(monthly_projection),

        "monthly_meta_percentage": "{:.2f}%".format(monthly_meta_percentage),
        "daily_meta_percentage": "{:.2f}%".format(daily_meta_percentage),

    })


def home_view(request):
    return render(request, "home.html", {})


def default_view(request):
    return render(request, "report-default.html", {})
