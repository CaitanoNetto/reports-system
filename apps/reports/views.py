from django.shortcuts import render
from django.db import connection


def home_view(request):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM home_table;")
    data = cursor.fetchall()
    return render(request, 'reports/home/home.html', {'data': data})


def daily_view(request):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM daily_table;")
    rows = cursor.fetchall()
    return render(request, 'reports/report-daily/report-daily.html', {'rows': rows})


def default_view(request):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM default_table;")
    items = [row[0] for row in cursor.fetchall()]
    return render(request, 'reports/report-default/report-default.html', {'items': items})
