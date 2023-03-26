import os
from django.shortcuts import render, redirect
from django import forms
from django.core import validators
from django.forms import ModelForm, HiddenInput
from django.urls import reverse_lazy, reverse
from pathlib import Path
from django.views import generic
from django.views.decorators.http import require_http_methods

from ttnexample.models import TTNExample
from mic.models import MIC
from esadbsrv.models import ATCTTNDirectory
from albumstore.models import albumpath, ALBUM_DIR
from esadbsrv.viewmods.viewcommon import CompleteListView
from esadbsrv.viewmods.viewatcttndir import ATCTTNDirectoryListView

class TTNExampleListView(CompleteListView):
    model = TTNExample
    template_name = 'ttnexample_list.html'
    paginate_by = 10
    ordering = 'ttndir'
    subtitle = 'Оборудование: измерительные трансформаторы'
    contextmenu = {'Просмотреть/Изменить': 'formmethod=GET formaction=detail/',
        'Добавить': 'formmethod=GET formaction=create/',
        'Удалить': 'formmethod=GET formaction=delete/',
        'Копировать': 'formmethod=GET formaction=copy/',
        'Вернуться': 'formmethod=GET formaction=../'}
    filterkeylist = {'Сброс':'', 'Серийный номер':'sn', 'Модель':'ttnmodel', 'Изготовитель':'fabric', 'номер в ГРСИ':''}
    is_filtered = True
    def get_queryset(self):
        micid = self.request.GET.get('micid')
        if micid == None: micid = self.request.session.get('micid')
        if micid == None:
            return super().get_queryset()
        else:
            return TTNExample.objects.filter(mic = micid)
    
@require_http_methods(['GET'])
def ttnexampledetailview(request):
    ttneid = request.GET.get('ttneid')
    if ttneid == None: ttneid = request.session.get('ttneid')
    if ttneid == None: return redirect('../')
    ttne = TTNExample.objects.get(id = ttneid)
    request.session['ttneid'] = ttne.pk
    request.session.modified = True
    context = {'status':'', 'ttnexample':ttne, 'dsownerclass': ttne.__class__.__name__,
        'contextmenu':{'Изменить модель': 'formmethod=GET formaction=ttndirchoice/', 
            'Параметры': 'formmethod=GET formaction=update/',
            'Документы': 'formmethod=GET formaction=docs/',
            'Демонтировать': 'formmethod=GET formaction=deinst/',
            'Изменить ИИК': 'formmethod=GET formaction=reinst/',
            'Вернуться':'formmethod=GET formaction=../'}, 
        'subtitle':'Оборудование: измерительные трансформаторы: просмотр'}
    context['albumpath'] = ALBUM_DIR
    return render(request, 'ttnexample_detail.html', context = context)
    
@require_http_methods(['GET'])
def ttnexampledeleteview(request):
    ttneid = request.GET.get('ttneid')
    if ttneid == None: ttneid = request.session.get('ttneid')
    if ttneid != None: TTNExample.objects.filter(id = ttneid).delete()
    return redirect('../')

@require_http_methods(['GET'])
def ttnexampledeinstview(request):
    ttneid = request.GET.get('ttneid')
    if ttneid == None: ttneid = request.session.get('ttneid')
    if ttneid != None: 
        ttne = TTNExample.objects.get(id = ttneid)
        ttne.mic = None
        ttne.save()
        if 'ttneid' in request.session:
            del request.session['ttneid']
            request.session.modified = True
    return redirect('../')

@require_http_methods(['GET'])
def ttnexamplemicselectview(request):
    ttneid = request.GET.get('ttneid')
    if ttneid == None: ttneid = request.session.get('ttneid')
    if ttneid != None: 
        micid = request.GET.get('micid')
        if micid != None:
            ttne = TTNExample.objects.get(id = ttneid)
            ttne.mic = MIC.objects.get(id = micid)
            ttne.save()
    return redirect('../../')
        
class ATCTTNDirectoryChoiceView(ATCTTNDirectoryListView):
    subtitle = 'Оборудование: измерительный трансформатор: выбор модели из справочника АТС'
    contextmenu = {'Выбрать': 'formmethod=GET formaction=select/',
        'Отменить': 'formmethod=GET formaction=../'}

