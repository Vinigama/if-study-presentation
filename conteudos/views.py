from datetime import datetime
import math
from re import T, U
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from django.db import transaction
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.db.models import Count
from django.contrib import messages
import json
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.urls import reverse
from .models import Comentario, Conteudo, Secao, Tecnologia, Tag, Visualizacao, Historico
from .forms import DivulgarTrilhasForm
from requisicoes.models import RequisicaoFormulario
from denuncias.models import HistoricoSinalizacaoConteudo, SinalizacaoComentario, SinalizacaoConteudo, PerfilSilenciado
from usuarios.models import Perfil
from django.db.models import Q
from denuncias import apps, classifier
from utils.email.email import EmailSender
from utils.email_templates.rejeicao_conteudo import default_message as template_rejeicao_conteudo
from utils.email_templates.abandono_conteudo import default_message as template_abandono_conteudo
from utils.certificado.certificate import GeradorCertificado


def trilhas(request):
    """ Informações sobre as trilhas """""

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login')) 

    context = {
        'tecnologias': Tecnologia.ativos.all(), 
        'secoes': Secao.ativos.all(), 
        'etiquetas': Tag.ativos.all(),
    }

    return render(request, 'conteudos/trilhas.html', context)

def em_alta(request):
    """ Lista dos vídeos mais assistidos ultimamente """

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login')) 

    dupes = Visualizacao.objects.values('conteudo').annotate(total=Count('visualizador')).order_by('-total')

    conteudo_id     = [conteudo['conteudo'] for conteudo in dupes]
    em_alta         = Conteudo.ativos.all().in_bulk(conteudo_id)
    sorted_em_alta  = [em_alta[id] for id in conteudo_id if id in em_alta]
    
    context = {
        'conteudos': sorted_em_alta
    }

    return render(request, 'conteudos/em_alta.html', context)


def registrar_trilha(request):
    """" Registrar uma trilha """""

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login')) 

    context = {
        'tecnologias': Tecnologia.ativos.all(), 
        'secoes': Secao.ativos.all(), 
    }

    return render(request, 'conteudos/registrar_conteudo.html', context)

def get_tecnologias(request):
    """ Mensagem assíncrona das seções quando seleciona uma tecnologia """

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login')) 

    tecnologia_id = request.GET.get('id')

    tecnologia = get_object_or_404(Tecnologia, nome=tecnologia_id)

    secao_list = list(tecnologia.secao_set.filter(ativo=True).values())

    return JsonResponse({'data': secao_list})

def post_comentario(request):
    """ Coletar as informações referente ao campo input comentário """

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login')) 

    comentario_valor = request.POST.get('comentario')
    conteudo_id      = request.POST.get('conteudo')

    perfil           = request.user
    conteudo         = Conteudo.objects.get(pk=conteudo_id)

    if not perfil.email_confirmado:
        return JsonResponse({"title": "Conta não ativada", "msg": "Para comentar no conteúdo é necessário ativar a conta. Acesse o menu perfil e clique em verificar email"} ,status=403)

    if PerfilSilenciado.objects.filter(perfil=perfil.id):
        return JsonResponse({"title": "Perfil Silenciado", "msg": "Por motivos de sinalizações. Você não pode comentar no momento"} ,status=403) 

    comentario = Comentario.objects.create(
        comentario  = comentario_valor,
        conteudo    = conteudo,
        criador     = request.user
    )
    comentario.save()    
    return JsonResponse({"comentarioId": comentario.pk, "perfil": perfil.dados().foto.url, "perfil_id": perfil.id}, status=200)

def post_like(request):
    """ Incrementar o like no comentário"""

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login')) 

    comentario_id = request.POST.get('comentario_id')

    if request.user in Comentario.objects.get(id=comentario_id).dislike.all():
        Comentario.objects.get(id=comentario_id).dislike.remove(request.user)

        comentario = Comentario.objects.get(id=comentario_id)

        comentario.like.add(request.user)

        comentario.save()

    elif request.user not in Comentario.objects.get(id=comentario_id).like.all():

        comentario = Comentario.objects.get(id=comentario_id)

        comentario.like.add(request.user)

        comentario.save()

    else:
        Comentario.objects.get(id=comentario_id).like.remove(request.user)
        
    return JsonResponse({"msg": "Criado com sucesso"} ,status=200)

def post_dislike(request):
    """ Incrementar o dislike """

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login')) 

    comentario_id = request.POST.get('comentario_id')

    if request.user in Comentario.objects.get(id=comentario_id).like.all():
        Comentario.objects.get(id=comentario_id).like.remove(request.user)

        comentario = Comentario.objects.get(id=comentario_id)

        comentario.dislike.add(request.user)

        comentario.save()

    elif request.user not in Comentario.objects.get(id=comentario_id).dislike.all():

        comentario = Comentario.objects.get(id=comentario_id)

        comentario.dislike.add(request.user)

        comentario.save()

    else:
        Comentario.objects.get(id=comentario_id).dislike.remove(request.user)

    return JsonResponse({"msg": "Criado com sucesso"} ,status=200)

