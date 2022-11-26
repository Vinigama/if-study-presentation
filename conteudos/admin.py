from django.contrib import admin
from . import models

def ativar_conteudo(modeladmin, request, queryset):
    queryset.update(ativo=True)
ativar_conteudo.short_description = "Ativar conteúdo"

class ConteudoAdmin(admin.ModelAdmin):
    actions = [ativar_conteudo]

admin.site.register(models.Conteudo, ConteudoAdmin)

# Register your models here.
admin.site.register([
            # models.Conteudo,
            models.Secao,
            models.Tecnologia,
            models.Tag,
            models.Comentario,
            models.Visualizacao,
            models.Historico
            ])
