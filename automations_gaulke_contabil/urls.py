from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler404

urlpatterns = [
    path('admin/', admin.site.urls),
    path("automations/", include("app_payroll_relation.urls"))
]
handler404 = 'app_payroll_relation.views.error_404_view'
