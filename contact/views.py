import os.path

# import google API
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/contacts.readonly']

# django modules
from django.shortcuts import render, redirect
from django import forms
from django.views.decorators.http import require_http_methods

# ESADB modules
from esadbsrv.viewmods.viewcommon import CompleteListView
from contact.models import Contact
from org.models import Organization
from einst.models import EInst
from project.models import Project


class ContactListView(CompleteListView):
    model = Contact
    template_name = 'contact_list.html'
    paginate_by = 10
    ordering = 'name'
    subtitle = 'Контакты'
    filterkeylist = {'ФИО':'name', 'Контакт инфо':'contactinfo'}
    is_filtered = True
    contextmenu = {
        'Добавить': 'formmethod=GET formaction=create/', 
        'Выбрать из справочника': 'formmethod=GET formaction=phonebook/',
#        'Выбрать из google account': 'formmethod=GET formaction=gcontacts/',
        'Просмотреть': 'formmethod=GET formaction=detail/',
        'Удалить': 'formmethod=GET formaction=delete/',
        'Вернуться': 'formmethod=GET formaction=../'}
    def get_queryset(self):
        cntownerid = self.request.GET.get('cntownerid')
        if cntownerid == None: cntownerid = self.request.session.get('cntownerid')
        cntownerclassname = self.request.GET.get('cntownerclass')
        if cntownerclassname == None: 
            cntownerclassname = self.request.session.get('cntownerclass')
            if (cntownerclassname == None) or (cntownerclassname == ''): 
                return super().get_queryset()
        cntowner = eval(cntownerclassname + '.objects.get(id = cntownerid)')
        if cntowner == None: return super().get_queryset()
        self.request.session['cntownerclass'] = cntownerclassname
        self.request.session['cntownerid'] = cntowner.id
        self.request.session.modified = True
        return cntowner.contacts.all()

class PhoneBookView(CompleteListView):
    model = Contact
    template_name = 'contact_list.html'
    paginate_by = 10
    ordering = 'name'
    subtitle = 'Контакты'
    filterkeylist = {'':'', 'ФИО':'name', 'Контакт инфо':'contactinfo'}
    is_filtered = True
    contextmenu = {'Выбрать': 'formmethod=GET formaction=select/',
        'Вернуться': 'formmethod=GET formaction=../'}

@require_http_methods(['GET'])
def contactdetailview(request):
    contactid = request.GET.get('contactid')
    if contactid == None: 
        contactid = request.session.get('contactid')
    if contactid == None: 
        return redirect('../')
    contact = Contact.objects.get(id = contactid)
    request.session['contactid'] = contact.pk
    request.session.modified = True
    context = {'status':'', 'contact': contact, 'ownerclass': contact.__class__.__name__,
        'contextmenu':{
            'Вернуться':'formmethod=GET formaction=../',
            'Изменить': 'formmethod=GET formaction=update/',
            'Документы':'formmethod=GET formaction=docs/'},
        'subtitle':'Контакты: просмотр'}
    return render(request, 'contact_detail.html', context = context)

class ContactModelForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'contactinfo', 'info', 'note']

@require_http_methods(['GET', 'POST'])
def contactcreateview(request):
    if request.method == 'POST':
        cntform = ContactModelForm(request.POST)
        if cntform.is_valid():
            contact = cntform.save(commit = True)
            cntownerid = request.session.get('cntownerid')
            cntownerclassname = request.session.get('cntownerclass')
            if cntownerclassname != None:
                cntowner = eval(cntownerclassname + '.objects.get(id = cntownerid)')
                if cntowner != None:
                    cntowner.contacts.add(contact)
            request.session['contactid'] = contact.pk
            request.session.modified = True
            return redirect('../detail/')
        else:
            cntform = ContactModelForm(request.POST)
    else: 
        cntform = ContactModelForm()
        context = {'status': '',
            'contextmenu': {'Отменить':'formmethod=GET formaction=../../', 'Подтвердить':'formmethod=POST'},
            'subtitle': 'Контакты: создание'}
        context['form'] = cntform
    return render(request, 'contact_form.html', context = context)

@require_http_methods(['GET', 'POST'])
def contactupdateview(request):
    if request.method == 'GET':
        contactid = request.GET.get('contactid')
        if contactid != None:
            contact = Contact.objects.get(id = contactid)
        else:
            return redirect('../')
        cntform = ContactModelForm(instance = contact)
    else:
        contactid = request.POST.get('contactid')
        contact = Contact.objects.get(id = contactid)
        cntform = ContactModelForm(request.POST, instance = contact)
        if cntform.is_valid(): 
            contact.save()
            return redirect('../')
    context = {'status':'',
        'contextmenu':{'Сохранить': 'formmethod=POST', 'Вернуться':'formmethod=GET formaction=../'}, 
        'subtitle':'Контакты: изменить'}
    context['form'] = cntform
    context['contactid'] = contactid
    return render(request, 'contact_form.html', context = context)

@require_http_methods(['GET'])
def contactdeleteview(request):
    contactid = request.GET.get('contactid')
    if contactid != None:
        Contact.objects.filter(id = contactid).delete()
    return redirect('../')
    
@require_http_methods(['GET'])
def contactselectview(request):
    contactid = request.GET.get('contactid')
    if contactid != None:
        cntownerid = request.session.get('cntownerid')
        cntownerclassname = request.session.get('cntownerclass')
        if cntownerclassname != None:
            cntowner = eval(cntownerclassname + '.objects.get(id = cntownerid)')
            if cntowner != None:
                cntowner.contacts.add(Contact.objects.get(id = contactid))
    return redirect('../../')

def gcontacts_open():
    status = None
    creds = None
    home_dir = os.path.expanduser('~')
    credential_path = os.path.join(home_dir,'esadb_client_secret.json')
    token_path = os.path.join(home_dir,'gcontacts_token.json')
# The file token.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first time.
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
# If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credential_path, SCOPES)
            creds = flow.run_local_server(port=0)
# Save the credentials for the next run
        with open(token_path, 'w') as token:
            token.write(creds.to_json())
    try:
        service = build('people', 'v1', credentials=creds)    
    except HttpError as status: pass
    return {'service': service, 'status': status}
    
@require_http_methods(['GET'])
def gcontactsview(request):
    srv = gcontacts_open()
    if srv['status'] == None:
        results = srv['service'].people().connections().list(
            resourceName = 'people/me',
            pageSize = 10,
            personFields = 'names,emailAddresses,phoneNumbers,biographies').execute()
        totalpeople = results.get('totalPeople')
        connections = results.get('connections')
#----------------------------------------------------------
    context = {'status': srv['status'], 'totalpeople': totalpeople, 'connections': connections,
        'contextmenu':{'Вернуться': 'formmethod=GET formaction=../'},
        'subtitle':'Контакты: goole contacts list'}
    return render(request, 'gcontacts_list.html', context = context)

