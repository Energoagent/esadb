from django.shortcuts import render, redirect
from django import forms
from django.views import generic
from django.views.decorators.http import require_http_methods

from esadbsrv.viewmods.viewcommon import CompleteListView
from channel.models import Channel
from channel.utils import channel_import
from einst.models import EInst

class ChannelListView(CompleteListView):
    model = Channel
    template_name = 'channel_list.html'
    paginate_by = 10
    ordering = 'name'
    subtitle = 'Каналы связи'
    filterkeylist = {'Наименование':'name', 'Тип':'chtype', 'Идентификатор':'ccid'}
    is_filtered = True
    contextmenu = {
    'Добавить': 'formmethod=GET formaction=create/', 
        'Выбрать': 'formmethod=GET formaction=select/',            
        'Просмотреть': 'formmethod=GET formaction=detail/',
        'Добавить': 'formmethod=GET formaction=create/',
        'Выбрать из базы': 'formmethod=GET formaction=frombase/',
        'Исключить': 'formmethod=GET formaction=exclude/',
#        'Удалить': 'formmethod=GET formaction=delete/',
        'Вернуться': 'formmethod=GET formaction=../'
        }
    def get_queryset(self):
        chownerid = self.request.GET.get('chownerid')
        if chownerid == None: chownerid = self.request.session.get('chownerid')
        chownerclassname = self.request.GET.get('chownerclass')
        if chownerclassname == None: 
            chownerclassname = self.request.session.get('chownerclass')
            if (chownerclassname == None) or (chownerclassname == ''): return super().get_queryset()
        chowner = eval(chownerclassname + '.objects.get(id = chownerid)')
        if chowner == None: return super().get_queryset()
        self.request.session['chownerclass'] = chownerclassname
        self.request.session['chownerid'] = chowner.id
        self.request.session.modified = True
        return chowner.channels.all()

class ChannelBaseView(CompleteListView):
    model = Channel
    template_name = 'channel_list.html'
    paginate_by = 10
    ordering = 'name'
    subtitle = 'Каналы связи'
    is_filtered = False
#    filterkeylist = {'Тип/Модель':'cddir'} фильтрация не работает
    contextmenu = {
        'Выбрать': 'formmethod=GET formaction=select/',            
        'Вернуться': 'formmethod=GET formaction=../'
        }

        
class ChannelSelectView(ChannelListView):
    contextmenu = {'Выбрать': 'formmethod=GET formaction=select/', 
        'Вернуться': 'formmethod=GET formaction=../'}

@require_http_methods(['GET'])
def channeldetailview(request):
    channelid = request.GET.get('channelid')
    if channelid == None: 
        channelid = request.session.get('channelid')
    if channelid == None: 
        return redirect('../')
    channel = Channel.objects.get(id = channelid)
    request.session['channelid'] = channel.pk
    request.session.modified = True
    context = {'status':'', 'channel': channel, 'ownerclass': channel.__class__.__name__,
        'contextmenu':{'Вернуться':'formmethod=GET formaction=../',
            'Изменить': 'formmethod=GET formaction=update/',
            'Документы':'formmethod=GET formaction=docs/'},
        'subtitle':'Каналы связи: просмотр'}
    return render(request, 'channel_detail.html', context = context)

class ChannelModelForm(forms.ModelForm):
    class Meta:
        model = Channel
        fields = ['name', 'bl','chtype', 'ccid', 'number', 'ip', 'operator', 'config','info', 'note']

@require_http_methods(['GET', 'POST'])
def channelcreateview(request):
    if request.method == 'POST':
        chform = ChannelModelForm(request.POST)
        if chform.is_valid():
            channel = chform.save(commit = False)
            channel.save()
            chownerid = request.session.get('chownerid')
            chownerclassname = request.session.get('chownerclass')
            if chownerclassname != None:
                chowner = eval(chownerclassname + '.objects.get(id = chownerid)')
                if chowner != None:
                    chowner.channels.add(channel)
            request.session['channelid'] = channel.pk
            request.session.modified = True
            return redirect('../detail/')
        else:
            chform = ChannelModelForm(request.POST)
    else: 
        chform = ChannelModelForm()
        context = {'status': '',
            'contextmenu': {'Отменить':'formmethod=GET formaction=../../', 'Подтвердить':'formmethod=POST'},
            'subtitle': 'Каналы связи: создание'}
        context['form'] = chform
    return render(request, 'channel_form.html', context = context)

@require_http_methods(['GET', 'POST'])
def channelupdateview(request):
    if request.method == 'GET':
        channelid = request.GET.get('channelid')
        if channelid != None:
            channel = Channel.objects.get(id = channelid)
        else:
            return redirect('../')
        chform = ChannelModelForm(instance = channel)
    else:
        channelid = request.POST.get('channelid')
        channel = Channel.objects.get(id = channelid)
        chform = ChannelModelForm(request.POST, instance = channel)
        if chform.is_valid(): channel.save()
        return redirect('../')
    context = {'status':'',
        'contextmenu':{'Сохранить': 'formmethod=POST', 'Вернуться':'formmethod=GET formaction=../'}, 
        'subtitle':'Каналы связи: изменить'}
    context['form'] = chform
    context['channelid'] = channelid
    return render(request, 'channel_form.html', context = context)

@require_http_methods(['GET'])
def channeldeleteview(request):
    channelid = request.GET.get('channelid')
    if channelid != None:
        Channel.objects.filter(id = channelid).delete()
    return redirect('../')

@require_http_methods(['GET'])
def channelexcludeview(request):
    channelid = request.GET.get('channelid')
    if channelid != None:
        einstid = request.session.get('einstid')
        if einstid != None:
            einst = EInst.objects.get(id = einstid)
            if einst != None:
                einst.channels.remove(Channel.objects.get(id = channelid))
    return redirect('../../')


@require_http_methods(['GET'])
def chimportview(request):
    channel_import()
    return redirect('../')

@require_http_methods(['GET'])
def channelselecteview(request):    
    channelid = request.GET.get('channelid')
    if channelid != None:
        einstid = request.session.get('einstid')
        if einstid != None:
            einst = EInst.objects.get(id = einstid)
            if einst != None:
                einst.channels.add(Channel.objects.get(id = channelid))
    return redirect('../../')
