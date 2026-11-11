from django.urls import path

from . import views

urlpatterns = [
    path("", views.ProdutoListView.as_view(), name="produto_list"),
    path("produtos/novo/", views.ProdutoCreateView.as_view(), name="produto_novo"),
    path("movimentacoes/nova/", views.MovimentacaoCreateView.as_view(), name="movimentacao_nova"),
    path("produtos/<int:pk>/editar/", views.ProdutoUpdateView.as_view(), name="produto_editar"),
]