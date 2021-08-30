from django import forms
from .models import Account
from devicesapi.models import Dispositivo, Configuracoes


class AccountForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter Password',
        'class': 'form-control',
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm Password',
        'class': 'form-control'
    }))

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'username','phone_number', 'email', 'password']

    def __init__(self, *args, **kwargs):
        super(AccountForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter first name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter last name'
        self.fields['username'].widget.attrs['placeholder'] = 'Enter username'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter phone number'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter email address'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super(AccountForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError("Password does not match!")


class DispositivoForm(forms.ModelForm):
    class Meta:
        model = Dispositivo
        fields = ['nome', 'placa', 'tipo']


class ConfiguracaoForm(forms.ModelForm):
    class Meta:
        model = Configuracoes
        fields = ['limite_inferior', 'limite_superior']
