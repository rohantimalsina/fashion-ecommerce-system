from unicodedata import name
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('signup', views.signup, name="signup"),
    path('login', views.signin, name="signin"),
    path('signout', views.signout, name="signout"),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('myaccount/', views.myaccount, name="myaccount"),
    path('contact', views.contact, name="contact"),
    path('about', views.about, name="about"),
    path('terms', views.terms, name="terms"),
    path('privacy-policy', views.privacy_policy, name="privacy-policy"),
    

    
    

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
