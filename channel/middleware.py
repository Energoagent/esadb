def middleware(next):
# Здесь можно выполнить какую-либо инициализацию
    def core_middleware(request):
# Здесь выполняется обработка клиентского запроса
        path = request.path
        if path != None:
            if path.find('channel') == -1:
                if 'channelid' in request.session:
                    del request.session['channelid']
                if 'chownerclass' in request.session:
                    del request.session['chownerclass']
                if 'chownerid' in request.session:
                    del request.session['chownerid']
        response = next(request)
# Здесь выполняется обработка ответа
        return response
    return core_middleware