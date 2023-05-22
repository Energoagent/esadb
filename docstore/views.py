import os
from django.shortcuts import render, redirect
from django import forms
from pathlib import Path
from django.views import generic
from django.views.decorators.http import require_http_methods
from django.db import models
from django.http import FileResponse

from django.conf import settings
from docstore.models import DocStore, documenttype, dtdict
from contact.models import Contact
from channel.models import Channel
from org.models import Organization
from project.models import Project
from commdevice.models import CommDevice
from esadbsrv.viewmods.viewcommon import CompleteListView
from einst.models import EInst
from ttnexample.models import TTNExample
from meter.models import Meter
from mic.models import MIC

class DocStoreListView(CompleteListView):
    model = DocStore
    template_name = 'docstore_list.html'
    paginate_by = 10
    ordering = 'doctype'
    subtitle = 'Медиа: документы'
    filterkeylist = {'Тип документа':'doctype', 'Наименование':'name', 'Номер':'number'}
    contextmenu = {'Добавить': 'formmethod=GET formaction=create/',
        'Просмотреть': 'formmethod=GET formaction=detail/',
        'Изменить': 'formmethod=GET formaction=update/',
        'Удалить': 'formmethod=GET formaction=delete/',
        'Вернуться': 'formmethod=GET formaction=../'}
    is_filtered = True
    def get_queryset(self):
        dsownerid = self.request.GET.get('dsownerid')
        if dsownerid == None: dsownerid = self.request.session.get('dsownerid')
        dsownerclassname = self.request.GET.get('dsownerclass')
        if dsownerclassname == None: 
            dsownerclassname = self.request.session.get('dsownerclass')
            if (dsownerclassname == None) or (dsownerclassname == ''): return super().get_queryset()
        dsowner = eval(dsownerclassname + '.objects.get(id = dsownerid)')
        if dsowner == None: return super().get_queryset()
        self.request.session['dsownerclass'] = dsownerclassname
        self.request.session['dsownerid'] = dsowner.id
        self.request.session.modified = True
        return dsowner.docs.all()


@require_http_methods(['GET'])
def deleteview(request):
    dsid = request.GET.get('dsid')
    if dsid != None:
        document = DocStore.objects.get(id = dsid)
# сделать удаление файла
        document.delete()
    return redirect('../')
        
@require_http_methods(['GET'])
def detailview(request):
    dsid = request.GET.get('dsid')
    if dsid != None: 
        return render(request, 'docstore_detail.html', 
            context = {
                'status':'', 
                'document': DocStore.objects.get(id = dsid),
                'contextmenu': {'Вернуться':'formmethod=GET formaction=../', 
                    'Изменить': 'formmethod=GET formaction=../update/', 
                    'Удалить': 'formmethod=GET formaction=../delete/'},
                'subtitle':'Медиа: документы: просмотр'})
    return redirect('../')

class DocStoreModelForm(forms.ModelForm):
    class Meta:
        model = DocStore
        fields = '__all__'
#        widgets = {
#            'doctype': forms.Select(attrs = {'size': 1}),
#            'date': forms.DateInput(attrs = {'format': 'd.m.Y'}),
#            'docfile': forms.FileInput()
#            }

@require_http_methods(['GET', 'POST'])
def updateview(request):
    context = {'status':'',
        'contextmenu':{'Подтвердить':'formmethod=POST', 'Отменить':'formmethod=GET formaction=../'}, 
        'subtitle':'Медиа: документы: изменение'}
    if request.method == 'POST':
        dsid = request.POST.get('dsid')
        if dsid == None:
            return redirect('../')
        else:
            dsform = DocStoreModelForm(request.POST, request.FILES, instance = DocStore.objects.get(id = dsid))
            if dsform.is_valid():
                dsform.save()
                return redirect('../')
            else:
                context['form'] = dsform
                context['dsid'] = dsid
                return render(request, 'docstore_form.html', context = context)
    else:
        dsid = request.GET.get('dsid')
        if dsid == None:
            return redirect('../')
        else:
            dsform = DocStoreModelForm(instance = DocStore.objects.get(id = dsid))
            context['form'] = dsform
            context['dsid'] = dsid
            return render(request, 'docstore_form.html', context = context)

@require_http_methods(['GET', 'POST'])
def createview(request):
    context = {'status':'',
        'contextmenu':{
            'Отменить':'formmethod=GET formaction=../',
            'Подтвердить':'formmethod=POST'}, 
        'subtitle':'Медиа: документы: изменение'}
    if request.method == 'POST':
        dsform = DocStoreModelForm(request.POST, request.FILES)
        if dsform.is_valid():
            document = dsform.save(commit = False)
            document.save()
            dsownerid = request.session.get('dsownerid')
            dsownerclassname = request.session.get('dsownerclass')
            if dsownerclassname != None:
                dsowner = eval(dsownerclassname + '.objects.get(id = dsownerid)')
                if dsowner != None:
                    dsowner.docs.add(document)
            return redirect('../')
        else:
            context['form'] = dsform
            return render(request, 'docstore_form.html', context = context)
    else:
        context['form'] = DocStoreModelForm()
        return render(request, 'docstore_form.html', context = context)


def fileview(request, filename):
    fn = os.path.join(settings.MEDIA_ROOT, 'docstore/', filename)
    return FileResponse(open(fn, 'rb'), content_type='application/octet-stream')        

