from django.urls import path, include

from channel import views

appname = 'channel'

urlpatterns = [
    path('', views.ChannelListView.as_view()),
    path('delete/', views.channeldeleteview, name ='delete'),
    path('detail/', views.channeldetailview, name ='detail'),
    path('create/', views.channelcreateview, name ='create'),
    path('detail/update/', views.channelupdateview, name ='detail_update'),
    path('detail/docs/', include('docstore.urls')),
    path('exclude/', views.channelexcludeview),
    path('frombase/', views.ChannelBaseView.as_view()),
    path('frombase/select/', views.channelselecteview),
    path('select/', views.channelselecteview),
]
