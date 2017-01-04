from django import template

register = template.Library()

@register.filter(name='get_selection_error')
def get_selection_error(errors_dict, name):
    return errors_dict.get(name, None)
