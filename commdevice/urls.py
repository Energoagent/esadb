from django.urls import path, include

from commdevice import views

appname = 'commdevice'

urlpatterns = [
    path('', views.CommDeviceListView.as_view()),
    path('detail/', views.commdevicedetailview),
    path('detail/cddirchoice/', views.CDDirectoryChoiceView.as_view()),
    path('detail/cddirchoice/select/', views.cddirchoiceselect),
    path('detail/docs/', include('docstore.urls')),
    path('create/', views.commdevicecreateview),
    path('delete/', views.commdevicedeleteview),
    path('exclude/', views.commdeviceexcludeview),
    path('frombase/', views.CommDeviceBaseView.as_view()),
    path('frombase/select/', views.commdeviceselecteview),
    path('select/', views.commdeviceselecteview),
    path('detail/update/', views.commdeviceupdateview),
    ]