def post_resposta(request):
    """ Postar resposta em um comentário """
    comentario      = request.POST.get('comentario')
    resposta_id     = request.POST.get('resposta')
    conteudo_id     = request.POST.get('conteudo')

    resposta    = Comentario.objects.get(pk=resposta_id)
    conteudo    = Conteudo.objects.get(pk=conteudo_id)
    perfil      = request.user

    if not perfil.email_confirmado:
        return JsonResponse({"title": "Conta não ativada", "msg": "Para comentar no conteúdo é necessário ativar a conta. Acesse o menu perfil e clique em verificar email"} ,status=403)

    if PerfilSilenciado.objects.filter(perfil=perfil.id):
        return JsonResponse({"title": "Perfil Silenciado", "msg": "Por motivos de sinalizações. Você não pode comentar no momento"} ,status=403) 

    comentario = Comentario.objects.create(
        comentario  = comentario,
        conteudo    = conteudo,
        resposta    = resposta,
        criador     = request.user
    )

    comentario.save()

    return JsonResponse({"comentarioId": comentario.pk, "perfil": perfil.dados().foto.url, "perfil_id": perfil.id}, status=200)

@transaction.atomic
def post_conteudo(request):
    """ Pegar as informações via AJAX """

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login')) 

    if not request.user.email_confirmado:
        return JsonResponse({"title": "Conta não ativada", "msg": "Para postar conteúdo é necessário ativar a conta. Acesse o menu perfil e clique em verificar email"} ,status=403)

    if PerfilSilenciado.objects.filter(perfil=request.user.id):
        return JsonResponse({"title": "Perfil Silenciado", "msg": "Por motivos de sinalizações. Você não pode postar conteúdo no momento"} ,status=403)

    titulo = request.POST.get('titulo')
    descricao = request.POST.get('descricao')
    tipo_conteudo = request.POST.get('tipo_de_conteudo')
    tipo_tecnologia = request.POST.get('tipo_de_tecnologia')
    tipo_secao = request.POST.get('tipo_de_secao')
    tags = request.POST.getlist('tags[]')
    
    carga_horas = abs(int(request.POST.get('carga_horas'))) if request.POST.get('carga_horas') else 0
    carga_minutos = abs(int(request.POST.get('carga_minutos'))) if request.POST.get('carga_minutos') else 0
    carga_segundos = abs(int(request.POST.get('carga_segundos'))) if request.POST.get('carga_segundos') else 0
    
    #arquivos
    thumbnail = request.FILES.get('thumbnail')
    arquivo_conteudo = request.FILES.get('arquivo')

    carga_total = carga_horas*60*60 + carga_minutos*60 + carga_segundos
    if carga_total <= 0:
        return JsonResponse({"msg": "Carga horaria negativa"} ,status=400)

    if Tecnologia.objects.filter(nome=tipo_tecnologia).exists():
        tecnologia = Tecnologia.objects.get(nome=tipo_tecnologia)
    else:
        tecnologia = Tecnologia.objects.create(
            nome = tipo_tecnologia,
        )

    if Secao.objects.filter(nome=tipo_secao, tecnologia__nome=tipo_tecnologia).exists():
        secao = Secao.objects.get(nome=tipo_secao, tecnologia__nome=tipo_tecnologia)
    else:
        secao = Secao.objects.create(
            nome        = tipo_secao,
            tecnologia  = tecnologia,
        )
    tag_list = []
    for tag in tags:
        if Tag.objects.filter(nome=tag).exists():
            tag_list.append(Tag.objects.get(nome=tag))
        else:
            tag_provisoria = Tag.objects.create(
                nome = tag
            )
            tag_list.append(tag_provisoria)
    
    conteudo = Conteudo.objects.create(
        arquivo     = arquivo_conteudo,
        titulo      = titulo,
        thumbnail   = thumbnail,
        descricao   = descricao,
        tipo        = tipo_conteudo,
        secao       = secao,
        criador     = request.user,
        carga       = carga_total,
        # tags        = tag_list,
    )
    conteudo.tags.set(tag_list)
    conteudo.save()

    RequisicaoFormulario.objects.create(
        conteudo_pendente = conteudo,
        tipo_requisicao = 'adicao',
    )   

    return JsonResponse({"msg": "Criado com sucesso"} ,status=200)

