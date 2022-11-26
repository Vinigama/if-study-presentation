from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .models import RequisicaoFormulario

def router_requisicao(request, requisicao_id):
    """ Executar roteamento da requisição de acordo com o tipo de solicitação """
    requisicao = get_object_or_404(RequisicaoFormulario, pk=requisicao_id)
    tipo_requisicao = requisicao.tipo_requisicao
    if tipo_requisicao=='adicao':
        return HttpResponseRedirect(reverse('validar_conteudo', args=[requisicao_id]))
    elif tipo_requisicao=='atualizacao':
        return HttpResponseRedirect(reverse('validar_edicao_conteudo', args=[requisicao_id]))
    elif tipo_requisicao=='exclusao':
        return HttpResponseRedirect(reverse('validar_exclusao_conteudo', args=[requisicao_id]))
    else:
        return HttpResponse('Tipo de solicitação inválida')
    
