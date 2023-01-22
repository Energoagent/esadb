from django.urls import path, include

from org import views

appname = 'org'

urlpatterns = [
    path('', views.OrganizationListView.as_view()),
    path('detail/', views.organizationdetailview, name ='detail'),
    path('detail/update/', views.organizationupdateview, name ='update'),
#    path('detail/einst/', include('einst.urls')),
    path('create/', views.organizationcreateview, name ='create'),
    path('delete/', views.organizationdeleteview, name ='delete'),
    path('update/', views.organizationupdateview, name ='update'),
    path('detail/docs/', include('docstore.urls')),
    path('detail/contacts/', include('contact.urls')),
]
