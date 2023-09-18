import os
from django.shortcuts import render, redirect
from django import forms
from django.core import validators
from django.forms import ModelForm, HiddenInput
from django.views.decorators.http import require_http_methods

from einst.models import EInst
from einst.views import EInstListView
from channel.models import Channel
from ttnexample.models import TTNExample

from mic.models import MIC
from esadbsrv.viewmods.viewcommon import CompleteListView
from ttnexample.views import TTNExampleListView
from meter.views import MeterListView
from channel.views import ChannelListView

class EInstSelectView(EInstListView):
    contextmenu = {'Выбрать': 'formmethod=GET formaction=select/',
        'Вернуться':'formaction=../'}

@require_http_methods(['GET'])
def einstselect(request):
    mic = MIC.objects.get(id = request.session.get('micid'))
    mic.einst = EInst.objects.get(id = request.GET.get('einstid'))
    mic.save()
    return redirect('../../')

@require_http_methods(['GET'])
def channelselect(request):
    mic = MIC.objects.get(id = request.session.get('micid'))
    mic.channels.add(Channel.objects.get(id = request.GET.get('channelid')))
    mic.save()
    return redirect('../../')

class MICListView(CompleteListView):
    model = MIC
    template_name = 'mic_list.html'
    paginate_by = 10
    ordering = ['einst', 'name']
    subtitle = 'ИИК'
    contextmenu = {'Создать': 'formmethod=GET formaction=create/',
        'Просмотреть/Изменить': 'formmethod=GET formaction=detail/',
        'Удалить': 'formmethod=GET formaction=delete/',
        'Вернуться': 'formmethod=GET formaction=../'}
    filterkeylist = {'Наименование':'name', 'Код АТС':'code'}
    is_filtered = True
    def get_queryset(self):
        einstid = self.request.session.get('einstid')
        if (einstid != None) and (einstid != ''):
            einst = EInst.objects.get(id = einstid)
            miclist = einst.mic_set.all()
            if miclist != None:
                return miclist
        return super().get_queryset()

class EInstMICListView(CompleteListView):
    model = MIC
    template_name = 'mic_list.html'
    ordering = ['einst', 'name']
    subtitle = 'ИИК'
    contextmenu = {'Создать': 'formmethod=GET formaction=create/',
        'Просмотреть/Изменить': 'formmethod=GET formaction=detail/',
        'Удалить': 'formmethod=GET formaction=delete/',
        'Вернуться': 'formmethod=GET formaction=../'}
    is_filtered = False
    
    def get_queryset(self):
        einstid = self.request.session.get('einstid')
        if (einstid != None) and (einstid != ''):
            einst = EInst.objects.get(id = einstid)
            miclist = einst.mic_set.all()
            if miclist != None:
                return miclist
        return super().get_queryset()

class MICChoiceView(EInstMICListView):
    contextmenu = {'Выбрать': 'formmethod=GET formaction=select/',
        'Вернуться': 'formmethod=GET formaction=../'}

@require_http_methods(['GET'])
def micdetailview(request):
    micid = request.GET.get('micid')
    if micid == None: micid = request.session.get('micid')
    if micid == None: return redirect('../')
    mic = MIC.objects.get(id = micid)
    request.session['micid'] = mic.pk
    request.session.modified = True
    context = {'status':'', 'mic':mic, 'dsownerclass': mic.__class__.__name__,
        'contextmenu':{'Объект': 'formmethod=GET formaction=einst/',
            'Параметры': 'formmethod=GET formaction=update/',
            'Трансформаторы': 'formmethod=GET formaction=ttnexample/',
            'Счетчики': 'formmethod=GET formaction=meter/',
#            'Каналы связи': 'formmethod=GET formaction=channel/',
            'Документы': 'formmethod=GET formaction=docs/',
            'Вернуться': 'formmethod=GET formaction=../'}, 
        'subtitle':'ИИК: просмотр'}
    return render(request, 'mic_detail.html', context = context)
    
