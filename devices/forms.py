from django import forms
from devicesapi.models import Dispositivo, Configuracoes


class DispositivoForm(forms.ModelForm):
    class Meta:
        model = Dispositivo
        fields = ['nome', 'placa', 'tipo']

    def __init__(self, *args, **kwargs):
        super(DispositivoForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class ConfiguracaoForm(forms.ModelForm):
    class Meta:
        model = Configuracoes
        fields = ['limite_inferior', 'limite_superior']

    def __init__(self, *args, **kwargs):
        super(ConfiguracaoForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'