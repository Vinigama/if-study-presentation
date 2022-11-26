from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', auth_views.LoginView.as_view(
        template_name='usuarios/login.html',
        redirect_authenticated_user=True
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('perfil/informacoes/<int:perfil_id>/', views.perfil, name='perfil'),
    path('perfil/editar/<int:perfil_id>/', views.editar_perfil, name='editar_perfil'),
    path('perfil/senha/<int:perfil_id>/', views.trocar_senha, name='trocar_senha'),
    path('perfil/conteudos/<int:perfil_id>/', views.perfil_conteudos, name='perfil_conteudos'),
    path('perfil/is_owner/<int:perfil_id>/', views.is_owner ,name='is_owner'),
    path('sinalizar_perfil/<int:perfil_id>/', views.gerar_sinalizacao_perfil, name='sinalizar_perfil'),
    path('verificar_perfil/<int:perfil_id>/', views.envio_confirmacao_email, name='envio_confirmacao_email'),
    path('ativar/<uidb64>/<token>/', views.ativar_perfil, name='ativar_perfil'),
]
