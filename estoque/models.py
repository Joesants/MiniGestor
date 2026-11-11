from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models, transaction


class Produto(models.Model):
    nome = models.CharField(max_length=120)
    unidade = models.CharField(
        max_length=2,
        choices=[("un", "un"), ("kg", "kg"), ("L", "L")],
        default="un",
    )
    preco = models.DecimalField("preço", max_digits=8, decimal_places=2)
    quantidade = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    estoque_minimo = models.DecimalField("estoque mínimo", max_digits=10, decimal_places=2, default=5)

    def __str__(self):
        return self.nome

    @property
    def estoque_baixo(self):
        return self.quantidade <= self.estoque_minimo


class Movimentacao(models.Model):
    ENTRADA = "E"
    SAIDA = "S"
    TIPOS = [(ENTRADA, "Entrada"), (SAIDA, "Saída")]
    MOTIVOS = [
        ("compra", "Compra"),
        ("uso", "Uso / venda"),
        ("perda", "Perda"),
        ("vencimento", "Vencimento"),
        ("ajuste", "Ajuste de contagem"),
    ]

    produto = models.ForeignKey(Produto, on_delete=models.PROTECT, related_name="movimentacoes")
    tipo = models.CharField(max_length=1, choices=TIPOS)
    quantidade = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))]
    )
    motivo = models.CharField(max_length=10, choices=MOTIVOS, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "movimentação"
        verbose_name_plural = "movimentações"
        ordering = ["-criado_em"]

    def __str__(self):
        return f"{self.get_tipo_display()} de {self.quantidade} x {self.produto}"

    def clean(self):
        if (self.tipo == self.SAIDA and self.produto_id and self.quantidade
                and self.quantidade > self.produto.quantidade):
            raise ValidationError("Estoque insuficiente para essa saída.")

    def save(self, *args, **kwargs):
        with transaction.atomic():
            sinal = 1 if self.tipo == self.ENTRADA else -1
            self.produto.quantidade += sinal * self.quantidade
            self.produto.save(update_fields=["quantidade"])
            super().save(*args, **kwargs)