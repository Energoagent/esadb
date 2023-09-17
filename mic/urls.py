from django.urls import path, include

from mic import views
from channel.views import ChannelSelectView

urlpatterns = [
    path('',views.MICListView.as_view()),
    path('create/', views.miccreateview),
    path('delete/', views.micdeleteview),
    path('detail/', views.micdetailview),
    path('detail/update/', views.micupdateview),
    path('detail/docs/', include('docstore.urls')),
    path('detail/einst/', views.EInstSelectView.as_view()),
    path('detail/einst/select/', views.einstselect),
    path('detail/channel/', views.CHNListView.as_view()),
#    path('detail/channel/add/', views.CHNListView.as_view()),
#    path('detail/channel/select/', views.channelselect),
    path('detail/ttnexample/', include('ttnexample.urls')),
    path('detail/meter/', include('meter.urls')),
    ]

