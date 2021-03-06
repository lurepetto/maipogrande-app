from django.forms import ModelForm, TextInput, NumberInput, EmailInput, Select, HiddenInput
from .models import Comercial, City


class CreateComercialForm(ModelForm):
    "Formulario para datos comerciales"

    class Meta:
        model = Comercial
        fields = (
            'ComercialId', 'ClientId', 'CompanyName', 'FantasyName', 'ComercialBusiness', 'Email',
            'ComercialDni', 'Address', 'Country', 'City', 'PhoneNumber'
        )
        widgets = {
            'ComercialId': HiddenInput(),
            'ClientId': HiddenInput(),
            'CompanyName': TextInput(attrs={'size': '15', 'minlength': 3, 'autofocus': '', 
                                            'pattern': '[ña-zÑA-ZáéíóúÁÉÍÓÚ\s\.]+$',
                                            'oninvalid': "setCustomValidity('Ingrese un nombre válido')", 'oninput': "setCustomValidity('')"}),
            'FantasyName': TextInput(attrs={'size': '15', 'minlength': 3, 'pattern': '[ña-zÑA-ZáéíóúÁÉÍÓÚ\s\.]+$',
                                            'oninvalid': "setCustomValidity('Ingrese un nombre válido')", 'oninput': "setCustomValidity('')"}),
            'ComercialBusiness': TextInput(attrs={'size': '15', 'minlength': 5, 'pattern': '[ña-zÑA-ZáéíóúÁÉÍÓÚ\s\.]+$',
                                                  'oninvalid': "setCustomValidity('Ingrese un nombre válido')", 'oninput': "setCustomValidity('')"}),
            'Email': EmailInput(),
            'ComercialDni': TextInput(),
            'Address': TextInput(attrs={'size': '27', 'pattern': '^[ÑA-Zña-záéíóúÁÉÍÓÚ0-9 _]*[ÑA-Zña-záéíóúÁÉÍÓÚ0-9][ÑA-ZñaáéíóúÁÉÍÓÚ-z0-9 _]*$', 
                                        'oninvalid': "setCustomValidity('Ingrese una dirección válida')", 'oninput': "setCustomValidity('')"}),
            'Country': Select(attrs={'autofocus': ''}),
            'City': Select(attrs={'autofocus': ''}),
            'PhoneNumber': NumberInput(attrs={'minlength': 7}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['City'].queryset = City.objects.none()
        if 'Country' in self.data:
            try:
                country_id = int(self.data.get('Country'))
                self.fields['City'].queryset = City.objects.filter(
                    Country_id=country_id).order_by('CityName')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['City'].queryset = self.instance.Country.city_set.order_by(
                'CityName')
