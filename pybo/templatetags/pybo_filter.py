import markdown
from django.utils.safestring import mark_safe
from django import template

register = template.Library()

@register.filter
def sub(value, arg):
    return value-arg    # 기존값 value- 입력받은값 arg

@register.filter
def mark(value):
    extendsions = ["nl2br","fenced_code"]
    return  mark_safe(markdown.markdown(value, extendsions=extendsions))

