def middleware(next):
# Здесь можно выполнить какую-либо инициализацию
    def core_middleware(request):
# Здесь выполняется обработка клиентского запроса
        path = request.path
        if path != None:
            if path.find('nxcstorage') == -1:
                if 'nxcfolderid' in request.session:
                    del request.session['nxcfolderid']
                if 'ownerclass' in request.session:
                    del request.session['ownerclass']
                if 'ownerid' in request.session:
                    del request.session['ownerid']
        response = next(request)
# Здесь выполняется обработка ответа
        return response
    return core_middleware