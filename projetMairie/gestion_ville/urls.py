from django.urls import path
#from django.contrib import admin
from . import views

urlpatterns = [
   # path('admin/', admin.site.urls),
    path('services/', views.services, name='services'),
    path('contact/', views.contact, name='contact'),
    path('team/', views.team, name='team'),
    path('about/', views.about, name='about'),
    path('pub/', views.publicite, name='pub'),
     #path('logout/', views.logout, name='logout'),
     #path('dashboard/', views.dashboard, name='dashboard'),
     #path('analyses/', views.analyses, name='analyses'),
]