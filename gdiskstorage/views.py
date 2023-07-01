import os
import io

# Django modules
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.forms import ModelForm

# Google drive API modules
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload

# other modules
from random import choice
from string import digits
from PIL import Image

# ESADB modules
from esadbsrv.viewmods.viewcommon import CompleteListView
from gdiskstorage.models import GDiskFolder, GDISK_PATH
from esadb.settings import BASE_DIR

# If modifying these scopes, delete the file token.json.
#SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']
SCOPES = ['https://www.googleapis.com/auth/drive.metadata',
          'https://www.googleapis.com/auth/drive',
          'https://www.googleapis.com/auth/drive.file'
          ]

# Google drive service open and return
def gdrive_open():
    status = None
    creds = None
    home_dir = os.path.expanduser('~')
    credential_path = os.path.join(home_dir,'client_secret_esadb.json')
    token_path = os.path.join(home_dir,'token_esadb.json')
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
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
        service = build('drive', 'v3', credentials=creds)
    except HttpError as status: pass
    return {'service': service, 'status': status}

@require_http_methods(['GET'])
def gdisk_list(request):
    srv = gdrive_open()
    if srv['status'] == None:
        # Call the Drive v3 API
        results = srv['service'].files().list(fields="files(id, name)").execute()
        items = results.get('files', [])
        context = {'filelist': items}
    else:
        context = {'status': srv['status']}
    return render(request, 'gdisk_list.html', context = context)

class GDiskFolderListView(CompleteListView):
    model = GDiskFolder
    paginate_by = 10
    ordering = 'name'
    template_name = 'gdiskfolder_list.html'
    subtitle = 'Медиа: альбомы изображений'
    contextmenu = {
        'Изображения': 'formmethod=GET formaction=detail/',
        'Изменить': 'formmethod=GET formaction=update/',
        'Добавить': 'formmethod=GET formaction=create/',
        'Удалить': 'formmethod=GET formaction=delete/',
        'Вернуться': 'formmethod=GET formaction=../'}
    filterkeylist = {'Наименование':'name', 'Дата': 'date', 'Информация':'info'}
    is_filtered = True
    def get_queryset(self):
        ownerid = self.request.GET.get('ownerid')
        if ownerid == None: ownerid = self.request.session.get('ownerid')
        ownerclass = self.request.GET.get('ownerclass')
        if ownerclass == None: ownerclass = self.request.session.get('ownerclass')
        if (ownerclass == None) or (ownerid == None): return super().get_queryset()
        owner = eval(ownerclass + '.objects.get(id = ownerid)')
        if owner == None: return super().get_queryset()
        self.request.session['ownerclass'] = ownerclass
        self.request.session['ownerid'] = owner.id
        self.request.session.modified = True
        return owner.albums.all()
        
class GDiskFolderModelForm(ModelForm):
    class Meta:
        model = GDiskFolder
        fields = ['name', 'info', 'note']

        
@require_http_methods(['GET', 'POST'])
def gdiskfolder_create(request):
    if request.method == 'POST':
        folderform = GDiskFolderModelForm(request.POST)
        if folderform.is_valid():
            folder = folderform.save(commit = False)
            folder.folder = ''.join(choice(digits) for i in range(12))
            folder.save()
            ownerid = request.session.get('ownerid')
            ownerclassname = request.session.get('ownerclass')
            if ownerclassname != None:
                owner = eval(ownerclassname + '.objects.get(id = ownerid)')
                if owner != None: owner.albums.add(folder)
#            remotedir = os.path.join(GDISK_PATH, folder.folder)
# google drive
            srv = gdrive_open()
            if srv['status'] == None:
