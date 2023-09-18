import os
import shutil
from django.conf import settings
from django.shortcuts import render, redirect
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.forms import ModelForm
from pathlib import Path
from django.views import generic
from django.views.decorators.http import require_http_methods
from django.http import FileResponse

from random import choice
from string import digits
from PIL import Image

from albumstore.models import AlbumStore, albumpath, ALBUM_DIR
from esadbsrv.viewmods.viewcommon import CompleteListView
from einst.models import EInst


class AlbumListView(CompleteListView):
    model = AlbumStore
    paginate_by = 10
    ordering = 'name'
    template_name = 'album_list.html'
    subtitle = 'Медиа: альбомы изображений'
    contextmenu = {
        'Изображения': 'formmethod=GET formaction=detail/',
        'Изменить': 'formmethod=GET formaction=update/',
        'Добавить': 'formmethod=GET formaction=create/',
        'Удалить': 'formmethod=GET formaction=delete/',
        'Вернуться': 'formmethod=GET formaction=../'}
    filterkeylist = {'Наименование':'name', 'Информация':'info'}
    is_filtered = True
    def get_queryset(self):
        ownerid = self.request.GET.get('ownerid')
        if ownerid == None: ownerid = self.request.session.get('ownerid')
        ownerclass = self.request.GET.get('ownerclass')
        if ownerclass == None: ownerclass = self.request.session.get('ownerclass')
        if (ownerclass == None) or (ownerid == None): return super().get_queryset()
        owner = eval(ownerclass + '.objects.get(id = ownerid)')
        self.request.session['ownerclass'] = ownerclass
        self.request.session['ownerid'] = owner.id
        self.request.session.modified = True
        return owner.albums.all()

@require_http_methods(['GET'])
def albumdetail(request):
    albumid = request.GET.get('albumid')
    if albumid != None:
        album = AlbumStore.objects.get(id = albumid)
        try: 
            filelist = sorted(os.listdir(album.get_path()))
            if 'tumbnails' in filelist:
                filelist.remove('tumbnails')
        except: filelist =['empty']
        context = {'status':'', 'album': album,
            'contextmenu':{'Загрузить изображения': 'formmethod=GET formaction=loadimage',
                'Удалить изображения': 'formmethod=GET formaction=deleteimage',
                'Вернуться': 'formmethod=GET formaction=../'},
            'subtitle':'Медиа: альбомы изображений: просмотр'}
        context['filelist'] = filelist
        context['albumpath'] = ALBUM_DIR
        request.session['albumid'] = albumid
        request.session.modified = True
        return render(request, 'album_detail.html', context = context)
    return redirect('../')
    
@require_http_methods(['GET', 'POST'])
def albumloadimage(request):
    albumid = request.session.get('albumid')
    if request.method == 'POST':
        if request.FILES != None:
            album = AlbumStore.objects.get(id = albumid)
            try:
                ap = os.path.join(albumpath(), album.folder)
                for fl in request.FILES.getlist('filelist'):
                    with open(os.path.join(ap, fl.name), 'wb+') as destination:
                        for chunk in fl.chunks(): destination.write(chunk)
                    image = Image.open(os.path.join(ap, fl.name))
                    MAX_SIZE = (200, 200)
                    image.thumbnail(MAX_SIZE)
                    image.save(os.path.join(ap, 'tumbnails', fl.name))
            except BaseException as e: 
                print('EXEPTION:', e)
        return redirect('../')
    else:
        context = {'status':'',
            'contextmenu':{'Подтвердить': 'formmethod=POST', 'Вернуться': 'formmethod=GET formaction=../'},
            'subtitle':'Медиа: альбомы изображений: загрузка'}
        request.session['albumid'] = albumid
        request.session.modified = True
        return render(request, 'album_loadimages.html', context = context)

@require_http_methods(['GET'])
def albumdeleteimage(request):
    albumid = request.session.get('albumid')
    if request.method == 'GET':
        album = AlbumStore.objects.get(id = albumid)
        ap = os.path.join(albumpath(), album.folder)
        for fl in request.GET.getlist('imgid'):
            try: os.remove(os.path.join(ap, fl))
            except: pass
    request.session['albumid'] = albumid
    request.session.modified = True
    return redirect('../')

class AlbumModelForm(forms.ModelForm):
    class Meta:
        model = AlbumStore
        fields = ['local', 'name', 'info', 'note']
    
@require_http_methods(['GET', 'POST'])
def albumcreate(request):
    if request.method == 'POST':
        albumform = AlbumModelForm(request.POST)
        if albumform.is_valid():
            ownerid = request.GET.get('ownerid')
            if ownerid == None: ownerid = request.session.get('ownerid')
            ownerclass = request.GET.get('ownerclass')
            if ownerclass == None: ownerclass = request.session.get('ownerclass')
            if (ownerclass == None) or (ownerid == None): return super().get_queryset()
            owner = eval(ownerclass + '.objects.get(id = ownerid)')
            album = albumform.save(commit = False)
            album.folder =  owner.__str__().replace('/', '_') + '_' + album.name + ''.join(choice(digits) for i in range(12))
            album.save()
            try: 
                os.mkdir(os.path.join(albumpath(), album.folder))
                os.mkdir(os.path.join(albumpath(), album.folder, 'tumbnails'))
            except BaseException as e: 
                print('EXEPTION:', e)
            else:
                ownerid = request.session.get('ownerid')
                ownerclassname = request.session.get('ownerclass')
                if ownerclassname != None:
                    owner = eval(ownerclassname + '.objects.get(id = ownerid)')
                    if owner != None: owner.albums.add(album)
            return redirect('../')
    else: 
        albumform = AlbumModelForm()
    context = {}
    context['status'] = ''
    context['contextmenu'] = {'Отменить':'formmethod=GET formaction=../', 'Подтвердить':'formmethod=POST'}
    context['subtitle'] = 'Медиа: альбомы изображений: создание'
    context['form'] = albumform
    return render(request, 'album_form.html', context = context)

@require_http_methods(['GET', 'POST'])
def albumupdate(request):
    albumid = request.session.get('albumid')
    if albumid == None: return redirect('../')
    if request.method == 'POST':
        albumform = AlbumModelForm(request.POST, instance = AlbumStore.objects.get(id = albumid))
        if albumform.is_valid():
            albumform.save()
            return redirect('../')
    else:
        albumid = request.GET.get('albumid')
        if albumid == None: return redirect('../')
        albumform = AlbumModelForm(instance = AlbumStore.objects.get(id = albumid))
        request.session['albumid'] = albumid
        request.session.modified = True
    context = {'status':'',
        'contextmenu':{
            'Отменить':'formmethod=GET formaction=../',
            'Подтвердить':'formmethod=POST'}, 
        'subtitle':'Медиа: альбом: изменение',
        'form': albumform}
    return render(request, 'album_form.html', context = context)
    
@require_http_methods(['GET'])
def albumdelete(request):
    albumid = request.GET.get('albumid')
    if albumid != None: 
        album = AlbumStore.objects.get(id = albumid)
        try:
            shutil.rmtree(album.get_path())
        except Exception as e1: 
            print('EXEPTION:', e1)
        album.delete()
    return redirect('../')
    

