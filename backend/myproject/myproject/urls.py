from django.urls import path
from myapp import views

urlpatterns = [
    path('get_product_price/', views.get_product_price, name='get_product_price'),
    # Add other URL patterns if needed
]
