from django.db import models
from django.utils import timezone


import uuid

class CamposBasicos(models.Model):
    criado_em = models.DateTimeField(editable=False)
    ultima_atualizacao = models.DateTimeField()

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.criado_em:
            self.criado_em = timezone.now()
        self.ultima_atualizacao = timezone.now()
        super().save(*args, **kwargs)

class VetoresLogisticos(CamposBasicos):
    identificador = models.CharField(max_length=100)

    def gerar_identificador_unico(self):
        if not self.identificador:
            self.identificador = str(uuid.uuid4())

    def __str__(self):
        temp_abrigos_qs = Abrigos.objects.filter(vetor_logistico__identificador=self.identificador)
        if temp_abrigos_qs.exists():
            return f"{Abrigos.objects.filter(vetor_logistico__identificador=self.identificador).first().nome} - {self.identificador}"
        return f"{self.identificador}"
        

    def save(self, *args, **kwargs):
        self.gerar_identificador_unico()
        super().save(*args, **kwargs)

class CategoriasDeItens(CamposBasicos):
    nome = models.CharField(max_length=150)
    # Agua
    # Alimentos pereciveis
    # Alimentos não perecíveis
    # Alimentos para animais
    # Roupas Masculinas
    # Roupas Femininas
    # Higiene pessoal geral
    # Higiene pessoal feminina
    # Remédios geral
    # Remédios controlados

    def __str__(self):
        return self.nome
    class Meta:
        ordering = ["-ultima_atualizacao"]
        verbose_name_plural = "Categorias de Item"


ITEMS_TIPOS_DE_AUXILIO = (
    ("receber", "Receber"),
    ("doar", "Doar"),
    ("outro", "Outro"),
)
ITEMS_UNIDADES_DE_MEDIDA = (
    ("kilos", "Kilos"),
    ("litros", "Litros"),
    ("unidade", "Unidade"),
    ("outro", "Outro"),
)
class Itens(CamposBasicos):
    nome = models.CharField(
        null=True, blank=True, verbose_name="Nome", max_length=200
    )
    tipo_de_auxilio = models.CharField(
        choices=ITEMS_TIPOS_DE_AUXILIO,
        max_length=50,
        verbose_name="Tipo de Auxilio"
    )
    categoria = models.ForeignKey(
        "abrigos.CategoriasDeItens", verbose_name='Categoria do item', null=True, related_query_name="itens", on_delete=models.SET_NULL
    )
    unidade_de_medida = models.CharField(
        choices=ITEMS_UNIDADES_DE_MEDIDA,
        max_length=50,
        verbose_name="Unidade de medida",
        null=True
    )
    quantidade_total = models.IntegerField(
        null=False, blank=False, default=0, verbose_name="Quantidade total de itens"
    )
    quantidade_atual = models.IntegerField(
        null=False, blank=False, default=0, verbose_name="Quantidade atual de itens"
    )
    vetor_logistico = models.ForeignKey(
        "abrigos.VetoresLogisticos", 
        verbose_name='Vetor Logistico', 
        null=True, 
        related_query_name="abrigos", 
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.nome} - {self.categoria.nome}"

    class Meta:
        ordering = ["-ultima_atualizacao"]
        verbose_name_plural = "Itens"

class Enderecos(CamposBasicos): # TODO

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

class TiposDeAbrigo(models.Model):
    nome = models.CharField(max_length=150)
    # ("idoso", "Idoso"),
    # ("infantil", "Infantil"),
    # ("feminino", "Feminino"),
    # ("animal", "Animal"),
    # ("outro", "Outro"),
    def __str__(self):
        return self.nome

class Abrigos(CamposBasicos):
    nome = models.CharField(
        null=False, blank=False, verbose_name="Nome do abrigo", max_length=250
    )
    tipo = models.ForeignKey(
        "abrigos.TiposDeAbrigo", verbose_name='Tipo do abrigo', null=True, related_query_name="abrigos", on_delete=models.SET_NULL
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
        "abrigos.enderecos", verbose_name='Endereço', null=True, related_query_name="abrigos", on_delete=models.SET_NULL
    )
    vetor_logistico = models.ForeignKey(
        "abrigos.VetoresLogisticos", 
        verbose_name='Vetor Logistico', 
        null=True,
        blank=True,
        related_query_name="abrigos", 
        on_delete=models.SET_NULL        
    )

    class Meta:
        ordering = ["-ultima_atualizacao"]
        verbose_name_plural = "Abrigos"
        permissions = [
            ("administrador_de_abrigo", "Pode editar todas as informações do abrigo."),
            ("voluntario_de_abrigo", "Pode editar informações administrativas.")
        ]

    def __str__(self):
        return self.nome
    
    def save(self, *args, **kwargs):
        if not self.vetor_logistico:
            novo_vetor_logistico = VetoresLogisticos.objects.create()
            self.vetor_logistico = novo_vetor_logistico
        super().save(*args, **kwargs)