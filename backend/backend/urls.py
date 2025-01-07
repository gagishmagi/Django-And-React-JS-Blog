from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

from django.conf import settings
from django.conf.urls.static import static

from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',TemplateView.as_view(template_name='index.html')),
    path('', include('core.urls')),
    path('auth/', obtain_auth_token),

]

urlpatterns += static(settings.IMG_URL,document_root=settings.IMG_ROOT)
urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)