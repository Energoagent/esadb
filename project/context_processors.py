
def projectcontext(request):
    projectname = request.session.get('projectname')
    if projectname == None:
        projectname = '-'
    return {'projectname': projectname}

