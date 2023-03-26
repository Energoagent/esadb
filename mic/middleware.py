def middleware(next):
# Здесь можно выполнить какую-либо инициализацию
    def core_middleware(request):
# Здесь выполняется обработка клиентского запроса
        path = request.path
        if path != None:
            if path.find('mic') == -1:
                if 'micid' in request.session:
                    del request.session['micid']
        response = next(request)
# Здесь выполняется обработка ответа
        return response
    return core_middleware