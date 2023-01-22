
def einstcontext(request):
    einstname = request.session.get('einstname')
    if einstname == None:
        einstname = '-'
    return {'einstname': einstname}

