from django.db import models

class BasicFields(models.Model):
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name="Data de criação no sistema")
    ultima_atualizacao = models.DateTimeField(auto_now=True, verbose_name="Ultima atualização")

TIPOS_DE_ABRIGO = (
        ("idoso", "Idoso"),
        ("infantil", "Infantil"),
        ("animal", "Animal"),
        ("outro", "Outro"),
    )

class Abrigos(BasicFields):
    nome = models.CharField(
        null=False, blank=False, verbose_name="Nome do abrigo", max_length=250
    )
    tipo = models.CharField(
        max_length=50,
        choices=TIPOS_DE_ABRIGO,
        verbose_name="Tipo de abrigo",
    )
    descricao = models.TextField(
        blank=True, verbose_name="Descrição"
    )
    capacidade_total_de_abrigados = models.IntegerField(
        null=False, blank=False, default=0, verbose_name="Capacidade total de abrigados"
    )
    informacoes_para_voluntarios = models.TextField(
        blank=True, verbose_name="Informações para voluntários"
    )
    informacoes_de_contato = models.TextField(
        blank=True, verbose_name="Informações de contato"
    )
    lat_long = models.CharField( # Formato: [x.xxx, y.yyy]
        max_length=30, null=True, blank=True, verbose_name="Latitude, Longitude",
    )

    class Meta:
        ordering = ["-ultima_atualizacao"]
        verbose_name_plural = "Abrigos"
        permissions = [
            ("administrador_de_abrigo", "Pode editar todas as informações do abrigo."),
            ("voluntario_de_abrigo", "Pode editar informações administrativas.")
        ]