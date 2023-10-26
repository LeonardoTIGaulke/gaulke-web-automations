from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("automations/", include("app_payroll_relation.urls"))
]
