from django.urls import path

from . import views

urlpatterns = [
    path("", views.ProdutoListView.as_view(), name="produto_list"),
    path("comprar/", views.ComprarListView.as_view(), name="comprar_list"),
    path("produtos/novo/", views.ProdutoCreateView.as_view(), name="produto_novo"),
    path("produtos/<int:pk>/editar/", views.ProdutoUpdateView.as_view(), name="produto_editar"),
    path("movimentacoes/nova/", views.MovimentacaoCreateView.as_view(), name="movimentacao_nova"),
]