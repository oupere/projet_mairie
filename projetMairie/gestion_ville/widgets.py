from django.forms.widgets import TextInput
from mapwidgets.widgets import GooglePointFieldWidget
from django.contrib.gis import forms
from .models import Signalement, Citoyen


class GoogleMapsPointWidget(TextInput):
    class Media:
        js = (
            'https://maps.googleapis.com/maps/api/js?key=AIzaSyCIBX9BJO-fPv7OyJLMsWUCQuv9JbH15SE&callback=initMap',
            'js/google-maps-point-widget.js',
        )

    def __init__(self, attrs=None):
        if attrs is None:
            attrs = {}
        attrs['readonly'] = 'readonly'
        super().__init__(attrs=attrs)

    def build_attrs(self, attrs=None, ):
        attrs = super().build_attrs(attrs=attrs)
        attrs['id'] = 'id_location'
        attrs['class'] = 'google-maps-point-widget'
        return attrs

class SignalementForm(forms.ModelForm):
    class Meta:
        model = Signalement
        fields = ['description', 'date_signalement', 'etat_signalement', 'lieu', 'type_signalement', 'location']
        widgets = {
            'location': GooglePointFieldWidget,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['location'].widget = GoogleMapsPointWidget()

class CitoyenForm(forms.ModelForm):
    class Meta:
        model = Citoyen
        fields = ['nom', 'adresse', 'telephone']

