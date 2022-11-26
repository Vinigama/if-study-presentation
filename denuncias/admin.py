from django.contrib import admin
from . import models

# Register your models here.
admin.site.register([
    models.SinalizacaoComentario,
    models.HistoricoSinalizacaoComentario,
    models.SinalizacaoConteudo,
    models.HistoricoSinalizacaoConteudo,
    models.SinalizacaoPerfil,
    models.HistoricoSinalizacaoPerfil,
    models.PerfilSilenciado
    ])