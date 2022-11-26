import dis
from django.shortcuts import get_object_or_404, render
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.core.paginator import Paginator
from conteudos.models import Comentario
from django.db.models import Count
from django.db.models import F
from conteudos.views import conteudo
import denuncias.models as denuncias
from utils.email.email import EmailSender
from usuarios.models import Perfil
from conteudos.models import Conteudo
from utils.email_templates.notificacao_edicao import default_message as template_notificacao_conteudo
from utils.email_templates.notificacao_perfil import default_message as template_notificacao_perfil
from django.db.models import Q

@user_passes_test(lambda u: u.is_superuser)
def sinalizacao_comentario(request):
    """Página que mostra as sinalizações dos comentários"""

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login')) 

    sinalizacao = denuncias.SinalizacaoComentario.objects.filter(classificador='Negative').first()

    context = {
        'sinalizacao': sinalizacao
    }    

    return render(request, 'denuncias/sinalizacoes_comentarios.html', context)

@user_passes_test(lambda u: u.is_superuser)
def apurar_comentario(request, sinalizacao_id):
    """Página que mostra a denúncia do usuário"""

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))   

    sinalizacao = get_object_or_404(denuncias.SinalizacaoComentario, id=sinalizacao_id)
    opcao       = request.POST['opcao']
    
    if request.method == "POST":
        comentario = Comentario.objects.get(id=sinalizacao.comentario.id)
        if opcao == 'remover':
            comentario.delete()
            messages.success(request, 'Comentário removido com sucesso.')
        else:
            sinalizacao.delete()
            messages.success(request, 'Comentário alterado para ok com sucesso.')

    perfil      = Perfil.objects.get(id=comentario.criador.id)

    denuncias.HistoricoSinalizacaoComentario.objects.create(
        usuario     = request.user,
        comentario  = sinalizacao.comentario,
        acao        = opcao,
        autor       = perfil
    )

    return HttpResponseRedirect("/denuncias/comentarios/")


def historico_sinalizacao_comentario(request):
    sinalizacao = denuncias.HistoricoSinalizacaoComentario.objects.all().order_by('-data')

    paginator = Paginator(sinalizacao, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'sinalizacoes': page_obj
    }

    return render(request, 'denuncias/historico_sinalizacao_comentario.html', context)


@user_passes_test(lambda u: u.is_superuser)
def sinalizacao_conteudo(request):
    """Página que mostra as sinalizações dos conteúdos"""

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))    

    conteudo_sinalizado = denuncias.SinalizacaoConteudo.objects.filter(notificado=False, classificador='Negative').first()

    context = {
        'conteudo_sinalizado': conteudo_sinalizado,
    }

    if conteudo_sinalizado is not None:
        contagem    =  denuncias.SinalizacaoConteudo.objects.annotate(
                            conteudo_count=Count("sinalizacoes_conteudo", distinct=True),
                            titulo_count=Count("sinalizacoes_titulo", distinct=True),
                            descricao_count=Count("sinalizacoes_descricao", distinct=True),
                            tecnologia_count=Count("sinalizacoes_tecnologia", distinct=True),
                            secao_count=Count("sinalizacoes_secao", distinct=True)
                        ).values(
                            "conteudo_count",
                            "titulo_count",
                            "descricao_count",
                            "tecnologia_count",
                            "secao_count",
                        ).get(
                            id=conteudo_sinalizado.id
                        )

        lista_traducao = ({'conteudo_count': 'Conteúdo', 
                'titulo_count': 'Título',
                'descricao_count': 'Descrição',
                'tecnologia_count': 'Tecnologia',
                'secao_count': 'Seção'
            })

        contagem = dict((lista_traducao[key], value) for (key, value) in contagem.items())
        contagem = {k:v for (k,v) in sorted(contagem.items(),key=lambda item: item[1], reverse=True) if v > 0}
        context['contagem'] = contagem
        
    return render(request, 'denuncias/sinalizacoes_conteudos.html', context)

