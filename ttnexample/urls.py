from django.urls import path, include

from ttnexample import views
from mic.views import MICChoiceView

appname = 'ttnexample'

urlpatterns = [
    path('',views.TTNExampleListView.as_view()),
    path('delete/', views.ttnexampledeleteview),
    path('copy/', views.ttnexamplecopyview),
    path('detail/', views.ttnexampledetailview),
    path('detail/deinst/', views.ttnexampledeinstview),
    path('detail/reinst/', MICChoiceView.as_view()),
    path('detail/reinst/select/', views.ttnexamplemicselectview),
    path('detail/update/', views.ttnexampleupdateview),
    path('detail/ttndirchoice/', views.ATCTTNDirectoryChoiceView.as_view()),
    path('detail/ttndirchoice/select/', views.directorychoiceselect),
    path('detail/docs/', include('docstore.urls')),
    path('create/ttndirchoice/', views.ATCTTNDirectoryChoiceView.as_view()),
    path('create/ttndirchoice/select/', views.ttnexamplecreateview),
    path('create/', views.ttnexamplecreateview),
]
