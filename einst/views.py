from django.shortcuts import render, redirect
from django import forms
from django.views import generic
from django.views.decorators.http import require_http_methods

from pathlib import Path
import openpyxl
import os
import re
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

def fnnormal(s1):
    s2 = []
    for c1 in s1:
        if re.match('[a-zA-Zа-яА-Я0-9]', c1):
            s2.append(c1)
        else:
            s2.append('_')
    return ''.join(s2)        
    

@require_http_methods(['GET'])
def einstreportview(request):
    '''
    формирование отчета в файл Excel
    '''    
    projectname = request.session.get('projectname')
    einstid = request.session.get('einstid')
    if einstid != None:
        einst = EInst.objects.get(id = einstid)
#        print('FL:', einst._meta.fieldlist())
# создаем книгу 
        wb = openpyxl.Workbook()
# делаем единственный лист активным 
        ws = wb.active
# вносим данные
        ws['A1'] = 'ПРОЕКТ'
        ws['B1'] = projectname
        ws['A2'] = 'ОБЪЕКТ'
        ws['B2'] = einst.name
        ws['A3'] = 'Перечень измерительных комплексов (ИИК)'
        ws.append(MIC.fldlist())
        miclist = einst.mic_set.all()
        for mic in miclist:
            ws.append(mic.valuelist())
        ws.append(['Перечень измерительных трансформаторов'])
        for mic in miclist:
            ws.append(TTNExample.fldlist())
            for ttn in mic.ttnexample_set.all():
                ws.append(ttn.valuelist())
# сохраняем таблицу в папку esadb export
        basedir = Path(__file__).resolve().parent.parent
#        expdir = os.path.join(basedir, 'export')
        wbname = fnnormal(einst.name +'_' + date.today().strftime('%m-%d-%y'))
        try: 
#            wb.save(os.path.join(expdir, wbname + '.xlsx'))
            wb.save(os.path.join(settings.MEDIA_ROOT, 'docstore', wbname + '.xlsx'))
            report = DocStore()
            report.doctype = 'отчет'
            report.name = 'Сводный отчет об объекте: ' +  einst.name
            report.number = '_'
            report.date = date.today()
#            report.docfile = 'docstore/' + wbname + '.xlsx'
            report.docfile = os.path.join('docstore', wbname + '.xlsx')
            print('DF:', report.docfile)
            report.save()
            einst.docs.add(report)
        except: pass
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

