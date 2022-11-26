from email.policy import default
from django.db import models
from usuarios.models import Perfil
from datetime import timedelta
from django.utils import timezone

class AtivoManager(models.Manager):
    def get_queryset(self):
        return super(AtivoManager, self).get_queryset().filter(ativo=True)

class InativoManager(models.Manager):
    def get_queryset(self):
        return super(InativoManager, self).get_queryset().filter(ativo=False)

class Ativo:
    def is_active(self):
        return self.ativo
    
    def ativar(self):
        self.ativo = True
        self.save()
    
    def desativar(self):
        self.ativo = False
        self.save()

class Conteudo(models.Model, Ativo):
    tipos = (
        ('video', 'Vídeo'),
        ('arquivo', 'Arquivo')
    )

    arquivo         = models.FileField(upload_to='conteudos')
    titulo          = models.CharField(max_length=255, verbose_name="Título")
    thumbnail       = models.FileField(upload_to='images')
    descricao       = models.TextField(max_length=255, verbose_name="Descrição")
    tipo            = models.CharField(max_length=255, choices=tipos)
    ativo           = models.BooleanField(default=False)
    carga           = models.PositiveIntegerField(default=0, null=False, blank=False) # Carga, em segundos, dada para o conteúdo

    secao           = models.ForeignKey("Secao", on_delete=models.CASCADE)
    criador         = models.ForeignKey(Perfil, on_delete=models.CASCADE)
    tags            = models.ManyToManyField("Tag", blank=True, related_name="tags")

    like            = models.ManyToManyField(Perfil, blank=True, related_name="+")
    dislike         = models.ManyToManyField(Perfil, blank=True, related_name="+")

    visualizacao    = models.ManyToManyField(Perfil, blank=True, related_name="+")

    data            = models.DateTimeField(auto_now_add=True)

    baixa           = models.BooleanField(default=False)
    data_baixa      = models.DateTimeField(null=True, blank=True)
    responsavel_baixa = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name="conteudo_baixa", null=True)

    objects     = models.Manager()
    ativos      = AtivoManager()
    inativos    = InativoManager()

    def __str__(self):
        return self.titulo

    def custom_titulo(self):
        if len(self.titulo) > 13:
            return self.titulo[0:13] + '.'

        return self.titulo

    def quantidade_like(self):
        """ Retorna a quantidade de like que o comentário possui """
        return self.like.count()

    def quantidade_dislike(self):
        """ Retorna a quantidade de dislike que o comentário possui """
        return self.dislike.count()

    def quantidade_visualizacao(self):
        """ Retorna a quantidade de like que o comentário possui """
        return self.visualizacao.count()

class Secao(models.Model, Ativo):
    class Meta:
        unique_together = ('nome', 'tecnologia',)
    nome        = models.CharField(max_length=255)
    ativo       = models.BooleanField(default=False)

    tecnologia  = models.ForeignKey("Tecnologia", on_delete=models.CASCADE)

    objects     = models.Manager()
    ativos      = AtivoManager()
    inativos    = InativoManager()

    def __str__(self):
        return self.nome


class Tecnologia(models.Model, Ativo):
    nome        = models.CharField(max_length=255, unique=True)
    ativo       = models.BooleanField(default=False)

    objects     = models.Manager()
    ativos      = AtivoManager()
    inativos    = InativoManager()

    def __str__(self):
        return self.nome

class Tag(models.Model, Ativo):
    nome        = models.CharField(max_length=255)
    ativo       = models.BooleanField(default=False)

    conteudos   = models.ManyToManyField(Conteudo)

    objects     = models.Manager()
    ativos      = AtivoManager()
    inativos    = InativoManager()

    def __str__(self):
        return self.nome


class Comentario(models.Model):
    comentario  = models.CharField(max_length=255)

    resposta    = models.ForeignKey('self', related_name='resposta_set', on_delete=models.CASCADE, blank=True, null=True)
    conteudo    = models.ForeignKey(Conteudo, on_delete=models.CASCADE)
    criador     = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='criador')

    like        = models.ManyToManyField(Perfil, blank=True, related_name="like")
    dislike     = models.ManyToManyField(Perfil, blank=True, related_name="dislike")

    publicado   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comentario

    def quantidade_like(self):
        """ Retorna a quantidade de like que o comentário possui """
        return self.like.count()

    def quantidade_dislike(self):
        """ Retorna a quantidade de dislike que o comentário possui """
        return self.dislike.count()

    def quantidade_like_resposta(self):
        """ Retorna a quantidade de like que a resposta possui """
        return self.resposta.like.count()

    def nome_completo(self):
        return f'{self.criador.first_name.title()} {self.criador.last_name.title()}'

class AltaManager(models.Manager):
    def select_old(self):
        seven_days_ago = timezone.now() - timedelta(days=7)
        return self.filter(data__lt=seven_days_ago)


class Visualizacao(models.Model):
    objects      = AltaManager()
    
    visualizador = models.ManyToManyField(Perfil, related_name='visualizador')
    conteudo     = models.ForeignKey(Conteudo, on_delete=models.CASCADE, related_name='conteudo', limit_choices_to={'ativo': True})
    data         = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return  f'{self.conteudo}'


class Historico(models.Model):
    visualizador = models.ManyToManyField(Perfil, related_name='+')
    conteudo     = models.ForeignKey(Conteudo, on_delete=models.CASCADE, limit_choices_to={'ativo': True}, related_name="+")   
    data         = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.conteudo}'

