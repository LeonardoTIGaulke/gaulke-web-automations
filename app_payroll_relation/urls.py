from django.urls import path
from . import views

urlpatterns = [
    path("",  views.home_page, name="home"),
    path("login/", views.loginUser, name="login_user"),
    path("logout/", views.logoutUser, name="logout"),

    # -------------  IMPORTAÇÃO DE ARQUIVOS -------------
    path("relacao-comprovante-banco-do-brasil/", views.post_file_fastAPI_comprovante_banco_do_brasil, name="post_file_fastAPI_comprovante_banco_do_brasil"),
    path("relacao-folha-pagamento-por-empregado/", views.post_file_fastAPI_folha_por_empregado, name="post_file_fastAPI_folha_por_empregado"),
    path("relacao-GNRE/", views.post_file_fastAPI_relacao_GNRE, name="post_file_fastAPI_relacao_GNRE"),
    path("relacao-entrada-titulos-desc-sicoob/", views.post_file_entrada_titulos_desc_sicoob, name="post_file_entrada_titulos_desc_sicoob"),
    path("relacao-cobrancas-pagas/", views.post_file_fastAPI_relacao_cobrancas_pagas, name="post_file_fastAPI_relacao_cobrancas_pagas"),

    path("config-contas-grne/",  views.config_contas_gnre, name="config_contas_gnre"),
    
    # TUTORIALS
    path("modos-de-uso/",  views.use_mode, name="use_mode"),
    path("use-login-e-logout/",  views.use_login_logout, name="use_login_logout"),


]

# # ------------- FOLHA DE PAGAMENTO -------------
# path("payroll-relation/", views.payroll_relation, name="payroll_relation"),
# path("preview-payroll-relation/", views.preview_payroll_relation, name="preview_payroll_relation"),

# # ------------- GNRE -------------
# path("gnre-relation", views.gnre_relation, name="gnre_relation"),
# path("preview-gnre-relation/", views.preview_gnre_relation, name="preview_gnre_relation"),

# # ------------- COBRANÇAS DE PAGEMENTO -------------
# path("cobrancas-pagas-relation/", views.relation_cobrancas_pagas, name="relation_cobrancas_pagas"),
# path("preview-relation-cobrancas-pagas/", views.preview_relation_cobrancas_pagas, name="preview_relation_cobrancas_pagas"),

# # ------------- TÍTULOS PAGOS SICOOB -------------
# path("relation-titulos-pagos-sicoob/", views.relation_titulos_pagos_sicoob, name="relation_titulos_pagos_sicoob"),
# path("preview-relation-titulos-pagos-sicoob/", views.preview_titulos_pagos_sicoob, name="preview_titulos_pagos_sicoob"),

# # ------------- PREVIEWS GENERICS -------------
# path("preview-generic/", views.preview_generic, name="preview_generic"),
# path("create-base-preview-to-text/", views.create_base_preview_to_text, name="create_base_preview_to_text"),