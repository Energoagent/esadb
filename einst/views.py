from django.shortcuts import render, redirect
from django import forms
from django.views import generic
from django.views.decorators.http import require_http_methods

from pathlib import Path
import os
from datetime import date
from datetime import datetime

from django.conf import settings

from org.models import Organization
from ttnexample.models import TTNExample
from mic.models import MIC
from esadbsrv.viewmods.viewcommon import CompleteListView
from commdevice.views import CommDeviceListView
from einst.models import EInst
from project.models import Project
from docstore.models import DocStore
from meter.models import Meter
#from docstore.views import DocStoreModelForm

class EInstListView(CompleteListView):
    model = EInst
    template_name = 'einst_list.html'
    paginate_by = 10
    ordering = 'name'
    subtitle = 'Объекты'
    filterkeylist = {'':'', 'Наименование':'name', 'Адрес':'adress'}
    is_filtered = True
    contextmenu = {'Добавить': 'formmethod=GET formaction=create/', 
        'Просмотреть': 'formmethod=GET formaction=detail/',
        'Удалить': 'formmethod=GET formaction=delete/',
        'Вернуться': 'formmethod=GET formaction=../'}
    def get_queryset(self):
        orgid = self.request.GET.get('orgid')
        projectid = self.request.session.get('projectid')
        if (orgid == None) or (orgid == ''):
            if (projectid == None) or (projectid == ''):
                return super().get_queryset()
            else:
                return super().get_queryset().filter(project = projectid)
        else:
            return super().get_queryset().filter(project = projectid, owner = orgid)

@require_http_methods(['GET'])
def einstownerselect(request):
    einst = EInst.objects.get(id = request.session.get('einstid'))
    einst.owner = Organization.objects.get(id = request.GET.get('orgid'))
    einst.save()
    return redirect('../../')

@require_http_methods(['GET'])
def projectselect(request):
    einst = EInst.objects.get(id = request.session.get('einstid'))
    einst.project = Project.objects.get(id = request.GET.get('projectid'))
    einst.save()
    request.session['projectid'] = einst.project.pk
    request.session['projectname'] = einst.project.name
    request.session.modified = True
    return redirect('../../')

@require_http_methods(['GET'])
def einstdetailview(request):
    einstid = request.GET.get('einstid')
    if einstid == None: 
        einstid = request.session.get('einstid')
    if einstid == None: 
        return redirect('../')
    einst = EInst.objects.get(id = einstid)
    request.session['einstid'] = einst.pk
    request.session['einstname'] = einst.name
    request.session.modified = True
    context = {'status':'', 'einst': einst, 'ownerclass': einst.__class__.__name__,
        'contextmenu':{'Вернуться':'formmethod=GET formaction=../',
            'Изменить': 'formmethod=GET formaction=update/',
            'Включить в проект':'formmethod=GET formaction=project/',
            'Организация':'formmethod=GET formaction=owner/',
            'Контакты':'formmethod=GET formaction=contacts/',
            'Устройства связи':'formmethod=GET formaction=commdevice/',
            'Каналы связи':'formmethod=GET formaction=channels/',
            'ИИК':'formmethod=GET formaction=mic/',
            'Документы':'formmethod=GET formaction=docs/',
            'Альбомы':'formmethod=GET formaction=albums/',
            'Отчет':'formmethod=GET formaction=report/'},
        'subtitle':'Объекты: просмотр объекта'}
    return render(request, 'einst_detail.html', context = context)

class EInstModelForm(forms.ModelForm):
    class Meta:
        model = EInst
        fields = ['name', 'adress', 'info', 'note']

@require_http_methods(['GET', 'POST'])
def einstcreateview(request):
    if request.method == 'POST':
        eiform = EInstModelForm(request.POST)
        if eiform.is_valid():
            einst = eiform.save(commit = True)
            request.session['einstid'] = einst.pk
            request.session.modified = True
            return redirect('../detail/')
        else:
            eiform = EInstModelForm(request.POST)
    else: 
        eiform = EInstModelForm()
        context = {'status': '',
            'contextmenu': {'Отменить':'formmethod=GET formaction=../../', 'Подтвердить':'formmethod=POST'},
            'subtitle': 'Объекты: создание'}
        context['form'] = eiform
    return render(request, 'einst_form.html', context = context)

@require_http_methods(['GET', 'POST'])
def einstupdateview(request):
    if request.method == 'GET':
        einstid = request.GET.get('einstid')
        if einstid != None:
            einst = EInst.objects.get(id = einstid)
        else:
            return redirect('../')
        eiform = EInstModelForm(instance = einst)
    else:
        einstid = request.POST.get('einstid')
        einst = EInst.objects.get(id = einstid)
        eiform = EInstModelForm(request.POST, instance = einst)
        if eiform.is_valid():
            einst = eiform.save(commit = False)
            orgid = request.POST.get('orgid')
            if (orgid != None) and (orgid != ''):
                einst.owner = Organization.objects.get(id = orgid)
            einst.save()
        return redirect('../')
    context = {'status':'',
        'contextmenu':{'Сохранить': 'formmethod=POST', 'Вернуться':'formmethod=GET formaction=../'}, 
        'subtitle':'Объекты: изменить объект'}
    context['form'] = eiform
    context['einstid'] = einstid
    context['owner'] = einst.owner
    return render(request, 'einst_form.html', context = context)

@require_http_methods(['GET'])
def einstdeleteview(request):
    einstid = request.GET.get('einstid')
    if einstid != None:
        EInst.objects.filter(id = einstid).delete()
    return redirect('../')



class CDListView(CommDeviceListView):
    is_filtered = False
    def get_queryset(self):
        einstid = self.request.session.get('einstid')
        if (einstid != None) and (einstid != ''):
            einst = EInst.objects.get(id = einstid)
            cdlist = einst.commdevice_set.all()
            if cdlist != None:
                return cdlist
        return super.get_queryset()

