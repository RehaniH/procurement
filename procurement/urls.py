"""procurement URL Configuration

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
from django.urls import path
from orders import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index , name= 'login_page'),
    path('hi/', views.index, name= 'register_render'),
    path('login/', views.login_web, name= 'login_check'),
    path('logout/', views.logout_view, name= 'logout_view'),
    path('check/', views.check_web, name= 'login_view_check'),
]
