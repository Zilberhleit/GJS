import markdown
from django import template
from django.template.defaultfilters import truncatewords_html

register = template.Library()


@register.filter
def markdown_preview(value, words=100):
    if not value:
        return ""

    if "<!--more-->" in value:
        preview = value.split("<!--more-->")[0]
    else:
        preview = value

    html = markdown.markdown(preview, extensions=["extra", "codehilite"])

    return truncatewords_html(html, words)


@register.filter
def markdown_full(value):
    if not value:
        return ""
    return markdown.markdown(value, extensions=["extra", "codehilite"])
