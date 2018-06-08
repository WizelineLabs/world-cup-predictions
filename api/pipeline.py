from django.core.files.base import ContentFile
from requests import request, ConnectionError


def save_avatar(backend, user, response, is_new,  *args, **kwargs):
    '''
    Get the user avatar
    '''
    if response.get('image') and response['image'].get('url'):
        url = response['image'].get('url')
        user.avatar = url
        user.save()