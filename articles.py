import re

from django.conf import settings
from wordpress_xmlrpc import Client
from wordpress_xmlrpc.methods.posts import GetPost


def wpClient():
    '''
    Base class used to connect to Wordpress via XMLRPC.
    '''
    return Client(settings.WORDPRESS_MIGRATR['server'],
            settings.WORDPRESS_MIGRATR['user'], 
            settings.WORDPRESS_MIGRATR['pass'])

def wpCaption(post):
    '''
    Filters a Wordpress Post for Image Captions 
    and renders to match HTML.
    '''
    for match in re.finditer(r"\[caption (.*?)\](.*?)\[/caption\]", post):
        meta = '<div '
        caption = ''
        for imatch in re.finditer(r'(\w+)="(.*?)"', match.group(1)):
            if imatch.group(1) == 'id':
                meta += 'id="%s" ' % imatch.group(2)
            if imatch.group(1) == 'align':
                meta += 'class="wp-content %s" ' % imatch.group(2)
            if imatch.group(1) == 'width':
                meta += 'style="width: %spx;" ' % str(int(imatch.group(2)) + 10)
            if imatch.group(1) == 'caption':
                caption = imatch.group(2)
        meta += '>%s<p class="wp-caption-text">%s</p></div>' % \
            (match.group(2), caption)
        post = post.replace(match.group(0), meta)
    return post
