
from django.urls import path
from squeaker import views
urlpatterns = [
    path('houseprice/', views.HousePrice.as_view(), name='houseprice'),
    path('digit/', views.DetectDigitImage.as_view(), name='digits'),
    path('fashion/', views.DetectFashionImage.as_view(), name='fashion'),


]
