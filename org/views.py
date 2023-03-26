from django.shortcuts import render, redirect
from django import forms
from django.forms import ModelForm
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from org.models import Organization
from esadbsrv.viewmods.viewcommon import CompleteListView

class OrganizationListView(CompleteListView):
    model = Organization
    template_name = 'organization_list.html'
    paginate_by = 10
    ordering = 'name'
    subtitle = 'Организации'
    filterkeylist = {'':''}
    is_filtered = False
    contextmenu = {'Добавить': 'formmethod=GET formaction=create/', 
        'Просмотреть/Изменить': 'formmethod=GET formaction=detail/',
        'Удалить': 'formmethod=GET formaction=delete/',
        'Вернуться': 'formmethod=GET formaction=../'}

class OrganizationChoiceView(OrganizationListView):
    subtitle = 'Объекты: выбрать владельца'
    contextmenu = {'Выбрать': 'formmethod=GET formaction=select/',
        'Отменить': 'formmethod=GET formaction=../'}

def organizationdetailview(request):
    if request.method == 'GET':
        orgid = request.GET.get('orgid')
        if orgid == None: 
            orgid = request.session.get('orgid')
        if orgid == None: 
            return redirect('../')
        org = Organization.objects.get(id = orgid)
        request.session['orgid'] = org.pk
        request.session.modified = True
        context = {'status':'', 'organization':org, 'ownerclass': org.__class__.__name__,
            'contextmenu':{'Вернуться':'formmethod=GET formaction=../', 
                'Изменить': 'formmethod=GET formaction=update/',
                'Контакты': 'formmethod=GET formaction=contacts/',
                'Документы': 'formmethod=GET formaction=docs/',},
#                'Объекты':'formmethod=GET formaction=einst/'}, 
            'subtitle':'Организация: просмотр'}
        return render(request, 'organization_detail.html', context = context)
    else:
        return redirect('../')

class OrganizationModelForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ['name', 'inn', 'addr', 'req', 'contactinfo', 'info', 'note']

def organizationcreateview(request):
    if request.method == 'POST':
        orgform = OrganizationModelForm(request.POST)
        if orgform.is_valid():
            org = orgform.save()
            request.session['orgid'] = org.pk
            request.session.modified = True
            return redirect('../detail/' + '?orgid='+ str(org.id))
    else: orgform = OrganizationModelForm()
    context = {}
    context['status'] = ''
    context['contextmenu'] = {'Отменить':'formmethod=GET formaction=../', 'Подтвердить':'formmethod=POST'}
    context['subtitle'] = 'Организация: создание'
    context['form'] = orgform
    return render(request, 'organization_form.html', context = context)

def organizationupdateview(request):
    if request.method == 'POST':
        orgid = request.POST.get('orgid')
        if orgid == None:
            return redirect('../')
        else:
            org = Organization.objects.get(id = orgid)
            orgform = OrganizationModelForm(request.POST, instance = org)
            if orgform.is_valid():
                org = orgform.save(commit = True)
                return redirect('../' + '?orgid='+ str(org.id))
    else: 
        orgid = request.GET.get('orgid')
        if orgid == None:
            return redirect('../')
        else:
            org = Organization.objects.get(id = orgid)
            orgform = OrganizationModelForm(instance = org)
    context = {}
    context['status'] = ''
    context['contextmenu'] = {'Отменить':'formmethod=GET formaction=../', 'Подтвердить':'formmethod=POST'}
    context['subtitle'] = 'Организация: создание'
    context['form'] = orgform
    context['orgid'] = orgid
    return render(request, 'organization_form.html', context = context)

def organizationdeleteview(request):
    if request.method == 'GET':
        orgid = request.GET.get('orgid')
        if orgid == None: orgid = request.session.get('orgid')
        if orgid != None:
            Organization.objects.filter(id = orgid).delete()
    return redirect('../')

