from unicodedata import name
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name="home"),
    path('signup', views.signup, name="signup"),
    path('login', views.signin, name="signin"),
    path('logout', views.signout, name="signout"),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),

    
    

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
