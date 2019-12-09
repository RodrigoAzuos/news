from django.urls import path,include
from django.contrib.auth.views import login, logout_then_login
from usuario import views

urlpatterns = [
    ##Usuario##
    path('registrar/', views.RegistrarUsuarioView.as_view() , name = 'registrar'),
    path('gerar-senha/<int:usuario_id>/', views.gerar_senha , name = 'gerar_senha'),
    path('usuario/', views.UsuarioView.as_view() , name = 'usuario'),
    path('login/', views.login, name='login'),
    path('logout/', logout_then_login, {'login_url': 'login'},name= 'logout'),

]