from django.db import models

class VetorLogistico(models.Model): # TODO
    nome = models.CharField(max_length=150)

# class Items(models.Model): # TODO
#     nome = 
#     quantidade = 
#     categoria = 
#     proxy_logistico = models.ForeignKey(
#         "abrigos.VetorLogistico", verbose_name='Abrigo', null=True, related_name="enderecos", on_delete=models.CASCADE
#     )

class BasicFields(models.Model):
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name="Data de criação no sistema")
    ultima_atualizacao = models.DateTimeField(auto_now=True, verbose_name="Ultima atualização")

class Enderecos(models.Model): # TODO

    municipio = models.CharField(null=True, blank=True, verbose_name="Município", max_length=200)
    bairro = models.CharField(null=True, blank=True, verbose_name="Bairro", max_length=200)
    logradouro = models.CharField(null=True, blank=True, verbose_name="Logradouro", max_length=200)
    numero = models.CharField(null=True, blank=True, verbose_name="Número", max_length=50)
    complemento = models.CharField(null=True, blank=True, verbose_name="Complemento", max_length=200)

    zona = models.CharField(
        null=True,
        blank=True, 
        verbose_name="Zona", 
        max_length=100
    )

    cod_postal = models.CharField(
        null=True, 
        blank=True, 
        verbose_name="CEP", 
        max_length=20
    )
    anotacao = models.TextField(
        blank=True, verbose_name="Anotações"
    )

    lat_long = models.CharField( # Formato: [x.xxx, y.yyy]
        max_length=30, null=True, blank=True, verbose_name="Latitude, Longitude",
    )

class TiposDeAbrigo(models.Model): # TODO
    nome = models.CharField(max_length=150)
    # TIPOS_DE_ABRIGO = (
    #         ("idoso", "Idoso"),
    #         ("infantil", "Infantil"),
    #         ("feminino", "Feminino"),
    #         ("animal", "Animal"),
    #         ("outro", "Outro"),
    #     )

class Abrigos(BasicFields):
    nome = models.CharField(
        null=False, blank=False, verbose_name="Nome do abrigo", max_length=250
    )
    tipo = models.ForeignKey(
        "abrigos.TiposDeAbrigo", verbose_name='Tipo do abrigo', null=True, related_name="tipo", on_delete=models.CASCADE
    )
    descricao = models.TextField(
        blank=True, verbose_name="Descrição"
    )
    capacidade_total_de_abrigados = models.IntegerField(
        null=False, blank=False, default=0, verbose_name="Capacidade total de abrigados"
    )
    capacidade_atual_de_abrigados = models.IntegerField(
        null=False, blank=False, default=0, verbose_name="Capacidade atual de abrigados"
    )
    informacoes_para_voluntarios = models.TextField(
        blank=True, verbose_name="Informações para voluntários"
    )
    informacoes_de_contato = models.TextField(
        blank=True, verbose_name="Informações de contato"
    )
    
    endereco = models.ForeignKey(
        "abrigos.enderecos", verbose_name='Abrigo', null=True, related_name="enderecos", on_delete=models.CASCADE
    )

    class Meta:
        ordering = ["-ultima_atualizacao"]
        verbose_name_plural = "Abrigos"
        permissions = [
            ("administrador_de_abrigo", "Pode editar todas as informações do abrigo."),
            ("voluntario_de_abrigo", "Pode editar informações administrativas.")
        ]