# Call the Drive v3 API
                folder_metadata = {'name': folder.folder, 'parents': [],
                    'mimeType': 'application/vnd.google-apps.folder'}
                create_folder = srv['service'].files().create(body=folder_metadata, fields='id').execute()
                folder_id = create_folder.get('id', [])
                print('FLD_ID:', folder_id)
            return redirect('../')
    else: 
        folderform = GDiskFolderModelForm()
    context = {}
    context['status'] = ''
    context['contextmenu'] = {'Отменить':'formmethod=GET formaction=../', 'Подтвердить':'formmethod=POST'}
    context['subtitle'] = 'Медиа: альбомы изображений: создание'
    context['form'] = folderform
    return render(request, 'gdiskfolder_form.html', context = context)

@require_http_methods(['GET', 'POST'])
def gdiskfolder_update(request):
    if request.method == 'POST':
        folderid = request.session.get('albumid')
        if folderid != None: 
            folderform = GDiskFolderModelForm(request.POST, instance = GDiskFolder.objects.get(id = folderid))
            if folderform.is_valid():
                folder = folderform.save()
        return redirect('../')
    else: 
        folderid = request.GET.get('albumid')
        if folderid != None: 
            folderform = GDiskFolderModelForm(instance = GDiskFolder.objects.get(id = folderid))
        else:
            return redirect('../')
        request.session['albumid'] = folderid
        request.session.modified = True
    context = {'form': folderform,
        'contextmenu': {'Отменить':'formmethod=GET formaction=../', 'Подтвердить':'formmethod=POST'},
        'subtitle': 'Медиа: альбомы изображений: создание'}
    return render(request, 'gdiskfolder_form.html', context = context)

@require_http_methods(['GET', 'POST'])
def gdiskfolder_delete(request):
    if request.method == 'GET':
        folderid = request.GET.get('albumid')
        if folderid == None: folderid = request.session.get('albumid')
        if folderid != None:
            context = {'folder': GDiskFolder.objects.get(id = folderid),
                'contextmenu':{'Отменить':'formmethod=GET formaction=../', 'Удалить': 'formmethod=POST'}, 
                'subtitle':'Медиа: альбомы изображений: удаление'}
            return render(request, 'gdiskfolder_confirm_delete.html', context = context)
    else: 
        folderid = request.POST.get('albumid')
        if folderid != None:
            GDiskFolder.objects.filter(id = folderid).delete()
    return redirect('../')

@require_http_methods(['GET'])
def gdiskfolder_detail(request):
    folderid = request.GET.get('albumid')
    if folderid == None: 
        folderid = request.session.get('albumid')
    if folderid == None: 
        return redirect('../')
    folder = GDiskFolder.objects.get(id = folderid)
    request.session['albumid'] = folder.pk
    request.session.modified = True
    srv = gdrive_open()
    if srv['status'] == None:
#        info = srv['service'].about().get()
#        print('-->', type(info))
        # Call the Drive v3 API
        results = srv['service'].files().list(fields="files(id, name)").execute()
        items = results.get('files', [])
    context = {'status': srv['status'], 'folder': folder, 'filelist': items,
        'contextmenu':{'Скачать': 'formmethod=GET formaction=downloadimage',
            'Загрузить': 'formmethod=GET formaction=loadimage',
            'Удалить': 'formmethod=GET formaction=deleteimage',
            'Вернуться': 'formmethod=GET formaction=../'},
        'subtitle':'Медиа: альбомы изображений: просмотр'}
    return render(request, 'gdiskfolder_detail.html', context = context)

@require_http_methods(['GET'])
def gdiskfolder_downloadimage(request):
    srv = gdrive_open()
    if srv['status'] == None:
        for item in request.GET.getlist('imgid'):
            file_id, file_name = item.split(':')
            if file_id != None:
                request  = srv['service'].files().get_media(fileId = file_id)
                file_io = io.FileIO(os.path.join(BASE_DIR, 'export', file_name), 'wb')
                downloader = MediaIoBaseDownload(file_io, request)
                done = False
                while done is False:
                    status, done = downloader.next_chunk()
    return redirect('../')


