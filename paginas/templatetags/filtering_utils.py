from django import template

register = template.Library()

@register.simple_tag
def get_ativos(obj, atributo):
    metodo = getattr(obj, atributo)
    return metodo(manager='ativos').all()
