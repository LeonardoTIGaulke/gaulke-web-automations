from django.urls import path
from . import views

urlpatterns = [
    path("",  views.home_page, name="home"),
    path("login/", views.loginUser, name="login_user"),
    path("logout/", views.logoutUser, name="logout"),

    # -----------------------------------------------------------------
    # --------------------  IMPORTAÇÃO DE ARQUIVOS --------------------
    # -----------------------------------------------------------------

    path("relacao-folha-pagamento-por-empregado/", views.post_file_fastAPI_folha_por_empregado, name="post_file_fastAPI_folha_por_empregado"),
    path("relacao-GNRE/", views.post_file_fastAPI_relacao_GNRE, name="post_file_fastAPI_relacao_GNRE"),
    path("relacao-entrada-titulos-desc-sicoob/", views.post_file_entrada_titulos_desc_sicoob, name="post_file_entrada_titulos_desc_sicoob"),
    path("relacao-cobrancas-pagas/", views.post_file_fastAPI_relacao_cobrancas_pagas, name="post_file_fastAPI_relacao_cobrancas_pagas"),
    
    path("config-contas-grne/",  views.config_contas_gnre, name="config_contas_gnre"),
    path("relacao-decorise/", views.post_file_fastAPI_relacao_decorise, name="post_file_fastAPI_relacao_decorise"),
    path("relacao-arao-dos-santos/", views.post_file_fastAPI_relacao_arao_dos_santos, name="post_file_fastAPI_relacao_arao_dos_santos"),
    
    path("relacao-grupo-DAB/", views.post_file_fastAPI_relacao_grupo_DAB, name="post_file_fastAPI_relacao_grupo_DAB"),

    # -----------------------------------------------------------------
    # ------------------- COMPROVANTES DE PAGAMENTOS ------------------
    # -----------------------------------------------------------------
    path("relacao-comprovante-banco-do-brasil/", views.post_file_fastAPI_comprovante_banco_do_brasil, name="post_file_fastAPI_comprovante_banco_do_brasil"),
    path("relacao-comprovante-banco-bradesco/", views.post_file_fastAPI_comprovante_banco_bradesco, name="post_file_fastAPI_comprovante_banco_bradesco"),
    path("relacao-comprovante-banco-sicredi/", views.post_file_fastAPI_comprovante_banco_sicredi, name="post_file_fastAPI_comprovante_banco_sicredi"),
    path("relacao-comprovante-banco-sicoob/", views.post_file_fastAPI_comprovante_banco_sicoob, name="post_file_fastAPI_comprovante_banco_sicoob"),





    # -------------  DASHBOARDS -------------
    path("dashboard-visao-geral/", views.dashboard_visao_geral, name="dashboard_visao_geral"),


    # ------------- TUTORIALS -------------
    path("modos-de-uso/",  views.use_mode, name="use_mode"),
    path("use-login-e-logout/",  views.use_login_logout, name="use_login_logout"),


]