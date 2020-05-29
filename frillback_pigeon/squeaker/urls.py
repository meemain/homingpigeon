
from django.urls import path
from squeaker import views
urlpatterns = [
    path('', views.home, name='home'),
    path('classify/', views.call_house_model.as_view(), name='houseprice'),
    path('digit/', views.call_digits_model.as_view(), name='digits'),
    path('fashion/', views.call_fashion_model.as_view(), name='fashion'),


]
