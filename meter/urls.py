from django.urls import path, include

from meter import views

appname = 'meter'

urlpatterns = [
    path('',views.MeterListView.as_view()),
    path('delete/', views.meterdeleteview),
    path('copy/', views.metercopyview),
    path('detail/', views.meterdetailview),
    path('detail/update/', views.meterupdateview),
    path('detail/meterdirchoice/', views.ATCMeterDirChoiceView.as_view()),
    path('detail/meterdirchoice/select/', views.directorychoiceselect),
    path('detail/docs/', include('docstore.urls')),
    path('create/meterdirchoice/', views.ATCMeterDirChoiceView.as_view()),
    path('create/meterdirchoice/select/', views.metercreateview),
    path('create/', views.metercreateview),
    path('exclude/', views.meterexcludeview),
    path('frombase/', views.MeterBaseView.as_view()),
    path('frombase/select/', views.meterselecteview),
    path('select/', views.meterselecteview),
    ]