from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('user_service.urls')),
    path('', include('post_service.urls')),
    path('', include('ui_service.urls')),
    # path('', include('chat_service.urls')),
    # Add other app URLs as needed
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)