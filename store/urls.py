from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('success/', views.success, name='success'),
    path('track-order/', views.track_order, name='track_order'),
path('increase/<int:product_id>/', views.increase_quantity, name='increase_quantity'),
path('decrease/<int:product_id>/', views.decrease_quantity, name='decrease_quantity'),
path('mpesa-payment/', views.mpesa_payment, name='mpesa_payment'),
path('mpesa-callback/', views.mpesa_callback, name='mpesa_callback'),
]