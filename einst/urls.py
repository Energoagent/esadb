from django.urls import path, include

from einst import views, reports
from org.views import OrganizationChoiceView
from project.views import ProjectListView

appname = 'einst'

urlpatterns = [
    path('', views.EInstListView.as_view()),
    path('delete/', views.einstdeleteview, name ='delete'),
    path('detail/', views.einstdetailview, name ='detail'),
    path('create/', views.einstcreateview, name ='create'),

    path('detail/update/', views.einstupdateview, name ='detail_update'),
    path('detail/albums/', include('albumstore.urls')),
    path('detail/docs/', include('docstore.urls')),
    path('detail/contacts/', include('contact.urls')),
    path('detail/report/', reports.einst_report, name ='detail_report'),

    path('detail/owner/', OrganizationChoiceView.as_view(), name ='owner'),
    path('detail/owner/select/', views.einstownerselect, name ='owner_select'),

    path('detail/project/', ProjectListView.as_view(), name ='project'),
    path('detail/project/select/', views.projectselect, name ='project_select'),

# ИИК
    path('detail/mic/', include('mic.urls')),
# устройства связи
    path('detail/commdevice/', include('commdevice.urls')),
# каналы связи
    path('detail/channels/', include('channel.urls')),
]
