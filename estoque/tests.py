from django.core.exceptions import ValidationError
from django.test import TestCase

from .models import Movimentacao, Produto

class EstoqueTests(TestCase):
    def setUp(self):
        self .produto = Produto.objects.create(
            nome = "Arroz 5kg" , preco="25.90" , quantidade=10, estoque_minimo=3
        )

    def test_entrada_soma_no_estoque(self):
        Movimentacao.objects.create(produto=self .produto, tipo="E", quantidade=5)
        self .produto.refresh_from_db()
        self .assertEqual(self.produto.quantidade, 15)

    def test_saida_subtrai_do_estoque(self):
        Movimentacao.objects.create(produto=self .produto, tipo="S", quantidade=4)
        self .produto.refresh_from_db()
        self .assertEqual(self.produto.quantidade, 6)   

    def test_saida_maior_que_estoque_e_invalida(self):
        mov = Movimentacao(produto=self .produto, tipo="S", quantidade=11)
        with self .assertRaises(ValidationError):
            mov.full_clean()

    def test_alerta_de_estoque_baixo(self):
        Movimentacao.objects.create(produto=self.produto, tipo="S", quantidade=8)
        self.produto.refresh_from_db()
        self.assertTrue(self.produto.estoque_baixo)