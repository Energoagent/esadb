def as_middleware(next):
# Здесь можно выполнить какую-либо инициализацию
    def core_middleware(request):
# Здесь выполняется обработка клиентского запроса
        path = request.path
        if path != None:
            if path.find('albums') == -1:
                if 'albumid' in request.session:
                    del request.session['albumid']
                if 'ownerclass' in request.session:
                    del request.session['ownerclass']
                if 'ownerid' in request.session:
                    del request.session['ownerid']
        response = next(request)
# Здесь выполняется обработка ответа
        return response
    return core_middleware