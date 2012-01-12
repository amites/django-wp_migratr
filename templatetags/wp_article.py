from django import template
from django.utils.html import linebreaks
from wordpress_xmlrpc.methods.posts import GetPost

from wp_migratr.articles import wpClient, wpCaption


register = template.Library()

@register.simple_tag
def wpArticle(format_string):
    '''
    Simple tag to pull the contents of a Wordpress Article inside a Django
    template. Best used with caching.
    '''
    wp = wpClient()
    post = wp.call(GetPost(format_string))
    return linebreaks(wpCaption(post.description))


