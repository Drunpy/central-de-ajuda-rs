from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from abrigos.models import *

class ExtraDataInline(admin.StackedInline):
        model = ExtraData
        fk_name = "usuario"
        fields = (
            "locais_de_atuacao",
        )
        extra = 1
        max_num = 1

class CustomUserAdmin(UserAdmin):
    inlines = (ExtraDataInline,)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

class EnderecosDeAbrigosInline(admin.StackedInline):
    model = Enderecos
   
    extra = 1
    max_num = 1

    exclude = [
        "ultima_atualizacao",
        "identificador"
    ]

class AbrigosAdmin(admin.ModelAdmin):
    model = Abrigos
    inlines = (
        EnderecosDeAbrigosInline,
    )
    exclude = [
        "endereco",
        "vetor_logistico",
        "ultima_atualizacao"
    ]         

admin.site.register(Abrigos, AbrigosAdmin)

class TiposDeAbrigosAdmin(admin.ModelAdmin):
    model = TiposDeAbrigo

admin.site.register(TiposDeAbrigo, TiposDeAbrigosAdmin)

class CategoriasDeItensAdmin(admin.ModelAdmin):
    model = CategoriasDeItens

    exclude = [
        "ultima_atualizacao",
        "identificador"
    ]

admin.site.register(CategoriasDeItens, CategoriasDeItensAdmin)

class ItensAdmin(admin.ModelAdmin):
    model = Itens

    exclude = [
        "ultima_atualizacao",
        "identificador"
    ]

    def get_changeform_initial_data(self, request):
        locais_de_atuacao_do_usuario = VetoresLogisticos.objects.filter(voluntarios__usuario=request.user)
        if locais_de_atuacao_do_usuario.exists(): # Seleciona o último local associado ao usuário
            return {
                "vetor_logistico": locais_de_atuacao_do_usuario.last(),
            }


admin.site.register(Itens, ItensAdmin)