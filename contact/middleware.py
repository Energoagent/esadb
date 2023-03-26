def middleware(next):
# Здесь можно выполнить какую-либо инициализацию
    def core_middleware(request):
# Здесь выполняется обработка клиентского запроса
        path = request.path
        if path != None:
            if path.find('contacts') == -1:
                if 'contactid' in request.session:
                    del request.session['contactid']
                if 'cntownerclass' in request.session:
                    del request.session['cntownerclass']
                if 'cntownerid' in request.session:
                    del request.session['cntownerid']
        response = next(request)
# Здесь выполняется обработка ответа
        return response
    return core_middleware