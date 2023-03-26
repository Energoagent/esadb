from django.urls import path

from docstore import views

appname = 'docstore'

urlpatterns = [
    path('', views.DocStoreListView.as_view(), name = 'docstore'),
    path('<str:filename>', views.fileview),
    path('detail/', views.detailview, name = 'docstore_detail'),
    path('create/', views.createview, name = 'docstore_create'),
    path('delete/', views.deleteview, name = 'docstore_delete'),
    path('update/', views.updateview, name = 'docstore_update'),
]