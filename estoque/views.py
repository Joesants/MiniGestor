from django.db.models import F
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from .form import MovimentacaoForm
from .models import Movimentacao, Produto


class ProdutoListView(ListView):
    model = Produto
    template_name = "estoque/produto_list.html"

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto["movimentacoes"] = Movimentacao.objects.select_related("produto")[:10]
        return contexto


class ComprarListView(ListView):
    model = Produto
    template_name = "estoque/comprar_list.html"

    def get_queryset(self):
        return (
            Produto.objects.filter(quantidade__lte=F("estoque_minimo"))
            .annotate(falta=F("estoque_minimo") - F("quantidade"))
            .order_by("nome")
        )


class ProdutoCreateView(CreateView):
    model = Produto
    fields = ["nome", "unidade", "preco", "quantidade", "estoque_minimo"]
    template_name = "estoque/form.html"
    success_url = reverse_lazy("produto_list")
    extra_context = {"titulo": "Novo produto"}


class ProdutoUpdateView(UpdateView):
    model = Produto
    fields = ["nome", "unidade", "preco", "estoque_minimo"]
    template_name = "estoque/form.html"
    success_url = reverse_lazy("produto_list")
    extra_context = {"titulo": "Editar produto"}


class MovimentacaoCreateView(CreateView):
    model = Movimentacao
    form_class = MovimentacaoForm
    template_name = "estoque/form.html"
    success_url = reverse_lazy("produto_list")
    extra_context = {"titulo": "Registrar entrada ou saída"}