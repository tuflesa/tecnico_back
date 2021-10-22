"""tecnico URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# from rest_framework.authtoken.views import obtain_auth_token
from administracion.views import CustomAuthToken

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/administracion/', include('administracion.urls')),
    path('api/estructura/', include('estructura.urls')),
    path('api/cargas/', include('cargas.urls')),
    path('api/velocidad/', include('velocidad.urls')),
    path('api/repuestos/', include('repuestos.urls')),
    path('api/mantenimiento/', include('mantenimiento.urls')),
    path('auth/', CustomAuthToken.as_view())
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
