# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User

class RegistrarUsuarioForm(forms.Form):

    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)


    def is_valid(self):
        valid = True

        if not super(RegistrarUsuarioForm, self).is_valid():
            self.adiciona_erro('Por favor, verifique os dados informados')
            valid = False

        email_exists = User.objects.filter(email=self.data['email']).exists()

        if email_exists:
            self.adiciona_erro('Email já existe')
            valid = False

        return valid

    def adiciona_erro(self, message):
        errors = self._errors.setdefault(forms.forms.NON_FIELD_ERRORS, forms.utils.ErrorList())
        errors.append(message)

class AlterarSenhaForm(forms.Form):

    password = forms.CharField(required=True)
