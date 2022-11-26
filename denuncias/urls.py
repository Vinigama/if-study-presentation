from django.urls import path, include
from . import views


urlpatterns = [
    path('comentarios/', views.sinalizacao_comentario, name='sinalizacao_comentario'),
    path('comentarios/apurar/<int:sinalizacao_id>/', views.apurar_comentario, name='apurar_comentario'),
    path('comentarios/historico/', views.historico_sinalizacao_comentario, name='historico_sinalizacao_comentario'),

    path('conteudos/', views.sinalizacao_conteudo, name='sinalizacao_conteudo'),
    path('conteudos/apurar/<int:sinalizacao_id>/', views.apurar_conteudo, name='apurar_conteudo'),
    path('conteudos/historico/', views.historico_sinalizacao_conteudo, name='historico_sinalizacao_conteudo'),

    path('perfis/', views.sinalizacao_perfil, name='sinalizacao_perfil'),
    path('perfis/apurar/<int:sinalizacao_id>/', views.apurar_perfil, name='apurar_perfil'),
    path('perfis/historico/', views.historico_sinalizacao_perfil, name='historico_sinalizacao_perfil')
]
