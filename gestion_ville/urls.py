from django.urls import path
#from django.contrib import admin
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

urlpatterns = [
  # path('admin/', admin.site.urls),
  path('services/', views.services, name='services'),
  path('contact/', views.contact, name='contact'),
  path('team/', views.team, name='team'),
  path('about/', views.about, name='about'),
  path('pub/', views.publicite, name='pub'),
  path('signalement/', views.signalement, name='signalement'),
  path('signalement_liste/', views.liste_signalements, name='signalement_liste'), 
  path('localiser/<int:signalement_id>/', views.localiser, name='localiser'),
  path('create-demande/', views.create_demande, name='create-demande'),
  path('index/', views.index, name='index'),
  path('suivi/', views.suivi, name='suivi'),
  path('demandes/', views.demandes, name='demandes'),
  path('demande/modifier/<int:demande_id>/', views.modifier_demande, name='modifier_demande'),



     #path('logout/', views.logout, name='logout'),
     #path('dashboard/', views.dashboard, name='dashboard'),
     #path('analyses/', views.analyses, name='analyses'),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
