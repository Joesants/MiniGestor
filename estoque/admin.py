from django.contrib import admin

from .models import Movimentacao, Produto


@admin.register(Produto)
class ProdutoAdmin (admin.ModelAdmin):
    list_display = ("nome", "preco", "quantidade", "estoque_minimo", "alerta")
    search_fields = ("nome", )

    @admin.display(boolean=True, description="Estoque baixo")
    def alerta(self, obj):
        return obj.estoque_baixo

@admin.register(Movimentacao)
class MovimentacaoAdmin(admin.ModelAdmin):
    list_display = ("produto", "tipo", "quantidade", "criado_em")
    list_filter = ("tipo", )

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_delete_permission(self, request, obj=None):
        return False

    admin.site.site_header = "MiniGestor"
    admin.site.index_title = "Painel de Controle"

    #admin.site.site_title = ""


    