def micdeleteview(request):
    if request.method == 'GET':
        micid = request.GET.get('micid')
        if micid == None: micid = request.session.get('micid')
        if micid != None:
            context = {'status': '', 'mic': MIC.objects.get(id = micid),
                'contextmenu':{'Отменить':'formmethod=GET formaction=../', 'Удалить': 'formmethod=POST'}, 
                'subtitle':'ИИК: удаление'}
            return render(request, 'mic_confirm_delete.html', context = context)
    else: 
        micid = request.GET.get('micid')
        if micid != None:
            MIC.objects.filter(id = micid).delete()
    return redirect('../')

class MICModelForm(forms.ModelForm):
    class Meta:
        model = MIC
        fields = ['name', 
            'code',
            'schnum', 
            'info', 
            'note']

def micupdateview(request):
    if request.method == 'POST':
        micid = request.POST.get('micid')
        if micid == None: micid = request.session.get('micid')
        if micid == None: 
            return redirect('../')
        else:
            mic = MIC.objects.get(id = micid)
            micform = MICModelForm(request.POST, instance = mic)
            if micform.is_valid():
                micform.save()
                return redirect('../' + '?micid=' + str(micid))
    else: 
        micid = request.GET.get('micid')
        if micid == None: 
            return redirect('../')
        mic = MIC.objects.get(id = micid)
        micform = MICModelForm(instance = mic)
    context = {}
    context['status'] = ''
    context['contextmenu'] = {'Отменить':'formmethod=GET formaction=../', 'Подтвердить':'formmethod=POST'}
    context['subtitle'] = 'ИИК: изменение'
    context['form'] = micform
    context['einst'] = mic.einst
    context['micid'] = mic.id
    return render(request, 'mic_form.html', context = context)
      
def miccreateview(request):
    if request.method == 'POST':
        micform = MICModelForm(request.POST)
        if micform.is_valid():
            mic = micform.save(commit = False)
            einstid = request.session.get('einstid')
            if einstid !=None: mic.einst = EInst.objects.get(id = einstid)
            mic.save()
            request.session['micid'] = mic.pk
            request.session.modified = True
            return redirect('../detail/' + '?micid=' + str(mic.id))
    else: 
        micform = MICModelForm()
    context = {}
    context['status'] = ''
    context['contextmenu'] = {'Отменить':'formmethod=GET formaction=../../', 'Подтвердить':'formmethod=POST'}
    context['subtitle'] = 'ИИК: создание'
    context['form'] = micform
    return render(request, 'mic_form.html', context = context)

class TTNListView(TTNExampleListView):
    is_filtered = False

    def get_queryset(self):
        micid = self.request.session.get('micid')
        if (micid != None) and (micid != ''):
            mic = MIC.objects.get(id = micid)
            ttnlist = mic.ttnexample_set.all()
            if ttnlist != None:
                return ttnlist
        return super().get_queryset()

class MtrListView(MeterListView):
    is_filtered = False

    def get_queryset(self):
        micid = self.request.session.get('micid')
        if (micid != None) and (micid != ''):
            mic = MIC.objects.get(id = micid)
            meterlist = mic.meter_set.all()
            if meterlist != None:
                return meterlist
        return super().get_queryset()

class CHNListView(ChannelListView):
    is_filtered = False
    contextmenu = {'Добавить': 'formmethod=GET formaction=add/', 
        'Просмотреть': 'formmethod=GET formaction=detail/',
        'Удалить': 'formmethod=GET formaction=delete/',
        'Вернуться': 'formmethod=GET formaction=../'}

    def get_queryset(self):
        micid = self.request.session.get('micid')
        if (micid != None) and (micid != ''):
            mic = MIC.objects.get(id = micid)
            chnlist = mic.channels.all()
            if chnlist != None:
                return chnlist
        return super().get_queryset()

