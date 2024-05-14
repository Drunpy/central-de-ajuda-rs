from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

import uuid


class ExtraData(models.Model):
    usuario = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        related_query_name="extradata"
    )
    locais_de_atuacao = models.ManyToManyField(
        "abrigos.VetoresLogisticos", 
        verbose_name='Locais de Atuação',
        related_query_name="voluntarios",
    )
    telefone_para_contato = models.CharField(
        null=True,
        blank=True,
        verbose_name="Telefone para contato", 
        max_length=25,
        help_text="Digite apenas números, utilizando o DDD na frente. Sem espaços ou caracteres especiais."
    )

    def __str__(self):
        return f"{self.usuario.username}"

    class Meta:
        verbose_name = "Ficha do Usuário"
        permissions = [
            ("administrador", "Pode editar todas as informações de um estabelecimento."),
            ("voluntario_em_campo", "Pode editar informações administrativas.")
        ]


class CamposBasicos(models.Model):
    identificador = models.CharField(max_length=100)
    criado_em = models.DateTimeField(editable=False)
    ultima_atualizacao = models.DateTimeField()

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.criado_em:
            self.criado_em = timezone.now()
        self.ultima_atualizacao = timezone.now()
        self.gerar_identificador_unico()
        super().save(*args, **kwargs)

    def gerar_identificador_unico(self):
        if not self.identificador:
            self.identificador = str(uuid.uuid4())

class VetoresLogisticos(CamposBasicos):

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

    vetor_logistico = models.ForeignKey(
        "abrigos.VetoresLogisticos", 
        verbose_name='Vetor Logistico',
        related_query_name="itens",
        null=True,
        on_delete=models.SET_NULL,
    )
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
    complemento = models.CharField(
        null=True, 
        blank=True, 
        verbose_name="Complemento", 
        max_length=200
    )

    zona = models.CharField(
        null=True,
        blank=True, 
        verbose_name="Zona",
        max_length=100,
        help_text="Exemplo: Zona Norte, Zona Sul"
    )

    cod_postal = models.CharField(
        null=True, 
        blank=True, 
        verbose_name="CEP",
        max_length=20,
        help_text="Digite apenas números."
    )
    anotacao = models.TextField(
        blank=True, 
        verbose_name="Anotações",
        help_text="Digite informações complementares de como as pessoas podem chegar neste endereço."
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
    tipo = models.ManyToManyField(
        "abrigos.TiposDeAbrigo", 
        verbose_name='Tipo de abrigo', 
        related_query_name="abrigos", 
    )
    descricao = models.TextField(
        blank=True, 
        verbose_name="Descrição", 
        help_text="Informações gerais sobre o abrigo."
    )
    informacoes_para_voluntarios = models.TextField(
        blank=True, 
        verbose_name="Informações para voluntários",
        help_text="Informações para voluntários que desejam contribuir de alguma forma."
    )
    informacoes_de_contato = models.TextField(
        blank=True, 
        verbose_name="Informações de contato",
        help_text="Informações para pessoas que desejam entrar em contato."
    )
    capacidade_total_de_abrigados = models.IntegerField(
        null=False, blank=False, default=0, verbose_name="Capacidade total de abrigados"
    )
    capacidade_atual_de_abrigados = models.IntegerField(
        null=False, blank=False, default=0, verbose_name="Capacidade atual de abrigados"
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

    def __str__(self):
        return self.nome
    
    def save(self, *args, **kwargs):
        if not self.vetor_logistico:
            novo_vetor_logistico = VetoresLogisticos.objects.create()
            self.vetor_logistico = novo_vetor_logistico
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["-ultima_atualizacao"]
        verbose_name_plural = "Abrigos"