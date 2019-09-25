from django.conf.urls import url
from django import template
import re

register = template.Library()

@register.filter
def add_link2(value):
    text3 = value.text3
    tags2 = value.tag_set2.all()
    for tag2 in tags2:
        text3 = re.sub(r'\#'+tag2.tag_name2+r'\b', '<a href="/what/explore/tags2/'+tag2.tag_name2+'">#'+tag2.tag_name2+'</a>', text3)
    return text3