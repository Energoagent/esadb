from django.urls import path

from gdiskstorage import views

appname = 'gdiskstorage'

urlpatterns = [
#    path('', views.GDiskListView.as_view(), name = 'gdisklist'),
    path('', views.gdisk_list, name = 'list'),
#    path('detail/loadimage', views.albumloadimage, name = 'loadimage'),
#    path('detail/deleteimage', views.albumdeleteimage, name = 'deleteimage'),
#    path('create/', views.albumcreate, name = 'create'),
#    path('update/', views.albumupdate, name = 'update'),
#    path('delete/', views.albumdelete, name = 'delete')
]