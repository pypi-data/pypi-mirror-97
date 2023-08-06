from django.conf import settings


class EntityUrlMap:
    _BASE_URL = 'tesis_asn/api/'

    if not settings.DEBUG:
        _HOST_INSTITUCION = 'http://:8010/'
        _HOST_USER = 'http://:8020/'
        _HOST_PUBLICATION = 'http://:8030/'
        _HOST_CHAT = 'http://:8040/'
        _HOST_SECURITY = 'http://:8050/'
    else:
        _HOST_INSTITUCION = 'http://127.0.0.1:8010/'
        _HOST_USER = 'http://127.0.0.1:8020/'
        _HOST_PUBLICATION = 'http://127.0.0.1:8030/'
        _HOST_CHAT = 'http://127.0.0.1:8040/'
        _HOST_SECURITY = 'http://127.0.0.1:8050/'

    USER = f'{_HOST_USER}{_BASE_URL}user/'
    SECURITY = f'{_HOST_SECURITY}{_BASE_URL}security/'
    CHAT = f'{_HOST_CHAT}{_BASE_URL}chat/'
    INSTITUCION = f'{_HOST_INSTITUCION}{_BASE_URL}institucion/'
    PUBLICATION = f'{_HOST_PUBLICATION}{_BASE_URL}publication/'
