from django.urls import path
from . import views

urlpatterns = [
    path('registrar/', views.registrar_trilha, name='registrar'),
    path('get_tecnologias/', views.get_tecnologias, name='get_tecnologias'),

    path('filtro/', views.filtro, name='filtro'),

    path('post_conteudo/', views.post_conteudo, name='post_conteudo'),
    path('post_comentario/', views.post_comentario, name='post_comentario'),

    path('post_resposta/', views.post_resposta, name='post_resposta'),

    path('post_like/', views.post_like, name='post_like'),
    path('post_dislike/', views.post_dislike, name='post_dislike'),

    path('post_like_conteudo/', views.post_like_conteudo, name='post_like_conteudo'),
    path('post_dislike_conteudo/', views.post_dislike_conteudo, name='post_dislike_conteudo'),

    path('post_delete_comentario/', views.post_delete_comentario, name='post_delete_comentario'),

    path('secoes/<int:tecnologia_id>/', views.secoes, name="secoes"),
    path('conteudo/<int:secao_id>/', views.conteudo, name='conteudo'),

    path('conteudo/<int:secao_id>/gerar_certificado', views.gerar_certificado, name='gerar_certificado'),

    path('conteudo/validar/<int:solicitacao_id>/', views.validar_conteudo, name='validar_conteudo'),
    path('conteudo/validar/<int:solicitacao_id>/aprovar/', views.aprovar_conteudo, name='aprovar_conteudo'),

    path('conteudo/validar_edicao/<int:solicitacao_id>/', views.validar_edicao_conteudo, name='validar_edicao_conteudo'),
    path('conteudo/validar_edicao/<int:solicitacao_id>/aprovar/', views.aprovar_edicao_conteudo, name='aprovar_edicao_conteudo'),
    
    path('conteudo/validar_exclusao/<int:solicitacao_id>/', views.validar_exclusao_conteudo, name='validar_exclusao_conteudo'),
    path('conteudo/validar_exclusao/<int:solicitacao_id>/aprovar/', views.aprovar_exclusao_conteudo, name='aprovar_exclusao_conteudo'),

    path('conteudo/validar/<int:solicitacao_id>/rejeitar/', views.rejeitar_solicitacao_conteudo, name='rejeitar_solicitacao_conteudo'),

    path('conteudo/editar/<int:conteudo_id>/', views.editar_conteudo, name='editar_conteudo'),
    path('conteudo/editar/<int:conteudo_id>/solicitar_edicao/', views.gerar_solicitacao_edicao, name='gerar_solicitacao_edicao'),
    path('conteudo/editar/<int:conteudo_id>/solicitar_exclusao/', views.gerar_solicitacao_exclusao, name='gerar_solicitacao_exclusao'),

    path('conteudo/historico/', views.historico_assistido, name='historico_assistido'),
    path('conteudo/post_delete_historico/<int:usuario_id>/', views.post_delete_historico, name='post_delete_historico'),
    path('conteudo/conteudo_postado/', views.conteudo_postado, name='conteudo_postado'),

    path('conteudo/verificar_baixa/', views.verificar_baixa_conteudo, name='verificar_baixa_conteudo'),
    path('conteudo/validar_baixa/<int:conteudo_id>/', views.validar_baixa_conteudo, name='validar_baixa_conteudo'),
    path('conteudo/validar_baixa/<int:conteudo_id>/executar_baixa/', views.executar_baixa_conteudo, name='executar_baixa_conteudo'),

    path('conteudo/<int:comentario_id>/gerar_sinalizacao_comentario/', views.gerar_sinalizacao_comentario, name='gerar_sinalizacao_comentario'),
    path('conteudo/<int:conteudo_id>/gerar_sinalizacao_conteudo/', views.gerar_sinalizacao_conteudo, name='gerar_sinalizacao_conteudo'),

    path('conteudo/em_alta/', views.em_alta, name='em_alta'),
    path('', views.trilhas, name='index'),
    path('conteudo/is_owner/<int:conteudo_id>/', views.is_owner, name='is_owner'),

    path('divulgar/', views.divulgar_trilhas, name='divulgar_trilhas'),
    path('divulgar/postar/', views.divulgar_trilhas_postar, name='divulgar_trilhas_postar'),

    path('notificar_abandono/', views.notificar_usuarios_abandono, name='notificar_usuarios_abandono'),
]

