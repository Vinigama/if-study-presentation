from django.contrib import admin
from . import models
from django.urls import reverse
from django.utils.html import format_html

def aceitar_solicitacao(modeladmin, request, queryset):
    for entry in queryset:
        entry.aceita_requisicao()
aceitar_solicitacao.short_description = "Aceitar solicitacao"

class RequisicaoFormularioAdmin(admin.ModelAdmin):
    actions = [aceitar_solicitacao]
    list_display = (
        'tipo_requisicao',
        'conteudo_pendente',
        'verifica_requisicao',
    )
    readonly_fields = (
        'verifica_requisicao',
    )

    def process_deposit(self):
        pass

    def verifica_requisicao(self, obj):
        return format_html(
            '<a class="ui green fluid button" href="{}">Verificar solicitação</a>&nbsp;',
            reverse('router_requisicao', args=[obj.pk]),
        )
    verifica_requisicao.short_description = 'Verificar solicitação'
    verifica_requisicao.allow_tags = True

admin.site.register(models.RequisicaoFormulario, RequisicaoFormularioAdmin)
