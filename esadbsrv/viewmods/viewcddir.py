from django.shortcuts import render, redirect
from django import forms
from django.forms import ModelForm
from django.views.decorators.http import require_http_methods

from esadbsrv.models import CDDirectory
from esadbsrv.viewmods.viewcommon import CompleteListView

    
class CDDirectoryListView(CompleteListView):
    model = CDDirectory
    template_name = 'cddir/cddirectory_list.html'
    paginate_by = 10
    ordering = 'cdtype'
    subtitle = 'Оборудование: справочник устройств связи'
    contextmenu = {'Просмотреть': 'formmethod=GET formaction=detail/',
        'Добавить':'formmethod=get formaction=create/',
        'Изменить':'formmethod=get formaction=update/',
        'Удалить': 'formmethod=GET formaction=delete/',
        'Вернуться': 'formmethod=GET formaction=../'}
    filterkeylist = {'':'', 'Тип':'cdtype', 'Модель':'model', 'Изготовитель':'fabric'}
    is_filtered = True

@require_http_methods(['GET'])
def cddirectorydetailview(request):
    cddirid = request.GET.get('cddirid')
    if cddirid == None: 
        return redirect('../')
    else:
        context = {'status':'', 
            'cddirectory': CDDirectory.objects.get(id = cddirid),
            'contextmenu':{'Вернуться':'formmethod=GET formaction=../'},
            'subtitle':'Оборудование: справочник устройства связи: просмотреть'}
        return render(request, 'cddir/cddirectory_detail.html', context = context)

class CDDirectoryModelForm(forms.ModelForm):
    class Meta:
        model = CDDirectory
        fields = ['cdtype', 'model', 'fabric', 'info', 'note']

@require_http_methods(['GET', 'POST'])
def cddirectorycreateview(request):
    if request.method == 'POST':
        cddirform = CDDirectoryModelForm(request.POST)
        if cddirform.is_valid():
            cddirform.save(commit = True)
            return redirect('../detail/')
        else:
            cddirform = CDDirectoryModelForm(request.POST)
    else: 
        cddirform = CDDirectoryModelForm()
        context = {'status': '',
            'contextmenu': {'Отменить':'formmethod=GET formaction=../../', 'Подтвердить':'formmethod=POST'},
            'subtitle': 'Оборудование: справочник устройства связи: создать'}
        context['form'] = cddirform
    return render(request, 'cddir/cddirectory_form.html', context = context)

@require_http_methods(['GET', 'POST'])
def cddirectoryupdateview(request):
    if request.method == 'GET':
        cddirid = request.GET.get('cddirid')
        if cddirid != None:
            cddir = CDDirectory.objects.get(id = cddirid)
        else:
            return redirect('../')
        cddirform = CDDirectoryModelForm(instance = cddir)
    else:
        cddirid = request.POST.get('cddirid')
        if cddirid != None:
            cddir = CDDirectory.objects.get(id = cddirid)
        else:
            return redirect('../')
        cddirform = CDDirectoryModelForm(request.POST, instance = cddir)
        if cddirform.is_valid(): 
            cddir.save()
            return redirect('../')
    context = {'status':'',
        'contextmenu':{'Сохранить': 'formmethod=POST', 'Вернуться':'formmethod=GET formaction=../'}, 
        'subtitle':'Оборудование: справочник устройства связи: изменить'}
    context['form'] = cddirform
    context['cddirid'] = cddirid
    return render(request, 'cddir/cddirectory_form.html', context = context)

@require_http_methods(['GET'])
def cddirectorydeleteview(request):
    cddirid = request.GET.get('cddirid')
    if cddirid != None:
        CDDirectory.objects.filter(id = cddirid).delete()
    return redirect('../')


