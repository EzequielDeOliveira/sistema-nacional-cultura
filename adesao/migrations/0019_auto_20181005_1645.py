# Generated by Django 2.0.8 on 2018-10-05 19:45

from django.db import migrations
from adesao.models import SistemaCultura, Municipio, EnteFederado, Secretario, Funcionario
from adesao.models import Gestor, Sede
from gestao.models import Diligencia, DiligenciaSimples
from planotrabalho.models import Componente
from django.core.exceptions import ObjectDoesNotExist


def cria_sistema_cultura(apps, schema_editor):

    erros = []

    for municipio in Municipio.objects.all():
        sistema_cultura = SistemaCultura()
        sistema_cultura.gestor = Gestor.objects.create(
                cpf=municipio.cpf_prefeito,
                rg=municipio.rg_prefeito,
                orgao_expeditor_rg=municipio.orgao_expeditor_rg,
                estado_expeditor=municipio.estado_expeditor,
                nome=municipio.nome_prefeito,
                telefone_um=municipio.telefone_um,
                telefone_dois=municipio.telefone_dois,
                telefone_tres=municipio.telefone_tres,
                email_institucional=municipio.email_institucional_prefeito,
                tipo_funcionario=3,
                termo_posse=municipio.termo_posse_prefeito,
                rg_copia=municipio.rg_copia_prefeito,
                cpf_copia=municipio.cpf_copia_prefeito
                )

        sistema_cultura.sede = Sede.objects.create(
                localizacao=municipio.localizacao,
                cnpj=municipio.cnpj_prefeitura,
                endereco=municipio.endereco,
                complemento=municipio.complemento,
                cep=municipio.cep,
                bairro=municipio.bairro,
                telefone_um=municipio.telefone_um,
                telefone_dois=municipio.telefone_dois,
                telefone_tres=municipio.telefone_tres,
                endereco_eletronico=municipio.endereco_eletronico
                )

        if municipio.cidade is None:
            try:
                sistema_cultura.ente_federado = EnteFederado.objects.get(cod_ibge=municipio.estado.codigo_ibge)
            except EnteFederado.DoesNotExist:
                ente = EnteFederado.objects.filter(nome__icontains=municipio.estado.nome_uf)
                if not ente:
                    print(f"Erro ao procurar UF {municipio.estado.nome_uf} - {municipio.estado.codigo_ibge}\n")
                    erros.append(municipio.estado.codigo_ibge)
                    pass
                sistema_cultura.ente_federado = ente[0]
        else:
            try:
                sistema_cultura.ente_federado = EnteFederado.objects.get(cod_ibge=municipio.cidade.codigo_ibge)
            except EnteFederado.DoesNotExist:
                ente = EnteFederado.objects.filter(cod_ibge__contains=municipio.cidade.codigo_ibge)
                if not ente:
                    print(f"Erro ao procurar Municipio {municipio.cidade.nome_municipio} - {municipio.cidade.codigo_ibge}\n")
                    erros.append(municipio.estado.codigo_ibge)
                    pass
                sistema_cultura.ente_federado = ente[0]

        componentes_antigos = ('criacao_sistema', 'orgao_gestor', 'fundo_cultura', 'conselho_cultural', 'plano_cultura')
        componentes_novos = ('legislacao', 'orgao_gestor', 'fundo_cultura', 'conselho', 'plano')

        sistema_cultura.numero_processo = municipio.numero_processo

        try:
            sistema_cultura.cadastrador = municipio.usuario
            sistema_cultura.estado_processo = municipio.usuario.estado_processo
            sistema_cultura.data_publicacao_acordo = municipio.usuario.data_publicacao_acordo
            sistema_cultura.link_publicacao_acordo = municipio.usuario.link_publicacao_acordo
            sistema_cultura.processo_sei = municipio.usuario.processo_sei

            if municipio.usuario.plano_trabalho:
                diligencia = municipio.usuario.plano_trabalho.diligencias.last()

                if diligencia:
                    sistema_cultura.diligencia = DiligenciaSimples.objects.create(
                            texto_diligencia=diligencia.texto_diligencia,
                            classificacao_arquivo=diligencia.classificacao_arquivo,
                            usuario=diligencia.usuario)
                    sistema_cultura.diligencia.save()

            for nome_componente_antigo, nome_componente_novo in zip(componentes_antigos, componentes_novos):
                if municipio.usuario.plano_trabalho:
                    componente_antigo = getattr(municipio.usuario.plano_trabalho, nome_componente_antigo)
                    if componente_antigo:
                        setattr(sistema_cultura, nome_componente_novo, Componente.objects.create())
                        componente_novo = getattr(sistema_cultura, nome_componente_novo)
                        componente_novo.tipo = componentes_novos.index(nome_componente_novo)
                        componente_novo.arquivo = componente_antigo.arquivo
                        componente_novo.situacao = componente_antigo.situacao.id
                        componente_novo.data_envio = componente_antigo.data_envio

                        diligencia = componente_antigo.diligencias.last()
                        if diligencia:
                            componente_novo.diligencia = DiligenciaSimples.objects.create(
                                    texto_diligencia=diligencia.texto_diligencia,
                                    classificacao_arquivo=diligencia.classificacao_arquivo,
                                    usuario=diligencia.usuario)
                            componente_novo.save()

            secretario = municipio.usuario.secretario
            if secretario:
                sistema_cultura.secretario = Funcionario.objects.create(cpf=secretario.cpf_secretario,
                        rg=secretario.rg_secretario, orgao_expeditor_rg=secretario.orgao_expeditor_rg,
                        estado_expeditor=secretario.estado_expeditor, nome=secretario.nome_secretario,
                        cargo=secretario.cargo_secretario, instituicao=secretario.instituicao_secretario,
                        telefone_um=secretario.telefone_um, telefone_dois=secretario.telefone_dois,
                        telefone_tres=secretario.telefone_tres,
                        email_institucional=secretario.email_institucional_secretario,
                        tipo_funcionario=0)

                responsavel = municipio.usuario.responsavel
            if responsavel:
                sistema_cultura.responsavel = Funcionario.objects.create(cpf=responsavel.cpf_responsavel,
                        rg=responsavel.rg_responsavel, orgao_expeditor_rg=responsavel.orgao_expeditor_rg,
                        estado_expeditor=responsavel.estado_expeditor, nome=responsavel.nome_responsavel,
                        cargo=responsavel.cargo_responsavel, instituicao=responsavel.instituicao_responsavel,
                        telefone_um=responsavel.telefone_um, telefone_dois=responsavel.telefone_dois,
                        telefone_tres=responsavel.telefone_tres,
                        email_institucional=responsavel.email_institucional_responsavel,
                        tipo_funcionario=1)

        except ObjectDoesNotExist:
            pass

        sistema_cultura.save()


class Migration(migrations.Migration):

    dependencies = [
            ('planotrabalho', '0007_componente_diligencia'),
            ('gestao', '0006_remove_diligenciasimples_tipo_diligencia'),
            ('adesao', '0020_auto_20181008_1610'),
            ]

    operations = [
            migrations.RunPython(cria_sistema_cultura),
            ]