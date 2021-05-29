from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


handler404 = 'vacancies.views.e_handler404'
handler500 = 'vacancies.views.e_handler500'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('vacancies.urls')),
    path('feedback/', include('feedback.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)