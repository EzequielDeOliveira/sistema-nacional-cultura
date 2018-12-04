from rest_framework import serializers
from drf_hal_json.fields import HalHyperlinkedIdentityField
from drf_hal_json import serializers as hal_serializers

from adesao.models import Municipio
from adesao.models import Uf
from adesao.models import Cidade
from adesao.models import Usuario
from planotrabalho.models import PlanoTrabalho
from planotrabalho.models import CriacaoSistema
from planotrabalho.models import OrgaoGestor
from planotrabalho.models import ConselhoCultural
from planotrabalho.models import FundoCultura
from planotrabalho.models import PlanoCultura
from planotrabalho.models import Conselheiro

from adesao.models import SistemaCultura
from planotrabalho.models import Componente
from adesao.models import EnteFederado


# Criacao do Sistema
class CriacaoSistemaSerializer(hal_serializers.HalModelSerializer):
    situacao = serializers.ReadOnlyField(source='situacao.descricao')

    class Meta:
        model = CriacaoSistema
        fields = ('lei_sistema_cultura', 'situacao')


class OrgaoGestorSerializer(hal_serializers.HalModelSerializer):
    situacao = serializers.ReadOnlyField(source='situacao.descricao')

    class Meta:
        model = OrgaoGestor
        fields = ('relatorio_atividade_secretaria',
                  'situacao')


class ConselhoCulturalSerializer(hal_serializers.HalModelSerializer):
    situacao = serializers.ReadOnlyField(source='situacao.descricao')

    class Meta:
        model = ConselhoCultural
        fields = ('ata_regimento_aprovado', 'situacao')


class ConselheiroSerializer(hal_serializers.HalModelSerializer):
    situacao = serializers.SerializerMethodField(source='situacao')

    class Meta:
        model = Conselheiro
        fields = ['nome', 'segmento', 'email', 'situacao',
                  'data_cadastro', 'data_situacao']

    def get_situacao(self, obj):
        return obj.get_situacao_display()


class FundoCulturaSerializer(hal_serializers.HalModelSerializer):
    situacao = serializers.ReadOnlyField(source='situacao.descricao')

    class Meta:
        model = FundoCultura
        fields = ('cnpj_fundo_cultura', 'lei_fundo_cultura',
                  'situacao')


class PlanoCulturaSerializer(hal_serializers.HalModelSerializer):
    situacao = serializers.ReadOnlyField(source='situacao.descricao')

    class Meta:
        model = PlanoCultura
        fields = ('relatorio_diretrizes_aprovadas', 'minuta_preparada',
                  'ata_reuniao_aprovacao_plano', 'ata_votacao_projeto_lei',
                  'lei_plano_cultura', 'situacao')


class ComponenteSCSerializer(serializers.ModelSerializer):
    situacao = serializers.ReadOnlyField(source='situacao')

    class Meta:
        model = Componente


class PlanoTrabalhoSCSerializer(hal_serializers.HalModelSerializer):
    criacao_lei_sistema = ComponenteSCSerializer(source='legislacao')
    criacao_orgao_gestor = ComponenteSCSerializer(source='orgao_gestor')
    criacao_plano_cultura = ComponenteSCSerializer(source='plano')
    criacao_fundo_cultura = ComponenteSCSerializer(source='fundo_cultura')
    criacao_conselho_cultural = ComponenteSCSerializer(source='conselho')
    # _embedded = serializers.SerializerMethodField(method_name='get_embedded')
    # self = HalHyperlinkedIdentityField(view_name='api:planotrabalho-detail')

    class Meta:
        model = SistemaCultura
        fields = ('id', 'self', 'criacao_lei_sistema', 'criacao_orgao_gestor',
                  'criacao_fundo_cultura', 'criacao_conselho_cultural')

