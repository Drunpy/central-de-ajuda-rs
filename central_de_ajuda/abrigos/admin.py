from django.contrib import admin

from abrigos.models import *


class EnderecosDeAbrigosInline(admin.StackedInline):
    model = Enderecos
   
    extra = 1
    max_num = 1

    exclude = [
        "ultima_atualizacao"
    ]

class ItensDeAbrigosInline(admin.StackedInline):
    model = Itens
   
    extra = 3 # TODO: Verificar pq não está sendo respeitado, o admin só deixa incluir 1 item no abrigo.
    max_num = 50
    exclude = [
        "ultima_atualizacao"
    ]


class AbrigosAdmin(admin.ModelAdmin):
    model = Abrigos
    inlines = (
        EnderecosDeAbrigosInline,
        ItensDeAbrigosInline,
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

admin.site.register(CategoriasDeItens, CategoriasDeItensAdmin)

class ItensAdmin(admin.ModelAdmin):
    model = Itens

admin.site.register(Itens, ItensAdmin)