from multiprocessing import managers
from django.db import models
from conteudos import models as models_conteudos
from django.contrib.auth.models import User
from django.forms.models import model_to_dict

class RequisicaoFormulario(models.Model):
    tipos = (
        ('adicao', 'Adição'),
        ('exclusao', 'Exclusão'),
        ('atualizacao', 'Atualização'),
    ) 
    tipo_requisicao     = models.CharField(max_length=255, choices=tipos)
    conteudo_pendente   = models.ForeignKey(models_conteudos.Conteudo, related_name="conteudo_pendente", on_delete=models.CASCADE, null=False, blank=False)
    conteudo_atualizar  = models.ForeignKey(models_conteudos.Conteudo, related_name="conteudo_atualizar", on_delete=models.CASCADE, null=True, blank=True)
    data_requisicao     = models.DateTimeField(auto_now_add=True)

    def aceita_requisicao(self):
        tipo = self.tipo_requisicao
        if tipo == 'adicao':
            self.adiciona_conteudo()
            self.delete_self()
        elif tipo == 'exclusao':
            self.apaga_conteudo()
        elif tipo == 'atualizacao':
            self.atualiza_conteudo()
            self.conteudo_pendente.delete()
            self.conteudo_pendente = self.conteudo_atualizar
            self.adiciona_conteudo()
            self.delete_self()
        else:
            raise ValueError("CRITICAL | Parâmetro 'tipo_requisicao' não está dentro dos valores aceitos")

    def adiciona_conteudo(self):
        conteudo = self.conteudo_pendente
        conteudo.ativar()
        conteudo.secao.ativar()
        conteudo.secao.tecnologia.ativar()
        tags_validar = conteudo.tags.all()
        for tag in tags_validar:
            tag.ativar()
    
    def atualiza_conteudo(self):
        conteudo = self.conteudo_pendente
        conteudo_atualizar = self.conteudo_atualizar
        black_list = ["id", "thumbnail", "arquivo", "visualizacao", "carga"] # Chaves que não devem ser atualizadas
        
        conteudo_dicionario = model_to_dict(conteudo)
        not_common_types = [dict, list]
        # Adiciona todos os tipos não comuns à black list
        for key in conteudo_dicionario:
            if type(conteudo_dicionario[key]) in not_common_types:
                black_list.append(key)
        # Atualiza todos os tipos comuns não encontrados na black list
        keys = conteudo_dicionario.keys() - black_list
        for key in keys:
            setattr(conteudo_atualizar, key, getattr(conteudo, key))
        # Atualiza tipos não comuns
        ## Tags
        conteudo_atualizar.tags.set(conteudo.tags.all())
        ## Thumbnail
        if conteudo.thumbnail:
            conteudo_atualizar.thumbnail = conteudo.thumbnail
        conteudo_atualizar.save()

    def apaga_conteudo(self):
        # Inativa atributos que ficaram sem pai
        conteudo = self.conteudo_pendente

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
        
        # Apaga a entrada no banco
        conteudo.delete()
        self.delete_self()
    
    def rejeita_requisicao(self):
        tipo = self.tipo_requisicao
        if tipo == 'adicao':
            self.conteudo_pendente.delete()
            self.delete_self()
        elif tipo == 'exclusao':
            self.delete_self()
        elif tipo == 'atualizacao':
            self.conteudo_pendente.delete()
            self.delete_self()
        else:
            raise ValueError("CRITICAL | Parâmetro 'tipo_requisicao' não está dentro dos valores aceitos")

 
    def delete_self(self):
        self.delete()
    
    def __str__(self):
        return f"{self.tipo_requisicao} - {self.conteudo_pendente.titulo}"


