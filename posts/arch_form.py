from django import template
from posts.forms import DateForm

register = template.Library()


@register.inclusion_tag('posts/_arch_form.html')
def arch_form():
    arch_form = DateForm()
    return {'arch_form': arch_form}
