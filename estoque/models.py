from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models, transaction

class Produto(models .Model):
    nome = models .CharField(max_length=120)
    preco = models .DecimalField("preço" , max_digits=8 , decimal_places=2)
    quantidade = models .PositiveBigIntegerField(default=0)
    estoque_minimo = models .PositiveBigIntegerField("estoque mínimo" , default=5)


    def __str__(self):
        return self .nome
    @property
    def estoque_baixo(self):
        return self .quantidade <= self .estoque_minimo
class Movimentacao (models .Model):
        ENTRADA = "E"
        SAIDA = "S"
        TIPOS = [(ENTRADA, "Entrada"), (SAIDA, "Saída" )]

        produto = models.ForeignKey(Produto, on_delete=models.PROTECT, related_name="movimentacoes")
        tipo = models.CharField(max_length=1, choices=TIPOS)
        quantidade = models.PositiveBigIntegerField(validators=[MinValueValidator(1)])
        criado_em = models.DateTimeField(auto_now_add=True)

        def __str__(self):
            return F"{self.get_tipo_display()} de {self.quantidade} x {self.produto}"

        def clean(self):
            if (self.tipo == self.SAIDA and self.produto_id and self.quantidade
                    and self.quantidade > self.produto.quantidade):
                raise ValidationError("Estoque insuficiente para essa saída.")

        def save(self, *args, **kwargs):
            with transaction.atomic():
                sinal = 1 if self.tipo == self.ENTRADA else -1
                self.produto.quantidade += sinal * self.quantidade
                self.produto.save(update_fields=['quantidade'])
                super().save(*args, **kwargs)
        class Meta:
            verbose_name = "movimentação"
            verbose_name_plural = "movimentações"
            ordering = ["-criado_em"]