import os
from django.shortcuts import render, redirect
from django import forms
from django.core import validators
from django.forms import ModelForm, HiddenInput
from django.urls import reverse_lazy, reverse
from pathlib import Path
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.decorators.http import require_http_methods

from meter.models import Meter
from mic.models import MIC
from esadbsrv.models import ATCMeterDir
from albumstore.models import albumpath, ALBUM_DIR
from esadbsrv.viewmods.viewcommon import CompleteListView
from esadbsrv.viewmods.viewatcmeterdir import ATCMeterDirListView

class MeterListView(CompleteListView):
    model = Meter
    template_name = 'meter_list.html'
    paginate_by = 10
    ordering = 'mtrdir'
    subtitle = 'Оборудование: счетчики'
    contextmenu = {'Просмотреть/Изменить': 'formmethod=GET formaction=detail/',
        'Добавить': 'formmethod=GET formaction=create/',
        'Удалить': 'formmethod=GET formaction=delete/',
        'Копировать': 'formmethod=GET formaction=copy/',
        'Вернуться': 'formmethod=GET formaction=../'}
    filterkeylist = {'Серийный номер':'sn', 'Модель':'mtrmodel', 'Изготовитель':'fabric', 'номер в ГРСИ':''}
    is_filtered = True
    def get_queryset(self):
        micid = self.request.GET.get('micid')
        if micid == None: micid = self.request.request.get('micid')
        if micid == None:
            return super().get_queryset()
        else:
            return Meter.objects.filter(mic = micid)
    
@require_http_methods(['GET'])
def meterdetailview(request):
    meterid = request.GET.get('meterid')
    if meterid == None: meterid = request.session.get('meterid')
    if meterid == None: return redirect('../')
    meter = Meter.objects.get(id = meterid)
    request.session['meterid'] = meter.pk
    request.session.modified = True
    context = {'status':'', 'meter':meter, 'dsownerclass': meter.__class__.__name__,
        'contextmenu':{'Изменить модель': 'formmethod=GET formaction=meterdirchoice/', 
            'Параметры': 'formmethod=GET formaction=update/',
            'Документы': 'formmethod=GET formaction=docs/',
            'Вернуться':'formmethod=GET formaction=../'}, 
        'subtitle':'Оборудование: счетчики: просмотр'}
    context['albumpath'] = ALBUM_DIR
    return render(request, 'meter_detail.html', context = context)
    
@require_http_methods(['GET'])
def meterdeleteview(request):
    meterid = request.GET.get('meterid')
    if meterid == None: meterid = request.session.get('meterid')
    if meterid != None: Meter.objects.filter(id = meterid).delete()
    return redirect('../')
        
class ATCMeterDirChoiceView(ATCMeterDirListView):
    subtitle = 'Оборудование: счетчики: выбор модели из справочника АТС'
    contextmenu = {'Выбрать': 'formmethod=GET formaction=select/',
        'Отменить': 'formmethod=GET formaction=../'}

@require_http_methods(['GET'])
def directorychoiceselect(request):
    meterid = request.GET.get('meterid')
    if meterid == None: 
        meterid = request.session.get('meterid')
    if meterid != None:
        mdid = request.GET.get('mdid')
        if mdid != None:
            meter = Meter.objects.get(id = meterid)
            meter.mtrdir = ATCMeterDir.objects.get(id = mdid)
            meter.save()
    return redirect('../../')

class MeterModelForm(forms.ModelForm):
    class Meta:
        model = Meter
        fields = ['bl', 'mtrmodel', 'sn', 'fbdate', 'cldate', 
            'classae', 'classre', 'channelae', 'channelre', 'info', 'note']

@require_http_methods(['GET', 'POST'])
def meterupdateview(request):
    if request.method == 'POST':
        meterid = request.POST.get('meterid')
        if meterid == None:
            return redirect('../')
        else:
            meter = Meter.objects.get(id = meterid)
            meterform = MeterModelForm(request.POST, instance = meter)
            if meterform.is_valid():
                meterform.save()
                return redirect('../' + '?meterid=' + str(meterid))
    else:
        meterid = request.GET.get('meterid')
        if meterid == None: 
            return redirect('../')
        else:
            meter = Meter.objects.get(id = meterid)
        meterform = MeterModelForm(instance = meter)
        context = {}
        context['status'] = ''
        context['contextmenu'] = {'Отменить':'formmethod=GET formaction=../', 'Подтвердить':'formmethod=POST'}
        context['subtitle'] = 'Оборудование: счетчики: изменение'
        context['form'] = meterform
        context['meterdir'] = meter.mtrdir
        context['meterid'] = meter.id
        return render(request, 'meter_form.html', context = context)
      
def metercreateview(request):
    context = {}
    if request.method == 'POST':
        meterform = MeterModelForm(request.POST)
        if meterform.is_valid():
            meter = meterform.save(commit = False)
            mdid = request.POST.get('mdid')
            micid = request.session.get('micid')
            if (mdid != None) and (mdid != ''):
                meter.ttndir = ATCMeterDir.objects.get(id = mdid)
                сontext['meterdir'] = meter.mtrdir
            if (micid != None) and (micid != ''):
                meter.mic = MIC.objects.get(id = micid)
            meter.save()
            request.session['meterid'] = meter.id
            request.session.modified = True
            return redirect('../detail/')
    else: meterform = MeterModelForm()
    context['status'] = ''
    context['contextmenu'] = {'Отменить':'formmethod=GET formaction=../', 'Подтвердить':'formmethod=POST'}
    context['subtitle'] = 'Оборудование: счетчики: создание'
    context['form'] = meterform
    return render(request, 'meter_form.html', context = context)
     
def metercopyview(request):
    if request.method == 'POST':
        meterform = MeterModelForm(request.POST)
        if meterform.is_valid():
            meter = meterform.save(commit = False)
            mdid = request.POST.get('mdid')
            if ttndirid != None:
                meter.mtrdir = ATCMeterDir.objects.get(id = mdid)
                meter.save()
            request.session['meterid'] = meter.id
            request.session.modified = True
            return redirect('../')
    else:
        meterid = requestget(request, 'meterid')
        if meterid == None: 
            return redirect('../')
        else:
            meter = Meter.objects.get(id = meterid)
            meter.id = None
            meterform = MeterModelForm(instance = meter)
            if meterform.is_valid():
                meterform.save()
                return redirect('../' + '?meterid=' + str(meterid))
        meterform = MeterModelForm(instance = meter)
        context = {}
        context['status'] = ''
        context['contextmenu'] = {'Отменить':'formmethod=GET formaction=../', 'Подтвердить':'formmethod=POST'}
        context['subtitle'] = 'Оборудование: счетчики: копирование'
        context['form'] = meterform
        context['ttndir'] = meter.meteratcdirectoryrow
        context['meterid'] = meter.id
        return render(request, 'meter_form.html', context = context)
     

