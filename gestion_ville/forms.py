""" from django.contrib.gis import forms
from .models import Signalement, Citoyen
from mapwidgets.widgets import GooglePointFieldWidget


class SignalementForm(forms.ModelForm):
    class Meta:
        model = Signalement
        fields = ['description', 'date_signalement', 'etat_signalement', 'lieu', 'type_signalement', 'location']
        widgets = {
            'location': GooglePointFieldWidget,
        }
        #gis_models.PointField: {'widget': GooglePointFieldWidget}

class CitoyenForm(forms.ModelForm):
    class Meta:
        model = Citoyen
        fields = ['nom', 'adresse', 'telephone']


 """

from .models import Signalement, Citoyen, Demande
from django import forms
from django.forms.widgets import TextInput

class GoogleMapsPointWidget(TextInput):
    class Media:
        js = (
            'https://maps.googleapis.com/maps/api/js?key=AIzaSyCIBX9BJO-fPv7OyJLMsWUCQuv9JbH15SE',
            'js/google-maps-point-widget.js',
        )

    def __init__(self, attrs=None, **kwargs):
        if attrs is None:
            attrs = {}
        attrs['readonly'] = 'readonly'
        super().__init__(attrs=attrs)
        
    def build_attrs(self, base_attrs=None, extra_attrs=None):
        attrs = super().build_attrs(base_attrs, extra_attrs=extra_attrs)
        attrs['id'] = 'id_location'
        attrs['class'] = 'google-maps-point-widget'
        return attrs

    def render(self, name, value, attrs=None, renderer=None):
        if value is None:
            value = ''
        attrs = self.build_attrs(attrs)  # Utiliser directement "attrs" au lieu de "final_attrs"
        return super().render(name, value, attrs, renderer)
    
class SignalementForm(forms.ModelForm):
    location = forms.CharField(widget=GoogleMapsPointWidget)

    class Meta:
        model = Signalement
        fields = ['description', 'date_signalement', 'etat_signalement', 'lieu', 'type_signalement', 'location']


class CitoyenForm(forms.ModelForm):
    class Meta:
        model = Citoyen
        fields = '__all__'

class DemandeForm(forms.ModelForm):
    class Meta:
        model = Demande
        fields = '__all__'
        widgets = {
            'fichier': forms.ClearableFileInput(attrs={'multiple': False}),
            'recup': forms.RadioSelect(choices=[(True, 'Récupérer en ligne (coût plus élevé)'), (False, 'Passer à l\'hôtel de ville')]),
            'filerecup': forms.ClearableFileInput(attrs={'multiple': False}),
        }
    
    def clean(self):
        ...
