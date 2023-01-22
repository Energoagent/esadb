def middleware(next):
# Здесь можно выполнить какую-либо инициализацию
    def core_middleware(request):
# Здесь выполняется обработка клиентского запроса
        path = request.path
        if path != None:
            if path.find('einst') == -1:
                if 'einstid' in request.session:
                    del request.session['einstid']
                if 'einstname' in request.session:
                    del request.session['einstname']
        response = next(request)
# Здесь выполняется обработка ответа
        return response
    return core_middleware