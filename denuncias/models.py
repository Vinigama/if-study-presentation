
from tabnanny import verbose
from django.db import models
from conteudos import models as models_conteudos
from usuarios.models import Perfil
from django.db.models import Q

# Create your models here.
class SinalizacaoComentario(models.Model):
    tipos_sinalizacao = (
        ('rude', 'Rude'),
    ) 

    tipos_classificador = (
        ('Negative', 'Negativo'),
    )

    tipo_apuracao = (
        ('parece_ok', 'Parece Ok'),
    )

    classificador       = models.CharField(max_length=255, choices=tipos_classificador, blank=True)
    usuario             = models.ManyToManyField(Perfil, blank=True, related_name="+")
    tipo_sinalizacao    = models.CharField(max_length=255, choices=tipos_sinalizacao)
    comentario          = models.OneToOneField(models_conteudos.Comentario, related_name="Comentario", on_delete=models.CASCADE)
    apuracao_status     = models.CharField(max_length=255, choices=tipo_apuracao, blank=True)

    def __str__(self):
        return str(self.comentario)

    def conteudo(self):
        return self.comentario.conteudo

    def foto_conteudo(self):
        return self.comentario.criador

class HistoricoSinalizacaoComentario(models.Model):
    tipos_acoes = (
        ('parece_ok', 'Parece Ok'),
        ('remover', 'Remover'),
    )   

    usuario                     = models.ForeignKey(Perfil, max_length=255, related_name="+", verbose_name="Usuário", on_delete=models.CASCADE)
    autor                       = models.ForeignKey(Perfil, max_length=255, related_name="+", verbose_name="Autor", on_delete=models.CASCADE)
    comentario                  = models.CharField(max_length=255, verbose_name="Comentário")
    acao                        = models.CharField(max_length=255, choices=tipos_acoes, verbose_name='Ação')
    data                        = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comentario

    def acao_verbose(self):
        return dict(HistoricoSinalizacaoComentario.tipos_acoes)[self.acao]


class HistoricoSinalizacaoConteudo(models.Model):
    tipos_status = (
        ('aguardando_edicao', 'Aguardando Edição'),
        ('edicao_concluida', 'Edição Concluída'),
        ('excluir_conteudo', 'Excluir Conteúdo'),
        ('parece_ok', 'Parece Ok')
    )   

    usuario                     = models.ForeignKey(Perfil, max_length=255, verbose_name="Usuário", on_delete=models.CASCADE)
    notificacao                 = models.CharField(max_length=255, verbose_name="Notificação")
    status                      = models.CharField(max_length=255, choices=tipos_status, verbose_name='Ação')
    data                        = models.DateTimeField(auto_now_add=True)
    conteudo                    = models.ForeignKey(models_conteudos.Conteudo, related_name="+", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.usuario.nome_completo()} - {self.notificacao}"

    def status_verbose(self):
        return dict(HistoricoSinalizacaoConteudo.tipos_status)[self.status]


class SinalizacaoConteudo(models.Model):
    tipo_classificador = (
        ('Negative', 'Negativo'),
    )

    conteudo                    = models.OneToOneField(models_conteudos.Conteudo, related_name="Conteudo", on_delete=models.CASCADE, limit_choices_to={'ativo': True})
    sinalizacoes_conteudo       = models.ManyToManyField(Perfil, blank=True, related_name="+", verbose_name='Sinalizações Conteúdo')
    sinalizacoes_titulo         = models.ManyToManyField(Perfil, blank=True, related_name="+", verbose_name='Sinalizações Título')
    sinalizacoes_descricao      = models.ManyToManyField(Perfil, blank=True, related_name="+", verbose_name='Sinalizações Descrição')
    sinalizacoes_tecnologia     = models.ManyToManyField(Perfil, blank=True, related_name="+", verbose_name='Sinalizações Tecnologia')
    sinalizacoes_secao          = models.ManyToManyField(Perfil, blank=True, related_name="+", verbose_name='Sinalizações Seção')
    notificado                  = models.BooleanField(default=False)
    classificador               = models.CharField(max_length=255, choices=tipo_classificador, blank=True)

    def __str__(self):
        return f'{self.conteudo}'

class SinalizacaoPerfil(models.Model):
    tipo_classificador = (
        ('Negative', 'Negativo'),
    )

    perfil                      = models.OneToOneField(Perfil, related_name="Conteudo", on_delete=models.CASCADE)
    sinalizacoes_nome           = models.ManyToManyField(Perfil, blank=True, related_name="+", verbose_name='Sinalizações Nome')
    sinalizacoes_foto           = models.ManyToManyField(Perfil, blank=True, related_name="+", verbose_name='Sinalizações Foto')
    sinalizacoes_condutas       = models.ManyToManyField(Perfil, blank=True, related_name="+", verbose_name='Sinalizações Condutas')
    sinalizacoes_descricao      = models.ManyToManyField(Perfil, blank=True, related_name="+", verbose_name='Sinalizações Descrição')
    notificado                  = models.BooleanField(default=False)
    silenciado                  = models.BooleanField(default=False)
    classificador               = models.CharField(max_length=30, choices=tipo_classificador, blank=True)
    

    def __str__(self):
        return f'{self.perfil.nome_completo()}'


class HistoricoSinalizacaoPerfil(models.Model):
    tipos_status = (
        ('excluir_conta', 'Excluir Conta'),
        ('silenciar_perfil', 'Silenciar Perfil'),
        ('enviar_notificacao', 'Enviar Notificação'),
        ('parece_ok', 'Parece Ok'),
    )   

    usuario                     = models.ForeignKey(Perfil, max_length=255, verbose_name="Usuário", related_name="+", on_delete=models.CASCADE)
    notificacao                 = models.CharField(max_length=255, verbose_name="Notificação", null=True)
    acao                        = models.CharField(max_length=255, choices=tipos_status, default=tipos_status[0][0], verbose_name='Ação')
    data                        = models.DateTimeField(auto_now_add=True)
    perfil                      = models.CharField(max_length=100, verbose_name="Perfil Sinalizado")

    def __str__(self):
        return f"{self.notificacao}"

    def status_verbose(self):
        return dict(HistoricoSinalizacaoPerfil.tipos_status)[self.acao]

    def perfil_ativo(self):
        filtro = Perfil.objects.get(username=self.perfil)
        if filtro:
            return filtro.id
        return False

class PerfilSilenciado(models.Model):
    time_mute = (
        ('prazo_medio', '15 Dias'),
        ('prazo_grande', '30 Dias')
    )

    perfil          = models.OneToOneField(Perfil, related_name="+", verbose_name='Perfil Silenciado', on_delete=models.CASCADE)
    silenciado      = models.CharField(max_length=50, choices=time_mute, blank=True, verbose_name='Tempo Mutado')
    data            = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.perfil.nome_completo()}'