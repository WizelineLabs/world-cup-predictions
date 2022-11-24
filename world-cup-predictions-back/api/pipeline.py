import logging

def save_avatar(request, backend, strategy, details, response, user=None, *args, **kwargs):
    '''
    Get the user avatar
    '''
    if response.get('image') and response['image'].get('url'):
        url = response['image'].get('url')
        user.avatar = url
        user.save()
    elif response.get('picture'):
        url = response["picture"]
        user.avatar = url
        user.save()