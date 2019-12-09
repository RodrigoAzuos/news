from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from score.forms import PacienteForms, ScoreForms
from score.models import Paciente, Score
from usuario.views import  MyView, get_usuario_logado
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login')

def index(request):
    pacientes = Paciente.objects.order_by('-valor_score')
    top = pacientes[:4]
    len_page = 10

    paginator = Paginator(pacientes, len_page)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1


    try:
        p = paginator.page(page).object_list
    except (EmptyPage, InvalidPage):
        p = paginator.page(paginator.num_pages).object_list

    ultima = paginator.num_pages
    if page == 1: anterior = 1
    else: anterior = page - 1
    if page == ultima: proxima = ultima
    else: proxima = page + 1

    return render(request, 'index.html', {'pacientes': p, 'top': top, 'anterior': anterior, 'proxima': proxima, 'page': page, 'ultima': ultima})


def painel(request):
    pacientes = Paciente.objects.order_by('-valor_score')
    top = pacientes[:4]
    len_page = 10

    paginator = Paginator(pacientes, len_page)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1


    try:
        p = paginator.page(page).object_list
    except (EmptyPage, InvalidPage):
        p = paginator.page(paginator.num_pages).object_list

    ultima = paginator.num_pages
    if page == 1: anterior = 1
    else: anterior = page - 1
    if page == ultima: proxima = ultima
    else: proxima = page + 1

    return render(request, 'painel.html', {'pacientes': p, 'top': top, 'anterior': anterior, 'proxima': proxima, 'page': page, 'ultima': ultima})

class CadastroScoreView(MyView,View):

    def get(self, request, paciente_id):

        paciente = Paciente.objects.get(pk=paciente_id)
        form = ScoreForms()

        return render(request, 'paciente.html', {'form': form, 'paciente': paciente})

    def post(self,request, paciente_id):
        form = ScoreForms(request.POST)
        paciente = Paciente.objects.get(pk=paciente_id)

        if form.is_valid():

            dados = form.data
            score = Score()
            usuario = get_usuario_logado(request)

            score.nivel_conciencia =  dados['nivel_conciencia']
            score.temperatura = float(dados['temperatura'])
            score.frequencia_cardiaca = int(dados['frequencia_cardiaca'])
            score.pa_sistolica = int(dados['pa_sistolica'])
            score.frequencia_respiratoria = int(dados['frequencia_respiratoria'])
            score.saturacao_oxigenio = int(dados['saturacao_oxigenio'])
            score.qualquer_o2 = dados['qualquer_o2']
            score.paciente = paciente
            score.profissional = usuario
            score.save()
            paciente.valor_score = score.score()
            paciente.save()

            return redirect('paciente', paciente_id)

        return render(request, 'paciente.html', {'form': form, 'paciente': paciente})


class CadastroPacienteView(MyView,View):

    def get(self, request):

        form = PacienteForms
        print(form)
        return render(request, 'cadastrar_paciente.html', {'form': form})

    def post(self, request):
        form = PacienteForms(request.POST)

        if form.is_valid():

            # model_instance = form.save(commit=False)
            dados = form.data
            paciente = Paciente(
                nome=dados['nome'],
                telefone= dados['telefone'],
                leito = dados['leito'],
                nome_mae = dados['nome_mae'],
                data_nascimento= dados['data_nascimento'])
            score = Score()
            score.save()
            paciente.score = score
            paciente.save()
            return redirect('paciente', paciente.id)

        return render(request, 'cadastrar_paciente.html', {'form': form })

# Create your views here.

# TODO
# REGISTRO colaborador
# PEDIR PRO RENATO OS HORARIOS
