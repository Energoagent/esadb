from django.urls import path, include

from contact import views

appname = 'contact'

urlpatterns = [
    path('', views.ContactListView.as_view()),
    path('delete/', views.contactdeleteview, name ='delete'),
    path('exclude/', views.contactexcludeview, name ='exclude'),
    path('detail/', views.contactdetailview, name ='detail'),
    path('create/', views.contactcreateview, name ='create'),
    path('phonebook/select/', views.contactselectview, name ='phonebook_select'),
    path('phonebook/', views.PhoneBookView.as_view(), name ='phonebook'),
#    path('gcontacts/', views.gcontactsview, name ='gcontacts'),
    path('detail/update/', views.contactupdateview, name ='detail_update'),
    path('detail/docs/', include('docstore.urls')),
]
