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
    path('', views.index, name='login_page'),
    path('hi/', views.index, name='register_render'),
    path('rulelist/', views.Ruleslist.as_view(), name='rulelist'),

    path('rules/rule1',views.AddItemRule.as_view(), name='rule1add'),
    path('rule1status/rule1status',views.getItemRule, name='rule1status'),

    path('rules/rule2',views.AddPriceRule.as_view(), name='rule2add'),
    path('rule1status/rule2status',views.getPriceRule, name='rule2status'),

     path('rules/rule3',views.AddlevelRule.as_view(), name='rule3add'),
    path('rule1status/rule3status',views.getlevelRule, name='rule3status'),




]
