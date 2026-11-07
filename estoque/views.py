from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from .models import Movimentacao, Produto

from .form import MovimentacaoForm


class ProdutoListView(ListView):
    model = Produto
    template_name = "estoque/produto_list.html"

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto["movimentacoes"] = Movimentacao.objects.select_related("produto")[:10]
        return contexto


class ProdutoCreateView(CreateView):
    model = Produto
    fields = ["nome", "preco", "quantidade", "estoque_minimo"]
    template_name = "estoque/form.html"
    success_url = reverse_lazy("produto_list")
    extra_context = {"titulo": "Novo produto"}


class MovimentacaoCreateView(CreateView):
    model = Movimentacao
    form_class = MovimentacaoForm
    template_name = "estoque/form.html"
    success_url = reverse_lazy("produto_list")
    extra_context = {"titulo": "Registrar entrada ou saída"}