class PlanoTrabalhoSerializer(hal_serializers.HalModelSerializer):
    criacao_lei_sistema_cultura = serializers.SerializerMethodField(source='criacao_sistema')
    criacao_orgao_gestor = serializers.SerializerMethodField(source='orgao_gestor')
    criacao_plano_cultura = serializers.SerializerMethodField(source='plano_cultura')
    criacao_fundo_cultura = serializers.SerializerMethodField(source='fundo_cultura')
    criacao_conselho_cultural = serializers.SerializerMethodField(source='conselho_cultural')
    _embedded = serializers.SerializerMethodField(method_name='get_embedded')
    self = HalHyperlinkedIdentityField(view_name='api:planotrabalho-detail')

    class Meta:
        model = SistemaCultura
        fields = ('id', 'self', 'criacao_lei_sistema_cultura',
                  'criacao_orgao_gestor', 'criacao_conselho_cultural',
                  'criacao_fundo_cultura', 'criacao_plano_cultura', '_embedded'
                )

    def get_sistema_cultura_local(self, obj):

        try:
            obj.usuario
        except Usuario.DoesNotExist:
            return None

        if obj.usuario.municipio is not None:
            context = {}
            context['request'] = self.context['request']
            serializer = MunicipioLinkSerializer(obj.usuario.municipio, context=context)
            return serializer.data
        else:
            return None

    def get_embedded(self, obj):
        municipio = self.get_sistema_cultura_local(obj=obj)
        embedded = ({'sistema_cultura_local': municipio})

        return embedded

    def get_criacao_orgao_gestor(self, obj):
        if obj.orgao_gestor is not None:
            serializer = OrgaoGestorSerializer(obj.orgao_gestor)
            return serializer.data
        else:
            return None

    def get_criacao_plano_cultura(self, obj):
        if obj.plano_cultura is not None:
            serializer = PlanoCulturaSerializer(obj.plano_cultura)
            return serializer.data
        else:
            return None

    def get_criacao_fundo_cultura(self, obj):
        if obj.fundo_cultura is not None:
            serializer = FundoCulturaSerializer(obj.fundo_cultura)
            return serializer.data
        else:
            return None

    def get_criacao_lei_sistema_cultura(self, obj):
        if obj.criacao_sistema is not None:
            serializer = CriacaoSistemaSerializer(obj.criacao_sistema)
            return serializer.data
        else:
            return None

    def get_criacao_conselho_cultural(self, obj):
        if obj.conselho_cultural is not None:
            serializer = ConselhoCulturalSerializer(obj.conselho_cultural)
            return serializer.data
        else:
            return None


# Cidade
class CidadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cidade
        fields = ('codigo_ibge', 'nome_municipio')


class UfSerializer(serializers.ModelSerializer):
    class Meta:
        model = Uf
        fields = ('codigo_ibge', 'sigla', 'nome_uf')


class MunicipioLinkSerializer(hal_serializers.HalModelSerializer):
    self = HalHyperlinkedIdentityField(view_name='api:sistemacultura-detail')

    class Meta:
        model = Municipio
        fields = ('self',)


class EnteFederadoSerializer(hal_serializers.HalModelSerializer):
    
    class Meta:
        model = EnteFederado
        fields = ("cod_ibge", "nome", "territorio", "populacao", "idh", "is_municipio")


class SistemaCulturaSerializer(hal_serializers.HalModelSerializer):
    # ente_federado = serializers.CharField(source='ente_federado')

    class Meta:
        model = SistemaCultura
        fields = ("id", "ente_federado")


