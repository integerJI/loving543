from django.conf.urls import url
from django import template
import re

register = template.Library()

@register.filter
def add_link(value):
    text = value.text
    tags = value.tag_set.all()
    for tag in tags:
        text = re.sub(r'\#'+tag.tag_name+r'\b', '<a href="/what/explore/tags/'+tag.tag_name+'">#'+tag.tag_name+'</a>', text)
    return text