@require_http_methods(['GET'])
def directorychoiceselect(request):
    ttne = TTNExample.objects.get(id = request.session.get('ttneid'))
    ttne.ttndir = ATCTTNDirectory.objects.get(id = request.GET.get('ttndirid'))
    ttne.save()
    return redirect('../../')

class TTNExampleModelForm(forms.ModelForm):
    class Meta:
        model = TTNExample
        fields = ['ttntype', 'ph', 'bl', 'ttnmodel', 'sn', 'fbdate', 'cldate', 
            'primarycoil', 'secondarycoil', 'pclass', 'info', 'note']

@require_http_methods(['GET', 'POST'])
def ttnexampleupdateview(request):
    if request.method == 'POST':
        ttneid = request.GET.get('ttneid')
        if ttneid == None: 
            return redirect('../')
        else:
            ttne = TTNExample.objects.get(id = ttneid)
            ttneform = TTNExampleModelForm(request.POST, instance = ttne)
            if ttneform.is_valid():
                ttneform.save()
                return redirect('../' + '?ttneid=' + str(ttneid))
    else: 
        ttneid = request.GET.get('ttneid')
        if ttneid == None: 
            return redirect('../')
        else:
            ttne = TTNExample.objects.get(id = ttneid)
            ttneform = TTNExampleModelForm(instance = ttne)
    context = {}
    context['status'] = ''
    context['contextmenu'] = {'Отменить':'formmethod=GET formaction=../', 'Подтвердить':'formmethod=POST'}
    context['subtitle'] = 'Оборудование: трансформатор: изменение'
    context['form'] = ttneform
    context['ttndir'] = ttne.ttndir
    context['ttneid'] = ttne.id
    return render(request, 'ttnexample_form.html', context = context)
      
@require_http_methods(['GET', 'POST'])
def ttnexamplecreateview(request):
    context = {}
    if request.method == 'POST':
        ttneform = TTNExampleModelForm(request.POST)
        if ttneform.is_valid():
            ttne = ttneform.save(commit = False)
            ttndirid = request.POST.get('ttndirid')
            micid = request.session.get('micid')
            if (ttndirid != None) and (ttndirid != ''):
                ttne.ttndir = ATCTTNDirectory.objects.get(id = ttndirid)
                сontext['ttndir'] = ttne.ttndir
            if (micid != None) and (micid != ''):
                ttne.mic = MIC.objects.get(id = micid)
            ttne.save()
            request.session['ttneid'] = ttne.id
            request.session.modified = True
            return redirect('../detail/')
    else: ttneform = TTNExampleModelForm()
    context['status'] = ''
    context['contextmenu'] = {'Отменить':'formmethod=GET formaction=../', 'Подтвердить':'formmethod=POST'}
    context['subtitle'] = 'Оборудование: трансформатор: создание'
    context['form'] = ttneform
    return render(request, 'ttnexample_form.html', context = context)
     
@require_http_methods(['GET', 'POST'])
def ttnexamplecopyview(request):
    if request.method == 'POST':
        ttneform = TTNExampleModelForm(request.POST)
        if ttneform.is_valid():
            ttne = ttneform.save(commit = False)
            micid = request.session.get('micid')
            if micid != None: ttne.mic = MIC.objects.get(id = micid)
            ttne.save()
            request.session['ttneid'] = ttne.id
            request.session.modified = True
            return redirect('../')
    else:
        ttneid = request.GET.get('ttneid')
        if ttneid == None: 
            return redirect('../')
        else:
            ttne = TTNExample.objects.get(id = ttneid)
            ttne.id = None
            ttneform = TTNExampleModelForm(instance = ttne)
            if ttneform.is_valid():
                ttneform.save()
                return redirect('../' + '?ttneid=' + str(ttneid))
        ttneform = TTNExampleModelForm(instance = ttne)
        context = {}
        context['status'] = ''
        context['contextmenu'] = {'Отменить':'formmethod=GET formaction=../', 'Подтвердить':'formmethod=POST'}
        context['subtitle'] = 'Оборудование: трансформатор: изменение'
        context['form'] = ttneform
        context['ttndir'] = ttne.ttndir
        context['ttneid'] = ttne.id
        return render(request, 'ttnexample_form.html', context = context)
     

