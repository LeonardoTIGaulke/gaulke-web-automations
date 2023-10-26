from django.urls import path
from . import views

urlpatterns = [
    path("",  views.home_page, name="home"),
    path("login/", views.loginUser, name="login_user"),
    path("logout/", views.logoutUser, name="logout"),

    # ------------- FOLHA DE PAGAMENTO -------------
    path("payroll-relation/", views.payroll_relation, name="payroll_relation"),
    path("preview-payroll-relation/", views.preview_payroll_relation, name="preview_payroll_relation"),

    # ------------- GNRE -------------
    path("gnre-relation", views.gnre_relation, name="gnre_relation"),
    path("config-contas-grne/",  views.config_contas_gnre, name="config_contas_gnre"),
    path("preview-gnre-relation/", views.preview_gnre_relation, name="preview_gnre_relation"),
    
    # ------------- COBRANÇAS DE PAGEMENTO -------------
    path("cobrancas-pagas-relation/", views.relation_cobrancas_pagas, name="relation_cobrancas_pagas"),
    path("preview-relation-cobrancas-pagas/", views.preview_relation_cobrancas_pagas, name="preview_relation_cobrancas_pagas"),

    # TUTORIALS
    path("modos-de-uso/",  views.use_mode, name="use_mode"),
    path("use-login-e-logout/",  views.use_login_logout, name="use_login_logout"),


]