@user_passes_test(lambda u: u.is_superuser)
@transaction.atomic
def aprovar_conteudo(request, solicitacao_id):
    """ Aprovar conteúdos pendentes """

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login')) 

    titulo = request.POST.get('titulo')
    descricao = request.POST.get('descricao')
    tipo_conteudo = request.POST.get('tipo_de_conteudo')
    tipo_tecnologia = request.POST.get('tipo_de_tecnologia')
    tipo_secao = request.POST.get('tipo_de_secao')
    tags = request.POST.getlist('tags[]')
    
    carga_horas = abs(int(request.POST.get('carga_horas'))) if request.POST.get('carga_horas') else 0
    carga_minutos = abs(int(request.POST.get('carga_minutos'))) if request.POST.get('carga_minutos') else 0
    carga_segundos = abs(int(request.POST.get('carga_segundos'))) if request.POST.get('carga_segundos') else 0

    #arquivos
    thumbnail = request.FILES.get('thumbnail')
    arquivo_conteudo = request.FILES.get('arquivo')

    carga_total = carga_horas*60*60 + carga_minutos*60 + carga_segundos
    if carga_total <= 0:
        return JsonResponse({"msg": "Carga horaria negativa"} ,status=400)

    solicitacao = get_object_or_404(RequisicaoFormulario, pk = solicitacao_id)
    if Tecnologia.objects.filter(nome=tipo_tecnologia).exists():
        tecnologia = Tecnologia.objects.get(nome=tipo_tecnologia)
    else:
        tecnologia = Tecnologia.objects.create(
            nome = tipo_tecnologia,
        )

    if Secao.objects.filter(nome=tipo_secao, tecnologia__nome=tipo_tecnologia).exists():
        secao = Secao.objects.get(nome=tipo_secao, tecnologia__nome=tipo_tecnologia)
    else:
        secao = Secao.objects.create(
            nome        = tipo_secao,
            tecnologia  = tecnologia,
        )

    solicitacao.conteudo_pendente.titulo = titulo
    solicitacao.conteudo_pendente.descricao = descricao
    solicitacao.conteudo_pendente.tipo = tipo_conteudo
    solicitacao.conteudo_pendente.secao = secao
    solicitacao.conteudo_pendente.carga = carga_total

    if thumbnail:
        solicitacao.conteudo_pendente.thumbnail = thumbnail
    if arquivo_conteudo:
        solicitacao.conteudo_pendente.arquivo = arquivo_conteudo
    
    tag_list = []
    for tag in tags:
        if Tag.objects.filter(nome=tag).exists():
            tag_list.append(Tag.objects.get(nome=tag))
        else:
            tag_provisoria = Tag.objects.create(
                nome = tag
            )
            tag_list.append(tag_provisoria)
    
    solicitacao.conteudo_pendente.tags.set(tag_list)
    solicitacao.save()
    solicitacao.aceita_requisicao()

    return JsonResponse({"msg": "Criado com sucesso"} ,status=200)

@user_passes_test(lambda u: u.is_superuser)
def validar_conteudo(request, solicitacao_id):
    """ Validação do conteúdo """

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login')) 

    solicitacao = get_object_or_404(RequisicaoFormulario, id=solicitacao_id)
    tags = [tag.nome for tag in solicitacao.conteudo_pendente.tags.all()]
    context = {
        'tecnologias':  Tecnologia.ativos.all(),
        'secoes':       Secao.ativos.all(),
        'solicitacao':  solicitacao,
        'tags':         json.dumps(tags),
    }

    return render(request, 'conteudos/validar_conteudo.html', context)

@user_passes_test(lambda u: u.is_superuser)
@transaction.atomic
def aprovar_edicao_conteudo(request, solicitacao_id):
    """ Aprovar a edição de conteúdos pendentes """

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    
    solicitacao = get_object_or_404(RequisicaoFormulario, pk = solicitacao_id)

    titulo = request.POST.get('titulo')
    descricao = request.POST.get('descricao')
    tipo_conteudo = solicitacao.conteudo_atualizar.tipo
    tipo_tecnologia = request.POST.get('tipo_de_tecnologia')
    tipo_secao = request.POST.get('tipo_de_secao')
    tags = request.POST.getlist('tags[]')
    
    #arquivos
    thumbnail = request.FILES.get('thumbnail')
    
    if Tecnologia.objects.filter(nome=tipo_tecnologia).exists():
        tecnologia = Tecnologia.objects.get(nome=tipo_tecnologia)
    else:
        tecnologia = Tecnologia.objects.create(
            nome = tipo_tecnologia,
        )

    if Secao.objects.filter(nome=tipo_secao, tecnologia__nome=tipo_tecnologia).exists():
        secao = Secao.objects.get(nome=tipo_secao, tecnologia__nome=tipo_tecnologia)
    else:
        secao = Secao.objects.create(
            nome        = tipo_secao,
            tecnologia  = tecnologia,
        )

    solicitacao.conteudo_pendente.titulo = titulo
    solicitacao.conteudo_pendente.descricao = descricao
    solicitacao.conteudo_pendente.tipo = tipo_conteudo
    solicitacao.conteudo_pendente.secao = secao

    if thumbnail:
        solicitacao.conteudo_pendente.thumbnail = thumbnail
    
    tag_list = []
    for tag in tags:
        if Tag.objects.filter(nome=tag).exists():
            tag_list.append(Tag.objects.get(nome=tag))
        else:
            tag_provisoria = Tag.objects.create(
                nome = tag
            )
            tag_list.append(tag_provisoria)
    
    solicitacao.conteudo_pendente.tags.set(tag_list)
    solicitacao.save()
    solicitacao.aceita_requisicao()

    if SinalizacaoConteudo.objects.filter(conteudo=solicitacao.conteudo_atualizar.id, notificado=True).exists():
        sinalizacao = SinalizacaoConteudo.objects.get(conteudo=solicitacao.conteudo_atualizar.id, notificado=True)
        sinalizacao.delete()
        historico_sinalizacao = HistoricoSinalizacaoConteudo.objects.get(conteudo=solicitacao.conteudo_atualizar.id, status="aguardando_edicao")
        historico_sinalizacao.status = "edicao_concluida"
        historico_sinalizacao.save()

    return JsonResponse({"msg": "Criado com sucesso"} ,status=200)

