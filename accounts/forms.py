from django import forms
from .models import Account, UserProfile, Plano


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
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password']

    def __init__(self, *args, **kwargs):
        super(AccountForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Nome'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Sobrenome'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Celular com DDD'
        self.fields['phone_number'].widget.attrs['max_length'] = 11
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super(AccountForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError("Password does not match!")


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['cpf', 'endereco_completo', 'cep', 'cidade', 'estado']

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['cpf'].widget.attrs['placeholder'] = 'Apenas digítos'
        self.fields['cpf'].widget.attrs['max_length'] = 11
        self.fields['cep'].widget.attrs['placeholder'] = 'Apenas digítos'
        self.fields['cep'].widget.attrs['max_length'] = 8
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


# form de criação de plano
class PlanoForm(forms.ModelForm):
    class Meta:
        model = Plano
        fields = ['plano', 'periodo']

    def __init__(self, *args, **kwargs):
        super(PlanoForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


# form de renovação de plano
class PlanoUpdateForm(forms.ModelForm):
    class Meta:
        model = Plano
        fields = ['periodo']

    def __init__(self, *args, **kwargs):
        super(PlanoUpdateForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
