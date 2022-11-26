from django import template

register = template.Library()

@register.simple_tag
def admin_editable(is_admin:bool, app:str, model:str, id:int):
    """
        Recebe um booleano de user.is_superuser e retorna
        atributos necessários para a tag caso verdadeiro.
        app - Nome do app Django onde se encontra o Model a ser editado
        model - Model a ser editado
    """
    if is_admin == True:
        return f'data-editable-model={model} data-editable-app={app} data-editable-id={str(id)} data-editable-component=true'
    else:
        return ''