@user_passes_test(lambda u: u.is_superuser)
def validar_edicao_conteudo(request, solicitacao_id):
    """ Validação a edição do conteúdo """

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login')) 

    solicitacao = get_object_or_404(RequisicaoFormulario, id=solicitacao_id)
    tags = [tag.nome for tag in solicitacao.conteudo_pendente.tags.all()]
    context = {
        'tecnologias':  Tecnologia.ativos.all(),
        'secoes':       Secao.ativos.all(),
        'solicitacao':  solicitacao,
        'tags':         json.dumps(tags),
    }

    return render(request, 'conteudos/validar_edicao_conteudo.html', context)


@user_passes_test(lambda u: u.is_superuser)
def verificar_baixa_conteudo(request):
    """ Verificar da baixa do conteúdo """

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login')) 

    return render(request, 'conteudos/verificacao_conteudo.html')

@user_passes_test(lambda u: u.is_superuser)
def validar_baixa_conteudo(request, conteudo_id):
    """ Validação da baixa do conteúdo """

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login')) 

    conteudo = get_object_or_404(Conteudo, id=conteudo_id, ativo=True)
    tags = [tag.nome for tag in conteudo.tags.all()]
    context = {
        'tecnologias':  Tecnologia.ativos.all(),
        'secoes':       Secao.ativos.all(),
        'conteudo':     conteudo,
        'tags':         json.dumps(tags),
    }

    return render(request, 'conteudos/validar_baixa_conteudo.html', context)

@user_passes_test(lambda u: u.is_superuser)
def executar_baixa_conteudo(request, conteudo_id):
    """ Execução da baixa do conteúdo """

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login')) 

    conteudo = get_object_or_404(Conteudo, id=conteudo_id)
    conteudo.baixa = True
    conteudo.data_baixa = datetime.now()
    conteudo.save()

    return JsonResponse({"msg": "Baixa executada com sucesso"} ,status=200)

@user_passes_test(lambda u: u.is_superuser)
@transaction.atomic
def aprovar_exclusao_conteudo(request, solicitacao_id):
    """ Aprovar a exclusão de conteúdos pendentes """

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    
    solicitacao = get_object_or_404(RequisicaoFormulario, pk = solicitacao_id)
    solicitacao.aceita_requisicao()

    return JsonResponse({"msg": "Apagado com sucesso"} ,status=200)

@user_passes_test(lambda u: u.is_superuser)
@transaction.atomic
def rejeitar_solicitacao_conteudo(request, solicitacao_id):
    """ Rejeitar solicitação do usuário relacionada ao conteúdo (Inclusão, Exclusão e Edição) """

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    
    motivo = request.POST.get('motivo_rejeicao')

    solicitacao = get_object_or_404(RequisicaoFormulario, pk = solicitacao_id)

    mensagem = dict()
    mensagem["titulo_conteudo"] = solicitacao.conteudo_pendente.titulo if solicitacao.tipo_requisicao != "atualizacao" else solicitacao.conteudo_atualizar.titulo
    mensagem["tipo_solicitacao"] = solicitacao.tipo_requisicao if solicitacao.tipo_requisicao else "Não informado"
    mensagem["data_solicitacao"] = solicitacao.data_requisicao if solicitacao.data_requisicao else "Não informado" 
    mensagem["motivo_rejeicao"] = motivo if motivo else "Não informado"

    autor = solicitacao.conteudo_pendente.criador

    solicitacao.rejeita_requisicao()

    # Mensagem de retorno ao tutor
    EmailSender(
        "IF-Study ADMs",
        [autor.email],
        f"Rejeição de conteúdo - {mensagem['titulo_conteudo']}",
        template_rejeicao_conteudo.format(**mensagem)
    ).enviar()

    return JsonResponse({"msg": "conteudo rejeitado com sucesso"} ,status=200)

@user_passes_test(lambda u: u.is_superuser)
def validar_exclusao_conteudo(request, solicitacao_id):
    """ Validação a edição do conteúdo """

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login')) 

    solicitacao = get_object_or_404(RequisicaoFormulario, id=solicitacao_id)
    tags = [tag.nome for tag in solicitacao.conteudo_pendente.tags.all()]
    context = {
        'tecnologias':  Tecnologia.ativos.all(),
        'secoes':       Secao.ativos.all(),
        'solicitacao':  solicitacao,
        'tags':         json.dumps(tags),
    }

    return render(request, 'conteudos/validar_exclusao_conteudo.html', context)

