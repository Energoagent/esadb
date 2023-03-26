
contextdict = {
    'docs':'документы',
    'doc':'документы',
    'albums': 'альбомы',
    'album': 'альбомы',
    'org': 'организации',
    'organization': 'организации',
    'contact': 'контакты',
    'einst': 'объекты',
    'atcttndirectory': 'справочник ТТН',
    'ttnexample': 'измерительные трансформаторы',
    'cddirectory': 'справочник устройств связи',
    'commdevice': 'устройства связи',
    'channels': 'каналы связи',
    'channel': 'каналы связи',
    'mic': 'ИИК',
    'meter': 'счетчик',
    'create': 'создать',
    'update': 'изменить',
    'detail': 'детали',
    'delete': 'удалить',
    }

def contextinfo(request):
    path = request.path
    pathlist = path.split('/')
    s1 = '> '
    for key in pathlist:
        if key in contextdict:
            s1 = s1 + '> ' + contextdict[key]
    return {'contextinfo': s1}
    
def addmicid(request):
    micid = request.session.get('micid')
    return {'micid': micid}
