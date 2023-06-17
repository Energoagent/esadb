from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

appname = 'esadbsrv'

urlpatterns = [
    path('', include('esadbsrv.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('project/', include('project.urls')),
    path('albumstore/', include('albumstore.urls')),
    path('docstore/', include('docstore.urls')),
    path('contact/', include('contact.urls')),
    path('gdiskstorage/', include('gdiskstorage.urls')),
    ]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)