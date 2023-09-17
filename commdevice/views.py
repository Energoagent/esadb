from django.shortcuts import render
from django import forms
from django.shortcuts import render, redirect
from django.forms import ModelForm
from django.views import generic
from django.views.decorators.http import require_http_methods

from commdevice.models import CommDevice
from commdevice.utils import commdevice_import
from esadbsrv.models import CDDirectory
from esadbsrv.viewmods.viewcommon import CompleteListView
from esadbsrv.viewmods.viewcddir import CDDirectoryListView
from einst.models import EInst

class CDDirectoryChoiceView(CDDirectoryListView):
    contextmenu = {'Выбрать':'formmethod=GET formaction=select/',
        'Вернуться': 'formmethod=GET formaction=../'}

class CommDeviceListView(CompleteListView):
    model = CommDevice
    template_name = 'commdevice_list.html'
    paginate_by = 10
    ordering = 'cddir'
    subtitle = 'Оборудование: устройства связи'
    is_filtered = False
#    filterkeylist = {'Тип/Модель':'cddir'} фильтрация не работает
    contextmenu = {
        'Выбрать': 'formmethod=GET formaction=select/',            
        'Просмотреть/Изменить': 'formmethod=GET formaction=detail/',
        'Добавить': 'formmethod=GET formaction=create/',
        'Выбрать из базы': 'formmethod=GET formaction=frombase/',
        'Исключить': 'formmethod=GET formaction=exclude/',
#        'Удалить': 'formmethod=GET formaction=delete/',
        'Вернуться': 'formmethod=GET formaction=../'
        }
    def get_queryset(self):
        einstid = self.request.GET.get('einstid')
        if einstid == None: einstid = self.request.session.get('einstid')
        if einstid == None:
            return super().get_queryset()
        else:
            return CommDevice.objects.filter(einst = einstid)

class CommDeviceBaseView(CompleteListView):
    model = CommDevice
    template_name = 'commdevice_list.html'
    paginate_by = 10
    ordering = 'cddir'
    subtitle = 'Оборудование: устройства связи'
    is_filtered = False
#    filterkeylist = {'Тип/Модель':'cddir'} фильтрация не работает
    contextmenu = {
        'Выбрать': 'formmethod=GET formaction=select/',            
        'Вернуться': 'formmethod=GET formaction=../'
        }

#class CommDeviceChoiceView(CommDeviceListView):
#    contextmenu = {'Выбрать':'formmethod=GET formaction=../select/',
#        'Просмотреть/Изменить': 'formmethod=GET formaction=detail/',
#        'Добавить':'formmethod=GET formaction=create/',
#        'Удалить': 'formmethod=GET formaction=delete/',
#        'Вернуться': 'formmethod=GET formaction=../'}
#    subtitle = 'Оборудование: добавить устройство связи: выбрать модель из справочника'

class CommDeviceModelForm(forms.ModelForm):
    class Meta:
        model = CommDevice
        fields = ['bl', 'cdmodel', 'sn', 'fbdate', 'addrtype', 'addr', 'config', 'info', 'note']
   
@require_http_methods(['GET', 'POST'])
def commdevicecreateview(request):
    if request.method == 'POST':
        cdform = CommDeviceModelForm(request.POST)
        if cdform.is_valid():
            commdevice = cdform.save(commit = True)
            einstid = request.session.get('einstid')
            if einstid != None:
                EInst.objects.get(id = einstid).commdevices.add(commdevice)
            request.session['cdid'] = commdevice.pk
            request.session.modified = True
            return redirect('../' + 'detail/' + '?cdid='+ str(commdevice.id))
    else: cdform = CommDeviceModelForm()
    context = {}
    context['status'] = ''
    context['contextmenu'] = {'Отменить':'formmethod=GET formaction=../../', 'Подтвердить':'formmethod=POST'}
    context['subtitle'] = 'Оборудование: устройство связи: создание'
    context['form'] = cdform
    return render(request, 'commdevice_form.html', context = context)

@require_http_methods(['GET'])
def commdevicedetailview(request):
    cdid = request.GET.get('cdid')
    if cdid == None: cdid = request.session.get('cdid')
    if cdid == None: return redirect('../')
    commdevice = CommDevice.objects.get(id = cdid)
    request.session['cdid'] = commdevice.pk
    request.session.modified = True
    context = {'status':'', 'commdevice':commdevice, 'dsownerclass': commdevice.__class__.__name__,
        'contextmenu':{'Параметры': 'formmethod=GET formaction=update/',
            'Справочник': 'formmethod=GET formaction=cddirchoice/',
            'Документы': 'formmethod=GET formaction=docs/',
            'Вернуться':'formmethod=GET formaction=../'}, 
        'subtitle':'Оборудование: устройства связи: просмотр и изменение'}
    return render(request, 'commdevice_detail.html', context = context)

@require_http_methods(['GET'])
def commdevicedeleteview(request):
    cdid = request.GET.get('cdid')
    if cdid == None: cdid = request.session.get('cdid')
    if cdid != None: CommDevice.objects.filter(id = cdid).delete()
    return redirect('../')

@require_http_methods(['GET'])
def commdeviceexcludeview(request):
    cdid = request.GET.get('cdid')
    if cdid != None:
        einstid = request.session.get('einstid')
        if einstid != None:
            einst = EInst.objects.get(id = einstid)
            if einst != None:
                einst.commdevices.remove(CommDevice.objects.get(id = cdid))
    return redirect('../../')

@require_http_methods(['GET', 'POST'])
def commdeviceupdateview(request):
    if request.method == 'POST':
        cdid = request.POST.get('cdid')
        if cdid == None: 
            return redirect(reverse_lazy('commdevice'))
        else:
            commdevice = CommDevice.objects.get(id = cdid)
            cdform = CommDeviceModelForm(request.POST, instance = commdevice)
            if cdform.is_valid():
                cdform.save()
                return redirect('../' + '?cdid=' + str(commdevice.id))
    else: 
        cdid = request.GET.get('cdid')
        if cdid == None: 
            return redirect(reverse_lazy('commdevice'))
        else:
            commdevice = CommDevice.objects.get(id = cdid)
            cdform = CommDeviceModelForm(instance = commdevice)
    context = {}
    context['contextmenu'] = {'Отменить':'formmethod=GET formaction=../', 'Подтвердить':'formmethod=POST'}
    context['subtitle'] = 'Оборудование: устройство связи: изменение'
    context['form'] = cdform
    context['cddir'] = commdevice.cddir
    context['cdid'] = commdevice.id
    return render(request, 'commdevice_form.html', context = context)
      
@require_http_methods(['GET'])
def cddirchoiceselect(request):
    cdid = request.session.get('cdid')
    if cdid != None:
        commdevice = CommDevice.objects.get(id = cdid)
        cddirid = request.GET.get('cddirid')
        if cddirid != None:
            commdevice.cddir = CDDirectory.objects.get(id = cddirid)
            commdevice.save()
    return redirect('../../')

@require_http_methods(['GET'])
def cdimportview(request):
    commdevice_import()
    return redirect('../')
    
@require_http_methods(['GET'])
def commdeviceselecteview(request):    
    cdid = request.GET.get('cdid')
    if cdid != None:
        einstid = request.session.get('einstid')
        if einstid != None:
            einst = EInst.objects.get(id = einstid)
            if einst != None:
                einst.commdevices.add(CommDevice.objects.get(id = cdid))
    return redirect('../../')
    
       
