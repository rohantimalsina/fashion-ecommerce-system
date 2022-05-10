from unicodedata import name
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header  =  "Elite Store Admin Dashboard"  
admin.site.site_title  =  "Elite Store Admin Dashboard"
admin.site.index_title  =  "Elite Store Admin Dashboard"

urlpatterns = [
    
    path('', views.home, name="home"),
    path('product/<str:slug>/<int:id>',views.product_detail,name='product_detail'),
    path('product-list',views.product_list,name='product-list'),
    
    path('category-products/<int:cat_id>',views.category_products,name='category-products'),
    path('add-to-cart/', views.add_to_cart, name="add-to-cart"),
    path('remove-cart/<int:cart_id>/', views.remove_cart, name="remove-cart"),
    path('plus-cart/<int:cart_id>/', views.plus_cart, name="plus-cart"),
    path('minus-cart/<int:cart_id>/', views.minus_cart, name="minus-cart"),
    path('cart/', views.cart, name="cart"),
    path('save-review/<int:pid>',views.save_review, name='save-review'),
    path('checkout/', views.checkout, name="checkout"),
    path('add-to-wishlist/', views.add_to_wishlist, name="add-to-wishlist"),
    path('wishlist/', views.wishlist, name="wishlist"),
    path('remove-wishlist/<int:wishlist_id>/', views.remove_wishlist, name="remove-wishlist"),
    path('search',views.search,name='search'),

    path('update-address/<int:id>',views.update_address, name='update-address'),
    path('profile/add-address/', views.save_address, name="add-address"),
    
    
    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
