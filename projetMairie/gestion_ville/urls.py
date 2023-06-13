from django.urls import path
#from django.contrib import admin
from . import views

urlpatterns = [
  # path('admin/', admin.site.urls),
  path('login/', views.login, name='login'),
  path('logout/', views.logout, name='logout'),
  path('dashboard/', views.dashboard, name='dashboard'),
  
  path('services/', views.services, name='services'),
  path('contact/', views.contact, name='contact'),
  path('team/', views.team, name='team'),
  path('about/', views.about, name='about'),
  path('pub/', views.publicite, name='pub'),
  path('signalement/', views.signalement, name='signalement'),
  path('signalement_liste/', views.liste_signalements, name='signalement_liste'), 
  path('signalement_detail/<int:signalement_id>/', views.signalement_detail, name='signalement_detail'),
  path('signalement_detail/<int:signalement_id>/', views.supprimer_signalement, name='supprimer_signalement'),
  path('localiser/<int:signalement_id>/', views.localiser, name='localiser'),
  path('travail/create/<int:signalement_id>', views.creer_travail, name='create_travail'),
  path('travail/detail/<int:travail_id>/', views.detail_travail, name='detail_travail'),
  path('travail/update/<int:travail_id>/', views.update_travail, name='update_travail'),
  path('travaux/', views.liste_travaux, name='liste_travaux'),


     #path('logout/', views.logout, name='logout'),
     #path('dashboard/', views.dashboard, name='dashboard'),
     #path('analyses/', views.analyses, name='analyses'),
]