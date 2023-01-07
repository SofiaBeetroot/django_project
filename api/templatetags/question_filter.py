from django import template
import datetime
from api.models import Entry

register = template.Library()


@register.filter
def date_format(value):
    return datetime.datetime.strftime(value, '%d-%m-%y %H:%m')


@register.filter(name='title')
def make_title(value):
    return value.title()


@register.simple_tag
def current_time(format_string):
    return datetime.datetime.now().strftime(format_string)

@register.filter(name='likes')
def get_likes(post_id):
    return len(Entry.objects.filter(id=post_id))