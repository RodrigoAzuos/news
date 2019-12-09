from django.shortcuts import render
from django.forms import forms
from django.core.exceptions import ValidationError
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin
from usuario.forms import RegistrarUsuarioForm, AlterarSenhaForm
from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login as auth_login, update_session_auth_hash
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.hashers import check_password
import os, random

class MyView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

def login(request):
    if request.method == 'POST':
        
        form = AuthenticationForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']

        try:
            usuario = User.objects.get(email=username)
        except User.DoesNotExist:
            erro = True
            return render(request, 'login.html', {'form': form, 'erro': erro})

        match_check = check_password(password,usuario.password)

        if not match_check:
            erro = True
            return render(request, 'login.html', {'form': form,'erro':erro})
        else:
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('index')

    elif request.method == 'GET':
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

class RegistrarUsuarioView(MyView, View):
    def get(self, request):

        usuarios = User.objects.all()
        logado = get_usuario_logado(request)

        if not get_usuario_logado(request).is_superuser:
            return render(request,'permissao.html')

        form = RegistrarUsuarioForm
        logado = get_usuario_logado(request)
        return render(request, 'registrar_colaborador.html', {'form': form, 'usuarios': usuarios, 'logado': logado})

    @transaction.Atomic(using=None, savepoint=True)
    def post(self, request):
        form = RegistrarUsuarioForm(request.POST)
        password = "".join([chr(random.randrange(64, 90)) for x in range(8)])

        if not get_usuario_logado(request).is_superuser:
            return render(request,'permissao.html')

        if (form.is_valid()):
            dados = form.data

            User.objects.create_user(username=dados['email'],
                                     first_name=dados['first_name'],
                                     last_name=dados['last_name'],
                                     email=dados['email'],
                                     password=password,
                                     is_staff = True,
                                     )

            mensagem = 'Colaborador cadastrado. Usuario:  %s,  senha: %s' %(dados['email'], password)
            logado = get_usuario_logado(request)

            return render(request, 'registrar_colaborador.html', {'form': form, 'mensagem': mensagem, 'logado': logado })

        return render(request, 'registrar_colaborador.html', {'form': form})

class UsuarioView(MyView, View):
    
    def get(self, request):
        usuario = get_usuario_logado(request)
        return render(request, 'usuario.html', {'usuario': usuario})

    def post(self, request):
        usuario = get_usuario_logado(request)
        form = AlterarSenhaForm(request.POST)
        dados = form.data
        
        password = dados['password']
        new_password = dados['new_password']
        
        match_check = check_password(password,usuario.password)

        if not match_check:
            return render(request, 'usuario.html', {'usuario': usuario,
             'form': form,
             'erro': 'Senha antiga está incorreta'})

        if (form.is_valid()):
            usuario.set_password(new_password)
            usuario.save()
            return render(request, 'usuario.html', {'usuario': usuario,
             'form': form,
             'mensagem': 'Senha alterada'})

        return render(request, 'usuario.html', {'usuario': usuario, 'form': form})


        
def get_usuario_logado(request):
    return request.user

def gerar_senha(request, usuario_id):
  
    password = "".join([chr(random.randrange(64, 90)) for x in range(8)])
    usuarios = User.objects.all()
    usuario = usuarios.filter(pk=usuario_id)[0]
    
    logado = get_usuario_logado(request)
    usuario.set_password(password)
    usuario.save()
    
    mensagem = ('Senha alterada, usuario: %s nova senha: %s' % (usuario.email, password) )
    form = RegistrarUsuarioForm
    
    return render(request, 'registrar_colaborador.html', {'form': form, 'usuarios':usuarios, 'mensagem': mensagem, 'logado': logado })
