from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from .forms import PerfilForm, PerfilDataForm   
from .models import Perfil, PerfilData
from denuncias.models import SinalizacaoPerfil
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from conteudos.models import Conteudo
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Q
from django.db.models import Count

# Verificação de email
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from utils.email.email import EmailSender
from utils.email_templates.verificacao_perfil import default_message as template_verificacao_perfil


@login_required(login_url = 'login')
def perfil(request, perfil_id):
    """ Informações sobre o perfil """
    
    perfil = Perfil.objects.get(id=perfil_id)

    context = {
        'perfil': perfil,
        'perfil_id': perfil_id
    }

    return render(request, 'usuarios/perfil.html', context)


@login_required(login_url = 'login')
def editar_perfil(request, perfil_id):
    """ Edição de informações do perfil """

    perfil_instance = get_object_or_404(PerfilData, user=request.user)
    perfil          = get_object_or_404(Perfil, id=perfil_id)

    if request.method == 'POST':
        perfil_form         = PerfilForm(request.POST, instance=request.user)
        perfil_data_form    = PerfilDataForm(request.POST, request.FILES, instance=perfil_instance)

        if perfil_form.is_valid() and perfil_data_form.is_valid():
            perfil_form.save()
            perfil_data_form.save()
            messages.success(request, 'Seu perfil foi alterado com sucesso.')
            return HttpResponseRedirect('/perfil/editar/%d/'%request.user.id)
    else:
        perfil_form = PerfilForm(instance=request.user)
        perfil_data_form = PerfilDataForm(instance=perfil_instance)


    context={
        'perfil': perfil,
        'perfil_form': perfil_form,
        'perfil_data': perfil_data_form,
        'perfil_id': perfil_id
    }
 
    if SinalizacaoPerfil.objects.filter(perfil=perfil, notificado=True).exists():
        sinalizacao = SinalizacaoPerfil.objects.get(perfil=perfil, notificado=True)
        sinalizacao.delete()

    return render(request, 'usuarios/editar_profile.html', context)

@login_required(login_url = 'login')
def trocar_senha(request, perfil_id):
    """ Edição de senha """

    perfil = get_object_or_404(Perfil, id=perfil_id)

    if request.method == 'POST':
        atual_senha     = request.POST['atual_senha']
        nova_senha      = request.POST['nova_senha']
        confirmar_senha = request.POST['confirmar_senha']

        usuario = Perfil.objects.get(email__exact=request.user.email)

        if nova_senha == confirmar_senha:
            sucesso = usuario.check_password(atual_senha)
            if sucesso:
                usuario.set_password(nova_senha)
                usuario.save()
                messages.success(request, 'Senha alterado com sucesso.')
                return HttpResponseRedirect('/perfil/senha/%d/'%request.user.id)
            else:
                messages.error(request, 'A senha atual está inválida.')
                return HttpResponseRedirect('/perfil/senha/%d/'%request.user.id)
        else:
            messages.error(request, 'Senhas de confirmação não coincidem!')
            return HttpResponseRedirect('/perfil/senha/%d/'%request.user.id)

    context = {
        'perfil': perfil,
        'perfil_id': perfil_id
    }

    return render(request, 'usuarios/trocar_senha.html', context)


@login_required(login_url = 'login')
def perfil_conteudos(request, perfil_id):
    """ Conteúdos que o usuário postou """

    perfil      = get_object_or_404(Perfil, id=perfil_id)
    conteudos   = Conteudo.ativos.filter(criador=perfil_id).order_by('-data')
    
    paginator = Paginator(conteudos, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'conteudos': page_obj,
        'perfil': perfil,
        'perfil_id': perfil_id
    }

    return render(request, 'usuarios/perfil_conteudos.html', context)

def is_owner(request, perfil_id):
    """ Requisição que retorna True caso o requisitante seja dono do perfil e False caso não seja """
    return JsonResponse({"is_owner": request.user.id == perfil_id} ,status=200)

@transaction.atomic
def gerar_sinalizacao_perfil(request, perfil_id):
    """ Pegar as informações via AJAX """

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))   

    sinalizacao = SinalizacaoPerfil.objects.filter(perfil=perfil_id)
    perfil      = Perfil.objects.get(id=perfil_id)
    opcao       = request.POST['opcao']

    atributos = [
                    'sinalizacoes_nome', 'sinalizacoes_foto', 'sinalizacoes_condutas',
                    'sinalizacoes_descricao'
                ]

    if opcao not in atributos:
        return JsonResponse(status=403, data={"msg": "A opção que você escolheu é inválida."})

    if sinalizacao.exists():
        sinalizacao = SinalizacaoPerfil.objects.get(perfil=perfil_id)

        if sinalizacao.silenciado:
            return JsonResponse({"msg": "Este perfil está silenciado. Aguarde o término do silenciamento para denunciar."} ,status=403)

        if SinalizacaoPerfil.objects.filter(Q(sinalizacoes_nome=request.user)| Q(sinalizacoes_foto=request.user)
                                                | Q(sinalizacoes_condutas=request.user)|Q(sinalizacoes_descricao=request.user),
                                                perfil=perfil_id):
                                                return JsonResponse({"msg": "Espere a avaliação dos Administradores para a conclusão da sinalização"} ,status=403) 
        else:
            getattr(sinalizacao, opcao).add(request.user)

    else:
        sinalizacao = SinalizacaoPerfil.objects.create(
            perfil = perfil,
        )
        getattr(sinalizacao, opcao).add(request.user)

    if sinalizacao.classificador == '':
        total_sinalizacao = (
                            SinalizacaoPerfil.objects.filter(perfil=perfil_id)
                            .annotate(
                                total=Count("sinalizacoes_nome", distinct=True)
                                + Count("sinalizacoes_foto", distinct=True)
                                + Count("sinalizacoes_condutas", distinct=True)
                                + Count("sinalizacoes_descricao", distinct=True)
                            )
                            .values("total"))[0]['total']
    
    print(total_sinalizacao)

    # alterar para 10
    if total_sinalizacao > 2:
        sinalizacao.classificador = 'Negative'
        sinalizacao.save()

    return JsonResponse({"msg": "Criado com sucesso"} ,status=200)


@transaction.atomic
def envio_confirmacao_email(request, perfil_id):
    """ Função que envia email para o usuário confirmar o cadastro """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))  

    user = Perfil.objects.get(id=perfil_id)

    # Informações para o template
    current_site = get_current_site(request)
    mensagem = dict()
    mensagem["usuario"]         = user.nome_completo()
    mensagem["domain"]          = str(current_site)
    mensagem["uid"]             = urlsafe_base64_encode(force_bytes(user.pk))
    mensagem["token"]           = default_token_generator.make_token(user)

    # Mensagem para confirmação de email
    EmailSender(
        "IF-Study ADMs",
        [user.email],
        f"Confirmação de email - {mensagem['usuario']}",
        template_verificacao_perfil.format(**mensagem)
    ).enviar()

    return HttpResponseRedirect('/perfil/informacoes/%d/'%perfil_id)


@login_required(login_url = 'login')
def ativar_perfil(request, uidb64, token):
    """ Ativação do perfil """

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))  

    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Perfil._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Perfil.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.email_confirmado = True
        user.save()
        messages.success(request, 'Parabéns! Sua conta foi ativada.')
        return redirect('index')
    else:
        messages.error(request, 'Link de ativação inválido')
        return redirect('login')