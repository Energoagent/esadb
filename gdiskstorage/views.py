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
from googleapiclient.http import MediaIoBaseDownload, MediaInMemoryUpload

# other modules
from random import choice
from string import digits
from PIL import Image

# ESADB modules
from esadbsrv.viewmods.viewcommon import CompleteListView
from gdiskstorage.models import GDiskFolder, GDISK_PATH
from esadb.settings import BASE_DIR

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata',
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/drive.appdata',
    ]

# Google drive service open and return
def gdrive_open():
    status = None
    creds = None
    home_dir = os.path.expanduser('~')
    credential_path = os.path.join(home_dir,'esadb_client_secret.json')
    token_path = os.path.join(home_dir,'esadb_token.json')
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

class GDiskFolderListView(CompleteListView):
    model = GDiskFolder
    paginate_by = 10
    ordering = 'name'
    template_name = 'gdiskfolder_list.html'
    subtitle = 'Медиа: альбомы изображений'
    contextmenu = {
        'Просмотреть': 'formmethod=GET formaction=detail/',
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
# google drive
            srv = gdrive_open()
            if srv['status'] == None:
# get id of google storage
                results = srv['service'].files().list(q = 'name = "gdiskstorage"', fields = 'files(id, name)').execute()
                for item in results.get('files', []): 
                    parent_id = item['id']
                folder_metadata = {'name': folder.folder, 'parents': [parent_id],
                    'mimeType': 'application/vnd.google-apps.folder'}
                create_folder = srv['service'].files().create(body=folder_metadata, fields='id').execute()
                folderid = create_folder.get('id', [])
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
        folderid = request.session.get('folderid')
        if folderid != None: 
            folderform = GDiskFolderModelForm(request.POST, instance = GDiskFolder.objects.get(id = folderid))
            if folderform.is_valid():
                folder = folderform.save()
        return redirect('../')
    else: 
        folderid = request.GET.get('folderid')
        if folderid != None: 
            folderform = GDiskFolderModelForm(instance = GDiskFolder.objects.get(id = folderid))
        else:
            return redirect('../')
        request.session['folderid'] = folderid
        request.session.modified = True
    context = {'form': folderform,
        'contextmenu': {'Отменить':'formmethod=GET formaction=../', 'Подтвердить':'formmethod=POST'},
        'subtitle': 'Медиа: альбомы изображений: создание'}
    return render(request, 'gdiskfolder_form.html', context = context)

@require_http_methods(['GET', 'POST'])
def gdiskfolder_delete(request):
    if request.method == 'GET':
        folderid = request.GET.get('folderid')
        if folderid == None: folderid = request.session.get('folderid')
        if folderid != None:
            context = {'folder': GDiskFolder.objects.get(id = folderid),
                'contextmenu':{'Отменить':'formmethod=GET formaction=../', 'Удалить': 'formmethod=POST'}, 
                'subtitle':'Медиа: альбомы изображений: удаление'}
            return render(request, 'gdiskfolder_confirm_delete.html', context = context)
    else: 
        folderid = request.POST.get('folderid')
        if folderid == None: folderid = request.session.get('folderid')
        if folderid != None:
            folder = GDiskFolder.objects.get(id = folderid)
# google drive
            srv = gdrive_open()
            if srv['status'] == None:
                try:
# get folder id
                    results = srv['service'].files().list(q = ('name = %r and \
                        mimeType = "application/vnd.google-apps.folder"' %folder.folder), 
                        fields = 'files(id, name)').execute()
                    for item in results.get('files', []): 
                        parent_id = item['id']
# delete files
#                    results = srv['service'].files().list(q = ('%r in parents and \
#                        mimeType!="application/vnd.google-apps.folder" and \
#                        trashed != True' %parent_id), fields = 'files(id)').execute()
#                    for item in results.get('files', []):
#                        srv['service'].files().delete(fileId = item['id']).execute()
# delete folder
                    srv['service'].files().delete(fileId = parent_id).execute()
                except BaseException as e: 
                    print('EXEPTION:', e)
                folder.delete()
    return redirect('../')

@require_http_methods(['GET'])
def gdiskfolder_detail(request):
    folderid = request.GET.get('folderid')
    if folderid == None: 
        folderid = request.session.get('folderid')
    if folderid == None: 
        return redirect('../')
    folder = GDiskFolder.objects.get(id = folderid)
    request.session['folderid'] = folder.pk
    request.session.modified = True
    srv = gdrive_open()
    if srv['status'] == None:
        about = srv['service'].about().get(fields = 'user').execute()
# get id of google storage
#        results = srv['service'].files().list(q = 'name = "gdiskstorage"', fields = 'files(id, name)').execute()
#        for item in results.get('files', []): 
#            parent_id = item['id']
# get id of storage folder
        results = srv['service'].files().list(q = ('name = %r and \
            mimeType = "application/vnd.google-apps.folder"' %folder.folder), 
            fields = 'files(id, name, webViewLink)').execute()
        for item in results.get('files', []): 
            parent_id = item['id']
            folder_link = item['webViewLink']
# get files in folder
        results = srv['service'].files().list(q = ('%r in parents and \
            mimeType!="application/vnd.google-apps.folder" and \
            trashed != True' %parent_id), fields = 'files(id, name, webViewLink)').execute()
        items = results.get('files', [])
#----------------------------------------------------------
    context = {'status': srv['status'], 'folder': folder, 'filelist': items, 'about': about, 'folder_link': folder_link, 
        'contextmenu':{'Скачать': 'formmethod=GET formaction=downloadimage',
            'Загрузить': 'formmethod=GET formaction=uploadimage',
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

@require_http_methods(['GET', 'POST'])
def gdiskfolder_uploadimage(request):
    folderid = request.session.get('folderid')
    if folderid == None:
        return redirect('../')
    if request.method == 'POST':
        if request.FILES == None:
            return redirect('../')
        folder = GDiskFolder.objects.get(id = folderid)
        srv = gdrive_open()
        if srv['status'] == None:
            try:
# get id of storage folder
                results = srv['service'].files().list(q = ('name = %r and \
                    mimeType = "application/vnd.google-apps.folder"' %folder.folder), 
                    fields = 'files(id, name)').execute()
                for item in results.get('files', []): 
                    folder_id = item['id']
# get files in folder
                for fl in request.FILES.getlist('filelist'):
                    media = MediaInMemoryUpload(fl.read())
                    srv['service'].files().create(body = {'name': fl.name, 'parents': [folder_id]}, media_body = media).execute()
            except BaseException as e: 
                print('EXEPTION:', e)
        return redirect('../')
    else:
        context = {'status':'',
            'contextmenu':{'Подтвердить': 'formmethod=POST', 'Вернуться': 'formmethod=GET formaction=../'},
            'subtitle':'Медиа: альбомы изображений: загрузка'}
        return render(request, 'gdiskfolder_loadimages.html', context = context)

@require_http_methods(['GET'])
def gdiskfolder_deleteimage(request):
    srv = gdrive_open()
    if srv['status'] == None:
        for item in request.GET.getlist('imgid'):
            file_id, file_name = item.split(':')
            srv['service'].files().delete(fileId = file_id).execute()
    return redirect('../')

