def middleware(next):
# Здесь можно выполнить какую-либо инициализацию
    def core_middleware(request):
# Здесь выполняется обработка клиентского запроса
        path = request.path
        if path != None:
            if path.find('meter') == -1:
                if 'meterid' in request.session:
                    del request.session['meterid']
        response = next(request)
# Здесь выполняется обработка ответа
        return response
    return core_middleware