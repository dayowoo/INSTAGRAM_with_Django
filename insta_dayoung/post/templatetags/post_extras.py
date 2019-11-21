from django import template
import re

register = template.Library()

@register.filter
def add_link(value):
    content = value.content
    tags = value.hashtags.all()


    for tag in tags:
        content = content.replace(f"{tag.content}",f"<a href='/hashtags/{tag.id}/'>{tag.content}</a>")
        return content