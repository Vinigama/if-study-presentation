from django.urls import path
from . import views

urlpatterns = [
    path('router_requisicao/<requisicao_id>/', views.router_requisicao, name='router_requisicao'),
]