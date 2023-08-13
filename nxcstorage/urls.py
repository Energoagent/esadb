from django.urls import path

from nxcstorage import views

appname = 'nxcstorage'

urlpatterns = [
    path('', views.NXCFolderListView.as_view(), name = 'list'),
    path('detail/', views.nxcfolder_detail, name = 'detail'),
    path('detail/downloadimage', views.nxcfolder_downloadimage, name = 'downloadimage'),
    path('detail/uploadimage', views.nxcfolder_uploadimage, name = 'uploadimage'),
    path('detail/deleteimage', views.nxcfolder_deleteimage, name = 'deleteimage'),
    path('create/', views.nxcfolder_create, name = 'create'),
    path('update/', views.nxcfolder_update, name = 'update'),
    path('delete/', views.nxcfolder_delete, name = 'delete'),
    
]