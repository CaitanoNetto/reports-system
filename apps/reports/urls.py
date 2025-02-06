from django.urls import path
from apps.reports.views import home_view, daily_view, default_view

urlpatterns = [
    path("", home_view, name="home"),
    path("daily/", daily_view, name="report-daily"),
    path("default/", default_view, name="report-default"),
]
