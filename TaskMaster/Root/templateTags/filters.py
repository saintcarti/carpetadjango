from django import template

register = template.Library()

@register.filter
def is_in_groups(user, groups):
    """
    Verifica si un usuario pertenece a uno de los grupos especificados.
    `groups` debe ser una cadena de nombres de grupos separados por comas.
    """
    group_list = groups.split(',')
    return any(group in user.groups.values_list('name', flat=True) for group in group_list)
