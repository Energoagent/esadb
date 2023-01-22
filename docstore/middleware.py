def ds_middleware(next):
# Здесь можно выполнить какую-либо инициализацию
    def core_middleware(request):
# Здесь выполняется обработка клиентского запроса
        path = request.path
        if path != None:
            if path.find('docs') == -1:
                if 'dsownerclass' in request.session:
                    del request.session['dsownerclass']
                    request.session.modified = True
                if 'dsownerid' in request.session:
                    del request.session['dsownerid']
                    request.session.modified = True
        response = next(request)
# Здесь выполняется обработка ответа
        return response
    return core_middleware