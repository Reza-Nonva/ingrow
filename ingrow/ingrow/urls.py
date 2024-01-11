"""
URL configuration for ingrow project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from web import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('create_customer/', views.create_customer),
    path ('broadcast/', views.broadcast),
    path('create_product/', views.create_product),
    path('create_project/', views.create_project),
    path('insert_buy/', views.insert_buy),


]