@user_passes_test(lambda u: u.is_superuser)
def apurar_conteudo(request, sinalizacao_id):
    """Apuração de conteúdo"""

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))    

    sinalizacao     = get_object_or_404(denuncias.SinalizacaoConteudo, id=sinalizacao_id)
    opcao           = request.POST['opcao']

    if Conteudo.objects.filter(id=sinalizacao.conteudo.id):
        conteudo = Conteudo.objects.get(id=sinalizacao.conteudo.id)
        if opcao == 'aguardando_edicao':
            notificacao = request.POST['input-textarea']
            if len(notificacao) <= 0:
                messages.error(request, 'Campo de notificação está vázio')
                return JsonResponse({"msg": "Campo de notificação está vázio"} ,status=403) 

            sinalizacao.notificado = True
            sinalizacao.save()

            mensagem = dict()
            mensagem["titulo_conteudo"] = sinalizacao.conteudo.titulo
            mensagem["notificacao"]     = notificacao

            # Mensagem de retorno ao tutor
            EmailSender(
                "IF-Study ADMs",
                [sinalizacao.conteudo.criador.email],
                f"Conteúdo Sinalizado - {mensagem['titulo_conteudo']}",
                template_notificacao_conteudo.format(**mensagem)
            ).enviar()
            messages.success(request, 'Notificação enviada com sucesso.')

        elif opcao == 'excluir':
            notificacao = 'Conteúdo deletado permanentemente'
            
            messages.success(request, 'Conteúdo excluído com sucesso.')
        
            # Tags
            for tag in conteudo.tags.all():
                if tag.tags(manager="ativos").all().count() <= 1:
                    tag.ativo = False
                    tag.save()

            # Seção
            if conteudo.secao.conteudo_set(manager="ativos").all().count() <= 1:
                conteudo.secao.ativo = False
                conteudo.secao.save()

                if conteudo.secao.tecnologia.secao_set(manager="ativos").all().count() <= 1:
                    conteudo.secao.tecnologia.ativo = False
                    conteudo.secao.tecnologia.save()
            
            conteudo.delete()
            return HttpResponseRedirect("/denuncias/conteudos/")

        elif opcao == 'parece_ok':
            notificacao = 'Conteúdo ok'
            sinalizacao.delete()
            messages.success(request, 'Conteúdo com status ok.')
        else:
            messages.error(request, 'Opção inválida.')
            return HttpResponseRedirect("/denuncias/conteudos/")

    post_historico_sinalizacao_conteudo(request, conteudo, notificacao, opcao)
    return HttpResponseRedirect("/denuncias/conteudos/")

def post_historico_sinalizacao_conteudo(request, conteudo, notificacao, opcao):
    """ Criar objeto de histórico de sinalização de conteúdo """
    historico = denuncias.HistoricoSinalizacaoConteudo.objects.create(
                    usuario     = request.user,
                    notificacao = notificacao,
                    conteudo    = conteudo
                )
    historico.status = opcao
    historico.save()

def historico_sinalizacao_conteudo(request):
    """ Histórico de sinalizações de conteúdo """
    sinalizacao = denuncias.HistoricoSinalizacaoConteudo.objects.all().order_by('-data')

    paginator = Paginator(sinalizacao, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'sinalizacoes': page_obj
    }

    return render(request, 'denuncias/historico_sinalizacao_conteudo.html', context)

@user_passes_test(lambda u: u.is_superuser)
def sinalizacao_perfil(request):
    """ Página que mostra as sinalizações dos perfis """

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login')) 

    sinalizacao = denuncias.SinalizacaoPerfil.objects.filter(classificador='Negative').exclude(Q(notificado=True)|Q(silenciado=True)).first()
    
    context = dict()

    if sinalizacao:
        contagem    =  denuncias.SinalizacaoPerfil.objects.annotate(
                            nome_count=Count("sinalizacoes_nome", distinct=True),
                            foto_count=Count("sinalizacoes_foto", distinct=True),
                            condutas_count=Count("sinalizacoes_condutas", distinct=True),
                            descricao_count=Count("sinalizacoes_descricao", distinct=True),
                        ).values(
                            "nome_count",
                            "foto_count",
                            "condutas_count",
                            "descricao_count",
                        ).get(
                            id=sinalizacao.id
                        )

        lista_traducao = ({'nome_count': 'Nome', 
                'foto_count': 'Foto',
                'condutas_count': 'Condutas',
                'descricao_count': 'Descrição',
            })

        contagem = dict((lista_traducao[key], value) for (key, value) in contagem.items())
        contagem = {k:v for (k,v) in sorted(contagem.items(),key=lambda item: item[1], reverse=True) if v > 0}

        comentarios = denuncias.HistoricoSinalizacaoComentario.objects.filter(autor=sinalizacao.perfil.id, acao='remover')

        context['sinalizacao']  = sinalizacao
        context['perfil_id']    = sinalizacao.perfil.id
        context['contagem']     = contagem
        context['comentarios']  = comentarios

    return render(request, 'denuncias/sinalizacoes_perfis.html', context)

