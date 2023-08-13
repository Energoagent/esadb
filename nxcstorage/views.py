import os
import io

# Django modules
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.forms import ModelForm

# NextCloud API
from nextcloud import NextCloud

NEXTCLOUD_URL = "http://192.168.22.22:80"
NEXTCLOUD_USERNAME = 'esadb'
NEXTCLOUD_PASSWORD = 'Kvb3602489363'

# other modules
from random import choice
from string import digits
from PIL import Image

# ESADB modules
from esadbsrv.viewmods.viewcommon import CompleteListView
from nxcstorage.models import NXCFolder, NXC_PATH
from esadb.settings import BASE_DIR, EXPORT_DIR

def nxc_init():
    nxc = NextCloud(
        NEXTCLOUD_URL,
        user=NEXTCLOUD_USERNAME,
        password=NEXTCLOUD_PASSWORD,
        session_kwargs={
            'verify': False  # to disable ssl
            })
#    print('NXC_LIST', nxc.list_folders('/').data)
    return nxc

class NXCFolderListView(CompleteListView):
    model = NXCFolder
    paginate_by = 10
    ordering = 'name'
    template_name = 'nxcfolder_list.html'
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
        
class NXCFolderModelForm(ModelForm):
    class Meta:
        model = NXCFolder
        fields = ['name', 'info', 'note']

        
@require_http_methods(['GET', 'POST'])
def nxcfolder_create(request):
    if request.method == 'POST':
        folderform = NXCFolderModelForm(request.POST)
        if folderform.is_valid():
            folder = folderform.save(commit = False)
            folder.folder = ''.join(choice(digits) for i in range(12))
            folder.save()
            ownerid = request.session.get('ownerid')
            ownerclassname = request.session.get('ownerclass')
            if ownerclassname != None:
                owner = eval(ownerclassname + '.objects.get(id = ownerid)')
                if owner != None: 
                    owner.albums.add(folder)
# nextcloude code
            nxc = nxc_init()
            if nxc != None:
                new_folder_path = NXC_PATH + folder.folder
                nxc.create_folder(new_folder_path)
            return redirect('../')
    else: 
        folderform = NXCFolderModelForm()
    context = {}
    context['status'] = ''
    context['contextmenu'] = {'Отменить':'formmethod=GET formaction=../', 'Подтвердить':'formmethod=POST'}
    context['subtitle'] = 'Медиа: альбомы изображений: создание'
    context['form'] = folderform
    return render(request, 'nxcfolder_form.html', context = context)

@require_http_methods(['GET', 'POST'])
def nxcfolder_update(request):
    if request.method == 'POST':
        nxcfolderid = request.session.get('nxcfolderid')
        if nxcfolderid != None: 
            folderform = NXCFolderModelForm(request.POST, instance = NXCFolder.objects.get(id = nxcfolderid))
            if folderform.is_valid():
                folder = folderform.save()
        return redirect('../')
    else: 
        nxcfolderid = request.GET.get('nxcfolderid')
        if nxcfolderid != None: 
            folderform = NXCFolderModelForm(instance = NXCFolder.objects.get(id = nxcfolderid))
        else:
            return redirect('../')
        request.session['nxcfolderid'] = nxcfolderid
        request.session.modified = True
    context = {'form': folderform,
        'contextmenu': {'Отменить':'formmethod=GET formaction=../', 'Подтвердить':'formmethod=POST'},
        'subtitle': 'Медиа: альбомы изображений: создание'}
    return render(request, 'nxcfolder_form.html', context = context)

@require_http_methods(['GET', 'POST'])
def nxcfolder_delete(request):
    if request.method == 'GET':
        nxcfolderid = request.GET.get('nxcfolderid')
        if nxcfolderid != None:
            context = {'folder': NXCFolder.objects.get(id = nxcfolderid),
                'contextmenu':{'Отменить':'formmethod=GET formaction=../', 'Удалить': 'formmethod=POST'}, 
                'subtitle':'Медиа: альбомы изображений: удаление'}
            return render(request, 'nxcfolder_confirm_delete.html', context = context)
    else: 
        nxcfolderid = request.POST.get('nxcfolderid')
        if nxcfolderid != None:
            folder = NXCFolder.objects.get(id = nxcfolderid)
# next cloud
            nxc = nxc_init()
            if nxc != None:
                folder_path = NXC_PATH + folder.folder
                nxc.delete_path(folder_path)
            folder.delete()
    return redirect('../')

@require_http_methods(['GET'])
def nxcfolder_detail(request):
    filelist = ''
    nxcfolderid = request.GET.get('nxcfolderid')
    if nxcfolderid == None: 
        nxcfolderid = request.session.get('nxcfolderid')
    if nxcfolderid == None: 
        return redirect('../')
    folder = NXCFolder.objects.get(id = nxcfolderid)
    request.session['nxcfolderid'] = folder.pk
    request.session.modified = True
# next cloud
    nxc = nxc_init()
    if nxc != None:
        folder_path = NXC_PATH + folder.folder
        nxc_folder = nxc.get_folder(folder_path)
        if str(nxc_folder) != 'Null':
            filelist = nxc_folder.list(all_properties = True)
#----------------------------------------------------------
    context = {'status': '', 'folder': folder, 'filelist': filelist, 'about': nxc.user, 
        'folder_link': nxc_folder.href, 'host' : NEXTCLOUD_URL,
        'contextmenu':{'Скачать': 'formmethod=GET formaction=downloadimage',
            'Загрузить': 'formmethod=GET formaction=uploadimage',
            'Удалить': 'formmethod=GET formaction=deleteimage',
            'Вернуться': 'formmethod=GET formaction=../'},
        'subtitle':'Медиа: альбомы изображений: просмотр'}
    return render(request, 'nxcfolder_detail.html', context = context)

@require_http_methods(['GET'])
def nxcfolder_downloadimage(request):
# next cloud
    nxc = nxc_init()
    if nxc != None:
        for item in request.GET.getlist('filename'):
            nxc.download_file(item, target = EXPORT_DIR)
    return redirect('../')

@require_http_methods(['GET', 'POST'])
def nxcfolder_uploadimage(request):
    nxcfolderid = request.session.get('nxcfolderid')
    if nxcfolderid == None:
        return redirect('../')
    if request.method == 'POST':
        if request.FILES == None:
            return redirect('../')
        folder = NXCFolder.objects.get(id = nxcfolderid)
# next cloud
        nxc = nxc_init()
        if nxc != None:
            for fl in request.FILES.getlist('filelist'):
                remote_filepath = NXC_PATH + folder.folder + '/' + fl.name
                nxc.upload_file_contents(fl, remote_filepath, timestamp=None)
            return redirect('../')
    else:
        context = {'status':'',
            'contextmenu':{'Подтвердить': 'formmethod=POST', 'Вернуться': 'formmethod=GET formaction=../'},
            'subtitle':'Медиа: альбомы изображений: загрузка'}
        return render(request, 'gdiskfolder_loadimages.html', context = context)

@require_http_methods(['GET'])
def nxcfolder_deleteimage(request):
# next cloud
    nxc = nxc_init()
    if nxc != None:
        for item in request.GET.getlist('filename'):
            nxc.delete_path(item)
    return redirect('../')

