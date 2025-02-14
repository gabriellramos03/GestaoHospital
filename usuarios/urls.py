from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('home/', views.home, name='home'),
    path('lancar/', views.lancar, name='lancar'),
    path('alterar/', views.alterar, name='alterar'),
    path('visualizar/', views.visualizar_medicos, name='visualizar'),
    path('logout/', views.logout, name='logout'),
    path('excluir_verificacao/<int:pk>', views.excluir_verificacao, name="excluir_verificacao"),
    path('excluir/<int:pk>', views.excluir, name="excluir"),
    path('editar_verificacao/<int:pk>', views.editar_verificacao, name="editar_verificacao"),
    path('editar/<int:pk>', views.editar, name="editar"),
    path('sobre/', views.sobre, name='sobre'),  
    path('contatos/', views.contatos, name='contatos')
]