def editar_conteudo(request, conteudo_id):
    """ Solicitação de edição do conteúdo """

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    try:
        conteudo = Conteudo.ativos.get(pk=conteudo_id)
    except:
        return HttpResponseRedirect(reverse('login'))
    if request.user.id != conteudo.criador.id:
        return HttpResponseRedirect(reverse('login'))

    # Verifica se solicitação vinculada ao conteúdo já existe
    presente_em_pendente = Q(conteudo_pendente=conteudo)
    presente_em_atualizar = Q(conteudo_atualizar=conteudo)
    solicitacao_existe = RequisicaoFormulario.objects\
        .filter(presente_em_pendente | presente_em_atualizar).exists()

    tags = [tag.nome for tag in conteudo.tags.all()]
    context = {
        'tecnologias':  Tecnologia.ativos.all(),
        'secoes':       Secao.ativos.all(),
        'conteudo':     conteudo,
        'tags':         json.dumps(tags),
        'solicitacao_existe': solicitacao_existe
    }

    return render(request, 'conteudos/editar_conteudo.html', context)

@transaction.atomic
def gerar_solicitacao_edicao(request, conteudo_id):
    """ Pegar as informações via AJAX """

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login')) 

    conteudo_original = get_object_or_404(Conteudo, id=conteudo_id)
    if request.user.id != conteudo_original.criador.id and not request.user.is_superuser:
        return JsonResponse({"msg": "usuário não possui permissão"} ,status=200)

    titulo = request.POST.get('titulo')
    descricao = request.POST.get('descricao')
    tipo_tecnologia = request.POST.get('tipo_de_tecnologia')
    tipo_secao = request.POST.get('tipo_de_secao')
    tags = request.POST.getlist('tags[]')

    tipo_conteudo = conteudo_original.tipo
    
    #arquivos
    thumbnail = request.FILES.get('thumbnail')
    arquivo_conteudo = request.FILES.get('arquivo')


    if Tecnologia.objects.filter(nome=tipo_tecnologia).exists():
        tecnologia = Tecnologia.objects.get(nome=tipo_tecnologia)
    else:
        tecnologia = Tecnologia.objects.create(
            nome = tipo_tecnologia,
        )

    if Secao.objects.filter(nome=tipo_secao, tecnologia__nome=tipo_tecnologia).exists():
        secao = Secao.objects.get(nome=tipo_secao, tecnologia__nome=tipo_tecnologia)
    else:
        secao = Secao.objects.create(
            nome        = tipo_secao,
            tecnologia  = tecnologia,
        )
    tag_list = []
    for tag in tags:
        if Tag.objects.filter(nome=tag).exists():
            tag_list.append(Tag.objects.get(nome=tag))
        else:
            tag_provisoria = Tag.objects.create(
                nome = tag
            )
            tag_list.append(tag_provisoria)
    
    conteudo = Conteudo.objects.create(
        arquivo     = arquivo_conteudo,
        titulo      = titulo,
        thumbnail   = thumbnail,
        descricao   = descricao,
        tipo        = tipo_conteudo,
        secao       = secao,
        criador     = request.user,
        # tags        = tag_list,
    )
    conteudo.tags.set(tag_list)
    conteudo.save()

    RequisicaoFormulario.objects.create(
        conteudo_pendente = conteudo,
        conteudo_atualizar = conteudo_original,
        tipo_requisicao = 'atualizacao',
    )   

    return JsonResponse({"msg": "Criado com sucesso"} ,status=200)

@transaction.atomic
def gerar_solicitacao_exclusao(request, conteudo_id):
    """ Pegar as informações via AJAX """

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login')) 

    conteudo_original = get_object_or_404(Conteudo, id=conteudo_id)
    if request.user.id != conteudo_original.criador.id and not request.user.is_superuser:
        return JsonResponse({"msg": "usuário não possui permissão"} ,status=200)
    
    # Verifica se solicitação vinculada ao conteúdo já existe
    presente_em_pendente = Q(conteudo_pendente=conteudo_original)
    solicitacao_existe = RequisicaoFormulario.objects\
        .filter(presente_em_pendente, tipo_requisicao="exclusao").exists()
    if solicitacao_existe:
        return JsonResponse({"msg": "Conteúdo já cadastrado"} ,status=403) 

    RequisicaoFormulario.objects.create(
        conteudo_pendente = conteudo_original,
        tipo_requisicao = 'exclusao',
    )   

    return JsonResponse({"msg": "Criado com sucesso"} ,status=200)

def secoes(request, tecnologia_id):
    """ Exibição das seções """    

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login')) 

    context = {
        'tecnologia': Tecnologia.objects.get(ativo=True, id=tecnologia_id),
    }

    return render(request, 'conteudos/secoes.html', context)

