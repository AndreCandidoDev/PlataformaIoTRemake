from django import forms
from .models import DispositivoRede


class DispositivoRedeForm(forms.ModelForm):
    class Meta:
        model = DispositivoRede
        fields = ['nome', 'ip', 'placa', 'tipo']

    def __init__(self, *args, **kwargs):
        super(DispositivoRedeForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
