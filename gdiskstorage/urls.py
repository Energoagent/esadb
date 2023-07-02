from django.urls import path

from gdiskstorage import views

appname = 'gdiskstorage'

urlpatterns = [
    path('', views.GDiskFolderListView.as_view(), name = 'list'),
    path('detail/', views.gdiskfolder_detail, name = 'detail'),
    path('detail/downloadimage', views.gdiskfolder_downloadimage, name = 'downloadimage'),
    path('detail/uploadimage', views.gdiskfolder_uploadimage, name = 'uploadimage'),
    path('detail/deleteimage', views.gdiskfolder_deleteimage, name = 'deleteimage'),
    path('create/', views.gdiskfolder_create, name = 'create'),
    path('update/', views.gdiskfolder_update, name = 'update'),
    path('delete/', views.gdiskfolder_delete, name = 'delete'),
    
]