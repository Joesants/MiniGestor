from django import forms

from .models import Movimentacao


class MovimentacaoForm(forms.ModelForm):
    class Meta:
        model = Movimentacao
        fields = ["produto", "tipo", "quantidade"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["produto"].empty_label = "Selecione o produto"
        self.fields["tipo"].choices = [("", "Selecione o tipo")] + list(Movimentacao.TIPOS)