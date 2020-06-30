from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.Form):
    username = forms.CharField(required=True,
                               min_length=4, max_length=15,
                               widget=forms.TextInput(attrs={
                                   'class': 'form-control',
                                   'id': 'username',
                                   'placeholder': 'Username'
                               }))
    email = forms.EmailField(required=True,
                             widget=forms.EmailInput(attrs={
                                 'class': 'form-control',
                                 'id': 'email',
                                 'placeholder': 'example@correo.com'
                             }))
    password = forms.CharField(required=True,
                               widget=forms.PasswordInput(attrs={
                                   'class': 'form-control',
                                   'id': 'password',
                                   'placeholder': 'Password'
                               }))
    password_2 = forms.CharField(required=True,
                                 label='Confirmar password',
                                 widget=forms.PasswordInput(attrs={
                                     'class': 'form-control',
                                     'id': 'password_2',
                                     'placeholder': 'Password'
                                 }))

    def clean_username(self):  # metodo para validar que no exista el mismo username
        username = self.cleaned_data.get('username')

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('El username ya se encuentra en uso')
        return username

    def clean_email(self):  # metodo para validar que no exista el mismo email
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('El email ya se encuentra en uso')
        return email

    def clean(self):  # se usara siempre y cuando se tenga que validar campos que dependen de otro
        cleaned_data = super().clean()  # obtiene la información del formulario

        if cleaned_data.get('password_2') != cleaned_data.get('password'):
            self.add_error('password_2', 'La contraseña no coincide')

    def save(self):
        return User.objects.create_user(
                    self.cleaned_data.get('username'),
                    self.cleaned_data.get('email'),
                    self.cleaned_data.get('password'),
                )
