from django import forms

from .models import Movimentacao


class MovimentacaoForm(forms.ModelForm):
    class Meta:
        model = Movimentacao
        fields = ["produto", "tipo", "motivo", "quantidade"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["produto"].empty_label = "Selecione o produto"
        self.fields["tipo"].choices = [("", "Selecione o tipo")] + list(Movimentacao.TIPOS)
        self.fields["motivo"].choices = [("", "Selecione o motivo")] + list(Movimentacao.MOTIVOS)