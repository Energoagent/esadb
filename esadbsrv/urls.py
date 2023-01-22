from django.urls import path, include

from esadbsrv.viewmods import viewatcttndir, viewatcmeterdir, viewcddir
from esadbsrv import views

urlpatterns = [
    path('', views.about, name = 'about'),
    path('about/', views.about, name = 'about'),
    path('media/', views.media, name = 'media'),
    path('equipment/', views.equipment, name = 'equipment'),
    path('staff/', views.staff, name = 'staff'),
#ИИК
    path('mic/', include('mic.urls')),
# организация    
    path('organization/', include('org.urls')),
# энергообъект  
    path('einst/', include('einst.urls')),
# экземпляр ТТН 
    path('ttnexample/', include('ttnexample.urls')),
# экземпляр счетчика 
    path('meter/', include('meter.urls')),
# устройство связи, УСПД
    path('commdevice/', include('commdevice.urls')),
# каналы связи
    path('channel/', include('channel.urls')),
# справочник устройств связи, УСПД
    path('cddirectory/', viewcddir.CDDirectoryListView.as_view(), name = 'cddirectory'),
    path('cddirectory/detail/', viewcddir.cddirectorydetailview, name ='cddirectorydetail'),
    path('cddirectory/create/', viewcddir.cddirectorycreateview, name ='cddirectorycreate'),
    path('cddirectory/delete/', viewcddir.cddirectorydeleteview, name ='cddirectorydelete'),
    path('cddirectory/update/', viewcddir.cddirectoryupdateview, name ='cddirectoryupdate'),
# справочник счетчиков АТС 
    path('atcmeterdir/', viewatcmeterdir.ATCMeterDirListView.as_view(), name = 'atcmeterdir'),
    path('atcmeterdir/detail/', viewatcmeterdir.atcmeterdirdetailview, name = 'atcmeterdir_detail'),
    path('atcmeterdirimport/', viewatcmeterdir.atsmeterdirimport, name = 'atcmeterdir_import'),
# справочник ТТН АТС 
    path('atcttndirectory/', viewatcttndir.ATCTTNDirectoryListView.as_view(), name = 'atcttndir'),
    path('atcttndirectory/detail/', viewatcttndir.atcttndirectorydetailview, name = 'atcttndir_detail'),
    path('atcttndirectoryimport/', viewatcttndir.atcttndirectoryimport, name = 'atcttndir_import'),
    ]
