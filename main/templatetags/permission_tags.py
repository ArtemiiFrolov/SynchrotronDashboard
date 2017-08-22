from django import template
from django.conf import settings


register = template.Library()


@register.assignment_tag(takes_context=True)
def can(context, perm, obj=None):
    user = context['request'].user
    return user.has_perm(perm, obj)
