def middleware(next):
# Здесь можно выполнить какую-либо инициализацию
    def core_middleware(request):
# Здесь выполняется обработка клиентского запроса
        path = request.path
        if path != None:
            if path.find('ttnexample') == -1:
                if 'ttneid' in request.session:
                    del request.session['ttneid']
            if path.find('mic') == -1:
                if 'micid' in request.session:
                    del request.session['micid']
            if path.find('commdevice') == -1:
                if 'cdid' in request.session:
                    del request.session['cdid']
            if path.find('meter') == -1:
                if 'meterid' in request.session:
                    del request.session['meterid']
        response = next(request)
# Здесь выполняется обработка ответа
        return response
    return core_middleware