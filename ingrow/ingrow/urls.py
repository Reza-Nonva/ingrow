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
    path('create_service/', views.create_service),
    path('create_work/', views.create_work),
    path('create_work_report/', views.create_work_report),
    path('create_project/', views.create_project),
    path('create_payment/', views.create_payment),
    path('insert_buy/', views.insert_buy),
    path('delete_customer/', views.delete_customer),
    path('delete_payment/', views.delete_payment),
    path('delete_project/', views.delete_project),
    path('delete_service/', views.delete_service),
    path('delete_work/', views.delete_work),
    path('delete_work_report/', views.delete_work_report),
    path('delete_buy/', views.delete_buy),
    path('customer_list/', views.customer_list),
    path('project_list/', views.project_list),
    path('products_list/', views.products_list),
    path('services_list/', views.services_list),
    path('work_list/', views.work_list),
    path('work_report_list/', views.work_report_list),
    path('project_costs/', views.get_project_costs)
]