class MunicipioSerializer(hal_serializers.HalModelSerializer):
    ente_federado = serializers.SerializerMethodField()
    governo = serializers.SerializerMethodField()
    conselho = serializers.SerializerMethodField()
    _embedded = serializers.SerializerMethodField(method_name='get_embedded')
    situacao_adesao = serializers.SerializerMethodField()
    data_adesao = serializers.DateField(source='usuario.data_publicacao_acordo')
    self = HalHyperlinkedIdentityField(view_name='api:sistemacultura-detail')

    class Meta:
        model = Municipio
        fields = ('id', 'self', '_embedded', 'ente_federado', 'governo',
                  'conselho', 'situacao_adesao', 'data_adesao')

    def get_conselho(self, obj):

        try:
            conselho = obj.usuario.plano_trabalho.conselho_cultural
            conselheiros = conselho.conselheiro_set.filter(conselho_id=conselho)
        except AttributeError:
            return None

        lista = list(range(len(conselheiros)))

        for i in range(len(conselheiros)):
            while i <= len(conselheiros):
                serializer = ConselheiroSerializer(conselheiros[i])
                lista[i] = serializer.data
                break

        if conselheiros is None:
            return None

        else:
            return ({'conselheiros': lista})

    def get_embedded(self, obj):
        embedded = ({'acoes_plano_trabalho': self.get_acoes_plano_trabalho(obj=obj)})

        return embedded

    def get_acoes_plano_trabalho(self, obj):

        try:
            plano_trabalho = obj.usuario.plano_trabalho
            assert plano_trabalho
        except (Usuario.DoesNotExist, AssertionError):
            return None

        context = {}
        context['request'] = self.context['request']
        serializer = PlanoTrabalhoSerializer(instance=plano_trabalho, context=context)

        return serializer.data

    def get_ente_federado(self, obj):
        localizacao = Localizacao(estado=obj.estado, cidade=obj.cidade,
                cep=obj.cep, bairro=obj.bairro, endereco=obj.endereco, complemento=obj.complemento)
        telefones = Telefones(telefone_um=obj.telefone_um, telefone_dois=obj.telefone_dois,
                telefone_tres=obj.telefone_tres)
        ente_federado = EnteFederado(cnpj_prefeitura=obj.cnpj_prefeitura,localizacao=localizacao,
                endereco_eletronico=obj.endereco_eletronico, telefones=telefones)
        serializer = EnteFederadoSerializer(ente_federado)

        return serializer.data

    def get_governo(self, obj):
        governo = Governo(nome_prefeito=obj.nome_prefeito,
                          email_institucional_prefeito=obj.email_institucional_prefeito,
                          termo_posse_prefeito=obj.termo_posse_prefeito)
        serializer = GovernoSerializer(governo)

        return serializer.data

    def get_situacao_adesao(self, obj):
        try:
            processo = obj.usuario.get_estado_processo_display()
            serializer = {'situacao_adesao': processo}
        except AttributeError:
            serializer = None
        return serializer


""" Classes para estruturar os objetos de adesoes"""


class EnteFederado(object):
    def __init__(self, cnpj_prefeitura, localizacao, endereco_eletronico, telefones):
        self.cnpj_prefeitura = cnpj_prefeitura
        self.localizacao = localizacao
        self.endereco_eletronico = endereco_eletronico
        self.telefones = telefones


class Localizacao(object):
    def __init__(self, estado, cidade, cep, bairro, endereco, complemento):
        self.estado = estado
        self.cidade = cidade
        self.cep = cep
        self.bairro = bairro
        self.endereco = endereco
        self.complemento = complemento


class Telefones(object):
    def __init__(self, telefone_um, telefone_dois, telefone_tres):
        self.telefone_um = telefone_um
        self.telefone_dois = telefone_dois
        self.telefone_tres = telefone_tres


class Governo(object):
    def __init__(self, nome_prefeito, email_institucional_prefeito,
                 termo_posse_prefeito):
        self.nome_prefeito = nome_prefeito
        self.email_institucional_prefeito = email_institucional_prefeito
        self.termo_posse_prefeito = termo_posse_prefeito


"""Serializers das classes de estruturação de adesoes"""


class LocalizacaoSerializer(serializers.Serializer):
    estado = UfSerializer()
    cidade = CidadeSerializer()
    cep = serializers.CharField()
    bairro = serializers.CharField()
    endereco = serializers.CharField()
    complemento = serializers.CharField()


class TelefonesSerializer(serializers.Serializer):
    telefone_um = serializers.CharField()
    telefone_dois = serializers.CharField()
    telefone_tres = serializers.CharField()


class EnteFederadoSerializer(serializers.Serializer):
    cnpj_prefeitura = serializers.CharField()
    localizacao = LocalizacaoSerializer()
    telefones = TelefonesSerializer()
    endereco_eletronico = serializers.CharField()


class GovernoSerializer(serializers.Serializer):
    nome_prefeito = serializers.CharField()
    email_institucional_prefeito = serializers.CharField()
    termo_posse_prefeito = serializers.FileField()