@user_passes_test(lambda u: u.is_superuser)
def apurar_perfil(request, sinalizacao_id):
    """ Apuração de sinalização de perfil """

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login')) 

    opcao           = request.POST['opcao']
    opcaoTempo      = request.POST.get('opcaoTempo', False)

    sinalizacao = denuncias.SinalizacaoPerfil.objects.get(id=sinalizacao_id)
    

    if Perfil.objects.filter(id=sinalizacao.perfil.id):
        perfil = Perfil.objects.get(id=sinalizacao.perfil.id)
        if opcao == 'excluir':
            notificacao = 'Perfil deletado permanentemente'
            acao        = 'excluir_conta'
            perfil.delete()
            messages.success(request, 'Perfil excluído com sucesso.')
        
        if opcao == 'parece_ok':
            notificacao = 'Perfil ok'
            acao        = 'parece_ok'           
            messages.success(request, 'Perfil com status ok.')
            sinalizacao.delete()
                
        if opcao == 'notificacao':  
            notificacao = request.POST['input-textarea']
            if len(notificacao) <= 0:
                messages.error(request, 'Campo de notificação está vázio')
                return HttpResponseRedirect("/denuncias/perfis/")

            acao                        = 'enviar_notificacao'
            mensagem                    = dict()
            mensagem["perfil"]          = sinalizacao.perfil.nome_completo()
            mensagem["notificacao"]     = notificacao
            
            # Mensagem de retorno ao usuário
            EmailSender(
                "IF-Study ADMs",
                [sinalizacao.perfil.email],
                f"Perfil Sinalizado - {mensagem['perfil']}",
                template_notificacao_perfil.format(**mensagem)
            ).enviar()

            sinalizacao.notificado = True
            sinalizacao.save()
            messages.success(request, 'Notificação enviada com sucesso.')
        
        if opcao == 'silenciar':
            acao = 'silenciar_perfil'
            if opcaoTempo == 'prazo_medio':
                tempo = denuncias.PerfilSilenciado(
                            perfil = perfil
                        )
                tempo.silenciado = 'prazo_medio'
                notificacao = 'Perfil silenciado por 15 dias'
            else:
                tempo = denuncias.PerfilSilenciado(
                            perfil = perfil
                        )
                tempo.silenciado = 'prazo_grande'
                notificacao = 'Perfil silenciado por 30 dias'
            tempo.save()
            sinalizacao.silenciado = True
            sinalizacao.save()
            messages.success(request, 'Perfil silenciado com sucesso.')

    post_historico_sinalizacao(request, perfil, notificacao, acao)
    return HttpResponseRedirect("/denuncias/perfis/")


def post_historico_sinalizacao(request, perfil, notificacao, acao):
    """ Criar objeto de histórico de sinalização de perfil """
    historico = denuncias.HistoricoSinalizacaoPerfil(
                usuario     = request.user,
                notificacao = notificacao,
                perfil      = perfil.username
            )
    historico.acao = acao
    historico.save()


def historico_sinalizacao_perfil(request):
    """ Histórico de sinalizações de conteúdo """
    sinalizacao = denuncias.HistoricoSinalizacaoPerfil.objects.all().order_by('-data')

    paginator = Paginator(sinalizacao, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'sinalizacoes': page_obj
    }

    return render(request, 'denuncias/historico_sinalizacao_perfil.html', context)