def conteudo(request, secao_id):
    """ Exibição do conteúdo """

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login')) 

    conteudo = Conteudo.objects.get(id=secao_id, ativo=True)

    post_visualizacao_conteudo(request, conteudo)
    post_historico_conteudo(request, conteudo)

    context = {
        'conteudo': Conteudo.objects.get(ativo=True, id=secao_id),
        'comentarios': Comentario.objects.filter(conteudo=secao_id, resposta=None).order_by('comentario'),
        'comentario_id': Comentario.objects.all().count(),
        'quantidade_comentarios': Comentario.objects.filter(conteudo=secao_id, resposta=None).count(),
        'conteudo_like': '<i class="fas fa-thumbs-up fa-lg text-dark" title="Gostei" value="likado"></i>',
        'conteudo_dislike': '<i class="fas fa-thumbs-down fa-lg text-dark" title="Não gostei" value="dislikado"></i>'
    }

    if request.user not in conteudo.like.all():
        context['conteudo_like'] = '<i class="far fa-thumbs-up fa-lg text-dark" title="Gostei"></i>'

    if request.user not in conteudo.dislike.all():
        context['conteudo_dislike'] = '<i class="far fa-thumbs-down fa-lg text-dark" title="Não gostei"></i>'


    return render(request, 'conteudos/conteudo.html', context)

def gerar_certificado(request, secao_id):
    """ Gera certificado (png) para o conteúdo postado """

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login')) 

    conteudo = get_object_or_404(Conteudo, id=secao_id)
    if request.user.id != conteudo.criador.id and not request.user.is_superuser:
        return HttpResponseRedirect(reverse('login')) 

    autor = conteudo.criador

    segundos = math.floor(int(conteudo.carga))
    horas = math.floor(segundos/3600)
    sobra_horas = segundos % 3600
    minutos = math.floor(sobra_horas/60)
    segundos = sobra_horas % 60

    data_conclusao = conteudo.data.strftime("%d/%m/%Y")

    gerador = GeradorCertificado(f"{autor.first_name} {autor.last_name}", conteudo.titulo, str(horas), str(minutos), data_conclusao, str(conteudo.id))
    try:
        imagem = gerador.to_bytes()
        response = HttpResponse(imagem.getbuffer(), content_type="image/png")
        response['Content-Length'] = imagem.getbuffer().nbytes
        response['Content-Disposition'] = "attachment; filename=%s" % f"{'_'.join(conteudo.titulo.split(' '))}_cert.png".lower()
        imagem.close()
        return response
    except IOError as exc:
        print(exc)
        return HttpResponse("Couldn't process request")


def historico_assistido(request):
    """ Exibição do histórico de conteúdos visualizados """

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login')) 

    historicos_id = Historico.objects.filter(visualizador=request.user).order_by('visualizador').values_list('conteudo', flat=True)
    conteudos_id = Conteudo.ativos.all().in_bulk(historicos_id)
    conteudos = [conteudos_id[id] for id in historicos_id if id in conteudos_id]

    return render(request, 'conteudos/historico.html', context={'conteudos': conteudos})


def conteudo_postado(request):
    """ Exibição dos conteúdos postados """

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login')) 

    conteudos = Conteudo.ativos.filter(criador=request.user).order_by('-data')

    context = {
        "conteudos": conteudos,
    }

    return render(request, 'conteudos/video_postado.html', context)


def post_delete_historico(request, usuario_id):
    """ Deleta o histórico dos conteúdos assistidos """

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login')) 

    if request.user.id != usuario_id:
        return JsonResponse({"msg": "usuário não possui permissão"} ,status=200)

    if not Historico.objects.filter(visualizador=request.user).exists():
        return JsonResponse({"mensagem": "Não há conteúdos no seu histórico"}, status=403) 

    Historico.visualizador.through.objects.filter(perfil=request.user).delete()
    historico = Historico.objects.filter(visualizador=None)

    if historico.exists():
        historico.delete()

    messages.success(request, 'Histórico removido com sucesso.')
    return JsonResponse({"msg": "Histórico deletado com sucesso"} ,status=200)
    

def post_visualizacao_conteudo(request, conteudo):
    """ Atribuir o usuário no campo visualizacao """

    if request.user not in conteudo.visualizacao.all():
        conteudo.visualizacao.add(request.user)
        conteudo.save()
    
    if not Visualizacao.objects.filter(conteudo=conteudo.id).exists():
        conteudo = get_object_or_404(Conteudo, id=conteudo.id)
        visualizacao = Visualizacao.objects.create(
            conteudo=conteudo
        )
        visualizacao.visualizador.add(request.user)
        visualizacao.save()
    else:
        visualizacao = Visualizacao.objects.get(conteudo=conteudo.id)
        if request.user not in visualizacao.visualizador.all():
            visualizacao.visualizador.add(request.user)
            visualizacao.save()
            
    return JsonResponse({"msg": "Criado com sucesso"} ,status=200)


def post_historico_conteudo(request, conteudo):
    """ Atribuir um histórico para o usuário """

    conteudo = Conteudo.ativos.get(id=conteudo.pk)
    historico = Historico.objects.filter(conteudo=conteudo.id)
    
    if historico.exists():
            historico_usuario = Historico.objects.get(conteudo=conteudo)
            if request.user in historico_usuario.visualizador.all():
                return JsonResponse({"msg": "Usuário já faz parte desse histórico"} ,status=403) 
            else:
                historico_usuario.visualizador.add(request.user)
    else:
        historico = Historico.objects.create(
            conteudo      = conteudo,
        )
        historico.visualizador.add(request.user)
        historico.save()        
    return JsonResponse({"msg": "Criado com sucesso"} ,status=200)


