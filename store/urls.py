from unicodedata import name
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    path('', views.home, name="home"),
    path('product/<str:slug>/<int:id>',views.product_detail,name='product_detail'),
    path('add-to-cart/', views.add_to_cart, name="add-to-cart"),
    path('cart/', views.cart, name="cart"),
    path('save-review/<int:pid>',views.save_review, name='save-review'),
    path('checkout/', views.checkout, name="checkout"),
    
    
    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
