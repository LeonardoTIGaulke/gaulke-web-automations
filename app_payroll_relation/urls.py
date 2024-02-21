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
    path("relacao-gnre-base-nova/", views.post_file_fastAPI_relacao_GNRE_BASE_NOVA, name="post_file_fastAPI_relacao_GNRE_BASE_NOVA"),

    path("relacao-entrada-titulos-desc-sicoob/", views.post_file_entrada_titulos_desc_sicoob, name="post_file_entrada_titulos_desc_sicoob"),
    path("relacao-cobrancas-pagas/", views.post_file_fastAPI_relacao_cobrancas_pagas, name="post_file_fastAPI_relacao_cobrancas_pagas"),
    path("relacao-relatorio-beneficiario-civia/", views.post_file_fastAPI_relacao_relatorio_beneficiario_civia, name="post_file_fastAPI_relacao_relatorio_beneficiario_civia"),
    
    path("config-contas-grne/",  views.config_contas_gnre, name="config_contas_gnre"),
    path("relacao-decorise/", views.post_file_fastAPI_relacao_decorise, name="post_file_fastAPI_relacao_decorise"),
    path("relacao-arao-dos-santos/", views.post_file_fastAPI_relacao_arao_dos_santos, name="post_file_fastAPI_relacao_arao_dos_santos"),
    path("relacao-grupo-DAB/", views.post_file_fastAPI_relacao_grupo_DAB, name="post_file_fastAPI_relacao_grupo_DAB"),
    path("relacao-contas-a-receber-inova/", views.post_file_fastAPI_relacao_contas_a_receber_inova, name="post_file_fastAPI_relacao_contas_a_receber_inova"),
    path("relacao-contas-a-pagar-ponto-certo/", views.post_file_fastAPI_relacao_contas_a_pagar_ponto_certo, name="post_file_fastAPI_relacao_contas_a_pagar_ponto_certo"),
    path("relacao-contas-a-pagar-garra/", views.post_file_fastAPI_relacao_contas_a_pagar_garra, name="post_file_fastAPI_relacao_contas_a_pagar_garra"),

    # -----------------------------------------------------------------
    # ------------------- COMPROVANTES DE PAGAMENTOS ------------------
    # -----------------------------------------------------------------
    path("relacao-comprovante-banco-do-brasil/", views.post_file_fastAPI_comprovante_banco_do_brasil, name="post_file_fastAPI_comprovante_banco_do_brasil"),
    path("relacao-comprovante-banco-bradesco/", views.post_file_fastAPI_comprovante_banco_bradesco, name="post_file_fastAPI_comprovante_banco_bradesco"),
    path("relacao-comprovante-banco-sicredi/", views.post_file_fastAPI_comprovante_banco_sicredi, name="post_file_fastAPI_comprovante_banco_sicredi"),
    path("relacao-comprovante-banco-sicoob/", views.post_file_fastAPI_comprovante_banco_sicoob, name="post_file_fastAPI_comprovante_banco_sicoob"),
    path("relacao-comprovante-banco-itau/", views.post_file_fastAPI_comprovante_itau, name="post_file_fastAPI_comprovante_banco_itau"),
    path("relacao-comprovante-banco-civia/", views.post_file_fastAPI_comprovante_civia, name="post_file_fastAPI_comprovante_banco_civia"),
    path("relacao-comprovante-recebimentos-TELL/", views.post_file_fastAPI_comprovante_recebimentos_TELL, name="post_file_fastAPI_comprovante_recebimentos_TELL"),
    path("relacao-comprovante-pagamentos-TELL/", views.post_file_fastAPI_comprovante_pagamentos_TELL, name="post_file_fastAPI_comprovante_pagamentos_TELL"),


    # ------------------------------------------------------------------
    # ------------------- CRIAÇÃO DE REGRAS DINÂMICAS ------------------
    # ------------------------------------------------------------------
    path("all-comnpanies-clients/", views.all_companies_clients, name="all_companies_clients"),
    path("get-all-comnpanies-clients/", views.get_all_companies_clients, name="get_all_companies_clients"),
    path("query-all-comnpanies-clients/", views.query_account_all_companies_clients, name="query_account_all_companies_clients"),

    path("create-new-tag-rule/", views.create_new_tag_rule, name="create_new_tag_rule"),

    path("create-new-tag/", views.create_new_tag, name="create_new_tag"),
    path("get-all-tags-rules/", views.get_all_tags_rules, name="get_all_tags_rules"),

    path("calculate-stock-H020/", views.calculate_stock_H020, name="calculate_stock_H020"),


    # -----------------------------------------------------------------------------------
    # ------------------ CONFIGURAÇÃO DE PLANO DE CONTAS ANTIXO x NOVO ------------------
    # -----------------------------------------------------------------------------------
    path("config-plano-de-contas/", views.config_plano_de_contas, name="config_plano_de_contas"),
    path("post-plano-de-contas/", views.post_plano_de_contas, name="post_plano_de_contas"),
    path("post-update-plano-de-contas/", views.post_update_plano_de_contas, name="post_update_plano_de_contas"),

    
    # -------------  DASHBOARDS -------------
    path("dashboard-visao-geral/", views.dashboard_visao_geral, name="dashboard_visao_geral"),


    # ------------- TUTORIALS -------------
    path("modos-de-uso/",  views.use_mode, name="use_mode"),
    path("use-login-e-logout/",  views.use_login_logout, name="use_login_logout"),


]