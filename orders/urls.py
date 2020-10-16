from django.conf.urls import url
from django.urls.conf import path 
from orders import views

urlpatterns = [
    path('reqorderlist/', views.requestOrder_list), 
    path('requestorder/<int:pk>', views.reqOrder_detail),
    path('deliveryloglist/',views.DeliveryLog_list),
    path('deliverylog/<int:pk>',views.DeliveryLog_detail)
    
]