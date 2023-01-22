from django.shortcuts import render, redirect
from django import forms
from django.forms import ModelForm
from django.views import generic
from django.views.generic.edit import CreateView

from project.models import Project
from esadbsrv.viewmods.viewcommon import CompleteListView

class ProjectListView(CompleteListView):
    model = Project
    template_name = 'project_list.html'
    paginate_by = 10
    ordering = 'name'
    subtitle = 'Проекты'
    filterkeylist = {'':''}
    is_filtered = False
    contextmenu = {'Выбрать': 'formmethod=GET formaction=select/',
        'Очистить выбор': 'formmethod=GET formaction=clear/',
        'Добавить': 'formmethod=GET formaction=create/', 
        'Просмотреть/Изменить': 'formmethod=GET formaction=detail/',
        'Удалить': 'formmethod=GET formaction=delete/',
        'Вернуться': 'formmethod=GET formaction=../'}
    def get_queryset(self):
        user = self.request.user
        return user.project_set.all()

def projectdetailview(request):
    if request.method == 'GET':
        projectid = request.GET.get('projectid')
        if projectid == None: 
            projectid = request.session.get('projectid')
        if projectid == None: 
            return redirect('../')
        project = Project.objects.get(id = projectid)
        request.session['projectid'] = project.pk
        request.session.modified = True
        context = {'status':'', 'project':project, 'ownerclass': project.__class__.__name__,
            'contextmenu':{'Вернуться':'formmethod=GET formaction=../', 
                'Изменить': 'formmethod=GET formaction=update/',
                'Контакты': 'formmethod=GET formaction=contacts/',
                'Документы': 'formmethod=GET formaction=docs/',},
#                'Объекты':'formmethod=GET formaction=einst/'}, 
            'subtitle':'Проект: просмотр'}
        return render(request, 'project_detail.html', context = context)
    else:
        return redirect('../')

class ProjectModelForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'info', 'note']

def projectcreateview(request):
    if request.method == 'POST':
        projectform = ProjectModelForm(request.POST)
        if projectform.is_valid():
            project = projectform.save()
            project.users.add(request.user)
            project.save()
            request.session['projectid'] = project.pk
            request.session.modified = True
            return redirect('../detail/' + '?projectid='+ str(project.id))
    else: projectform = ProjectModelForm()
    context = {}
    context['status'] = ''
    context['contextmenu'] = {'Отменить':'formmethod=GET formaction=../', 'Подтвердить':'formmethod=POST'}
    context['subtitle'] = 'Проект: создание'
    context['form'] = projectform
    return render(request, 'project_form.html', context = context)

def projectupdateview(request):
    if request.method == 'POST':
        projectid = request.POST.get('projectid')
        if projectid == None:
            return redirect('../')
        else:
            project = Project.objects.get(id = projectid)
            projectform = ProjectModelForm(request.POST, instance = project)
            if projectform.is_valid():
                project = projectform.save(commit = True)
                return redirect('../' + '?projectid='+ str(project.id))
    else: 
        projectid = request.GET.get('projectid')
        if projectid == None:
            return redirect('../')
        else:
            project = Project.objects.get(id = projectid)
            projectform = ProjectModelForm(instance = project)
    context = {}
    context['status'] = ''
    context['contextmenu'] = {'Отменить':'formmethod=GET formaction=../', 'Подтвердить':'formmethod=POST'}
    context['subtitle'] = 'Проект: создание'
    context['form'] = projectform
    context['projectid'] = projectid
    return render(request, 'project_form.html', context = context)

def projectdeleteview(request):
    if request.method == 'GET':
        projectid = request.GET.get('projectid')
        if projectid == None: projectid = request.session.get('projectid')
        if projectid:
            Project.objects.filter(id = projectid).delete()
            if 'projectid' in request.session:
                del request.session['projectid']
            if 'projectname' in request.session:
                del request.session['projectname']
            request.session.modified = True
    return redirect('../')

def projectselectview(request):
    if request.method == 'GET':
        projectid = request.GET.get('projectid')
        if projectid == None: projectid = request.session.get('projectid')
        if projectid:
            project = Project.objects.get(id = projectid)
            request.session['projectid'] = project.pk
            request.session['projectname'] = project.name
            request.session.modified = True
    return redirect('../')

def projectclearview(request):
    if request.method == 'GET':
        if 'projectid' in request.session:
            del request.session['projectid']
        if 'projectname' in request.session:
            del request.session['projectname']
        request.session.modified = True
    return redirect('../')