def post_like_conteudo(request):
    """ Incrementar o like no conteúdo"""

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login')) 

    conteudo_id = request.POST.get('conteudo_id')

    if request.user in Conteudo.ativos.get(id=conteudo_id).dislike.all():
        Conteudo.objects.get(id=conteudo_id).dislike.remove(request.user)
        conteudo = Conteudo.objects.get(id=conteudo_id)
        conteudo.like.add(request.user)
        conteudo.save()

    elif request.user not in Conteudo.objects.get(id=conteudo_id).like.all():
        conteudo = Conteudo.objects.get(id=conteudo_id)
        conteudo.like.add(request.user)
        conteudo.save()

    else:
        Conteudo.objects.get(id=conteudo_id).like.remove(request.user)
        
    return JsonResponse({"msg": "Criado com sucesso"} ,status=200)

def post_dislike_conteudo(request):
    """ Incrementar o dislike """

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login')) 

    conteudo_id = request.POST.get('conteudo_id')

    if request.user in Conteudo.objects.get(id=conteudo_id).like.all():
        Conteudo.objects.get(id=conteudo_id).like.remove(request.user)
        conteudo = Conteudo.objects.get(id=conteudo_id)
        conteudo.dislike.add(request.user)
        conteudo.save()

    elif request.user not in Conteudo.objects.get(id=conteudo_id).dislike.all():
        conteudo = Conteudo.objects.get(id=conteudo_id)
        conteudo.dislike.add(request.user)
        conteudo.save()

    else:
        Conteudo.objects.get(id=conteudo_id).dislike.remove(request.user)

    return JsonResponse({"msg": "Criado com sucesso"} ,status=200)


@user_passes_test(lambda u: u.is_superuser)
def post_delete_comentario(request):
    """ Função para deletar comentário """

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login')) 

    comentario_id = request.POST.get('id')
    comentario = Comentario.objects.get(pk=comentario_id)

    if request.user == comentario.criador:
        comentario.delete()

    return JsonResponse({"msg": "Criado com sucesso"} ,status=200)

def is_owner(request, conteudo_id):
    """ Requisição que retorna True caso o requisitante seja dono do conteúdo e False caso não seja """
    conteudo = Conteudo.ativos.get(id=conteudo_id)
    return JsonResponse({"is_owner": conteudo.criador.id == request.user.id} ,status=200)


@user_passes_test(lambda u: u.is_superuser)
@transaction.atomic
def gerar_sinalizacao_comentario(request, comentario_id):
    """ Pegar as informações via AJAX """

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login')) 

    comentario = get_object_or_404(Comentario, id=comentario_id)
    if not request.user.id != comentario.criador.id:
        return JsonResponse({"msg": "usuário não possui permissão"} ,status=200)
    
    sinalizacao = SinalizacaoComentario.objects.filter(comentario=comentario.id)
    comentario  = Comentario.objects.get(pk=comentario.id)
 
    if sinalizacao.exists():
        sinalizacao = SinalizacaoComentario.objects.get(comentario=comentario.id)
        if request.user in sinalizacao.usuario.all():
            return JsonResponse({"msg": "Comentario já sinalizado"} ,status=403) 
        else:
            sinalizacao.usuario.add(request.user)
    else:
        sinalizacao = SinalizacaoComentario.objects.create(
            tipo_sinalizacao = 'rude',
            comentario       = comentario,
        )
        sinalizacao.usuario.add(request.user)
        sinalizacao.save()

    tagger        = apps.DenunciasConfig.tagger
    model         = apps.DenunciasConfig.model
    classificador = classifier.Classifier(str(comentario), tagger, model).classify_model()

    media_sinalizacao = ((sinalizacao.usuario.all().count() * 100) / comentario.conteudo.visualizacao.all().count())
    media_dislike = ((comentario.dislike.all().count() * 100) / comentario.conteudo.visualizacao.all().count())

    pesos = {
        'sinalizacao': 6,
        'classificador': 3,
        'dislike': 1
    }

    classificacao = 0
    if classificador == 'Negative':
        classificacao = 100

    media_sentimento_negativo = ((
        classificacao * pesos['classificador']) + 
        (media_sinalizacao * pesos['sinalizacao']) + 
        (media_dislike * pesos['dislike'])) / 100
        
    if media_sentimento_negativo >= 3:
        sinalizacao.classificador = 'Negative'

    sinalizacao.save()
    return JsonResponse({"msg": "Criado com sucesso"} ,status=200)

