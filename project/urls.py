from django.urls import path, include

from project import views

appname = 'project'

urlpatterns = [
    path('', views.ProjectListView.as_view()),
    path('select/', views.projectselectview, name ='select'),
    path('clear/', views.projectclearview, name ='clear'),
    path('detail/', views.projectdetailview, name ='detail'),
    path('detail/update/', views.projectupdateview, name ='update'),
    path('create/', views.projectcreateview, name ='create'),
    path('delete/', views.projectdeleteview, name ='delete'),
    path('update/', views.projectupdateview, name ='update'),
    path('detail/docs/', include('docstore.urls')),
    path('detail/contacts/', include('contact.urls')),
]