@transaction.atomic
def gerar_sinalizacao_conteudo(request, conteudo_id):
    """ Pegar as informações via AJAX """

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))   

    sinalizacao = SinalizacaoConteudo.objects.filter(conteudo=conteudo_id)
    conteudo = Conteudo.ativos.get(id=conteudo_id)
    opcao = request.POST['opcao']

    atributos = [
                    'sinalizacoes_conteudo', 'sinalizacoes_titulo', 'sinalizacoes_descricao',
                    'sinalizacoes_tecnologia', 'sinalizacoes_secao'
                ]

    if opcao not in atributos:
        return JsonResponse(status=403, data={"msg": "A opção que você escolheu é inválida."})

    if sinalizacao.exists():
        sinalizacao = SinalizacaoConteudo.objects.get(conteudo=conteudo_id)
        if SinalizacaoConteudo.objects.filter(Q(sinalizacoes_conteudo=request.user)| Q(sinalizacoes_titulo=request.user)
                                                | Q(sinalizacoes_descricao=request.user)|Q(sinalizacoes_tecnologia=request.user)
                                                | Q(sinalizacoes_secao=request.user),
                                                conteudo=conteudo_id):
                                                return JsonResponse({"msg": "Conteúdo já sinalizado"} ,status=403) 
        else:
            getattr(sinalizacao, opcao).add(request.user)

    else:
        sinalizacao = SinalizacaoConteudo.objects.create(
            conteudo = conteudo,
        )
        getattr(sinalizacao, opcao).add(request.user)

    if sinalizacao.classificador == '':
        total_sinalizacao = (
                            SinalizacaoConteudo.objects.filter(conteudo=conteudo_id)
                            .annotate(
                                total=Count("sinalizacoes_conteudo", distinct=True)
                                + Count("sinalizacoes_titulo", distinct=True)
                                + Count("sinalizacoes_descricao", distinct=True)
                                + Count("sinalizacoes_tecnologia", distinct=True)
                                + Count("sinalizacoes_secao", distinct=True)
                            )
                            .values("total"))[0]['total']

        porcentagem_sinalizacao = (total_sinalizacao * 100) / conteudo.visualizacao.count()
        porcentagem_dislike     = (conteudo.dislike.count() * 100) / total_sinalizacao

        if porcentagem_sinalizacao > 40 and porcentagem_dislike > 10:
            sinalizacao.classificador = 'Negative'
            sinalizacao.save()

    return JsonResponse({"msg": "Criado com sucesso"} ,status=200)

@user_passes_test(lambda u: u.is_superuser)
def divulgar_trilhas(request):
    form = DivulgarTrilhasForm()
    tecnologias = Tecnologia.ativos.all()
    secoes = Secao.ativos.all()
    context = {
        "quill_form": form,
        "tecnologias": tecnologias,
        "secoes": secoes,
    }
    return render(request, 'conteudos/divulgar_trilhas.html', context)

@user_passes_test(lambda u: u.is_superuser)
def divulgar_trilhas_postar(request):
    mensagem = json.loads(request.POST['body'])['html']
    assunto = request.POST.get("assunto")
    tecnologia = request.POST.get("tecnologia")
    secao = request.POST.get("secao")
    tecnologia_obj = Tecnologia.objects.get(nome=tecnologia)
    link = request.build_absolute_uri(reverse('secoes', args=[tecnologia_obj.id]))
    emails = list(Perfil.objects.filter(is_superuser=False, is_admin=False, is_staff=False, is_active=True, is_superadmin=False).values_list("email", flat=True))
    
    if secao:
        secao_mensagem = f"<p>Seção: {secao}</p>"
    else:
        secao_mensagem = ""

    EmailSender(
        "IF-Study ADMs",
        emails,
        assunto,
        f"<html><body>{mensagem}{secao_mensagem}<a href=\"{link}\">Visite a página</a></body></html>"
    ).enviar()
    messages.success(request, f'Mensagem enviada a {len(emails)} usuário(s).')
    return HttpResponseRedirect(reverse('divulgar_trilhas'))


def filtro(request):
    """ Filtrar conteúdos de acordo com os campos correspondentes """

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))  

    titulo          = request.GET.get('titulo', False)    
    tipo_tecnologia = request.GET.get('tipo_de_tecnologia', False)
    tipo_secao      = request.GET.get('tipo_de_secao', False)
    tags            = request.GET.getlist('tags')

    conteudos = Conteudo.objects.filter(
                    titulo__contains                    = titulo,
                    secao__nome__contains               = tipo_secao,
                    secao__tecnologia__nome__contains   = tipo_tecnologia,
                    tags__nome__in                      = tags,
                )

    context = {
        'conteudos': conteudos,
        'tecnologias': Tecnologia.ativos.all(), 
        'secoes': Secao.ativos.all(), 
        'etiquetas': Tag.ativos.all(),
    }

    if not conteudos:
        return render(request, 'conteudos/filtro.html', context)
    return render(request, 'conteudos/filtro.html', context)
    
@user_passes_test(lambda u: u.is_superuser)
def notificar_usuarios_abandono(request):
    usuarios_ativos = Perfil.objects.filter(is_active=True)
    emails = list()
    for usuario in usuarios_ativos:
        if usuario.has_abandoned():
            emails.append(usuario.email)
    print(f"Notificados {len(emails)} emails.")
    if emails:
        EmailSender(
            "IF-Study ADMs",
            emails,
            f"Volte a usar o IF-Study",
            template_abandono_conteudo
        ).enviar()  
    return HttpResponseRedirect(reverse('login'))
