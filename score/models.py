from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Base(models.Model):

    criado_em = models.DateTimeField('Criado em', auto_now_add=True, blank=False, null=False)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        abstract = True

    def get_criado_em(self, format):
        return self.criado_em.__format__(format).__str__()

    def get_atualizado_em(self, format):
        return self.atualizado_em.__format__(format).__str__()


class Paciente(Base):
    nome = models.CharField('Nome', max_length=128, null=False, blank=False)
    data_nascimento = models.DateField(null=False, blank=False)
    telefone = models.CharField ('Telefone', max_length=14, null=True, blank=True)
    valor_score = models.IntegerField('valor_score', default=0, null=True, blank=True)
    leito = models.IntegerField('leito', null=False, blank=False)
    nome_mae = models.CharField('Nome_da_mae', max_length=256, null=False, blank=False)

    def barScore(self):
        return self.valor_score * 10

class Score(Base):

    SIM_NAO = (
        ('S', 'Sim'),
        ('N', 'Nao'),
    )

    CONSCIENCIA = (
        ('A', 'Alerta'),
        ('V', 'Voz'),
        ('D', 'Dor'),
        ('NR', 'Nao responde'),
    )

    nivel_conciencia = models.CharField('Nivel_conciencia', choices=CONSCIENCIA, max_length=2, null=True,blank=True, default='A')
    temperatura = models.FloatField('Temperatura', default=36.1, null=True, blank=True)
    frequencia_cardiaca = models.IntegerField('Frequencia_cardiaca', default=51, null=True, blank=True)
    pa_sistolica = models.IntegerField('Pa_sistoliza', default= 111, null=True, blank=True)
    frequencia_respiratoria = models.IntegerField('Frequencia_respiratoria', default=12, null=True, blank=True)
    saturacao_oxigenio = models.IntegerField('Saturacao_de_oxigenio',default=96, null=True, blank=True)
    qualquer_o2 = models.CharField('Qualquer_suplemacao_o2', max_length=2, default='N', choices=SIM_NAO, null=True, blank=True)
    paciente = models.ForeignKey(Paciente, related_name='scores', on_delete=models.CASCADE, null=True, blank=True)
    profissional = models.ForeignKey(User, on_delete=models.CASCADE, related_name='avaliacoes')

    class Meta:
        ordering = ['-criado_em']

    def score_nivel_conciencia(self):
        if self.nivel_conciencia == 'A':
            return 0
        else:
            return 3

    def score_temperatura(self):
        if self.temperatura <= 35.0:
            return 3
        elif self.temperatura >= 35.1 and self.temperatura <= 36.0:
            return 1
        elif self.temperatura >= 36.1 and self.temperatura <= 38:
            return  0
        elif self.temperatura >= 38.1 and self.temperatura <= 39:
            return 1
        elif self.temperatura >= 39.1:
            return 2

    def score_freq_card(self):
        if self.frequencia_cardiaca <= 40:
            return 3
        elif self.frequencia_cardiaca >= 41 and self.frequencia_cardiaca <= 50:
            return 1
        elif self.frequencia_cardiaca >= 51 and self.frequencia_cardiaca <= 90:
            return 0
        elif self.frequencia_cardiaca >= 91 and self.frequencia_cardiaca <= 110:
            return 1
        elif self.frequencia_cardiaca >= 111 and self.frequencia_cardiaca <= 130:
            return 2
        elif self.frequencia_cardiaca >= 131:
            return 3

    def score_pa_sist(self):
        if self.pa_sistolica <= 90:
            return 3
        if self.pa_sistolica >= 91 and self.pa_sistolica <= 100:
            return 2
        if self.pa_sistolica >= 101 and self.pa_sistolica <= 110:
            return 1
        if self.pa_sistolica >= 111 and self.pa_sistolica <= 219:
            return 0
        if self.pa_sistolica >= 220:
            return 3

    def score_freq_resp(self):
        if self.frequencia_respiratoria < 8:
            return 3

        if self.frequencia_respiratoria >= 8 and self.frequencia_respiratoria <= 11:
            return 1

        if self.frequencia_respiratoria >= 12 and self.frequencia_respiratoria <= 20:
            return 0

        if self.frequencia_respiratoria >= 21 and self.frequencia_respiratoria <= 24:
            return 2

        if self.frequencia_respiratoria >= 25:
            return 3

    def score_sat_oxi(self):
        if self.saturacao_oxigenio <= 91:
            return 3

        if self.saturacao_oxigenio >= 92 and self.saturacao_oxigenio <= 93:
            return 2

        if self.saturacao_oxigenio >= 94 and self.saturacao_oxigenio <= 95:
            return 1
        if self.saturacao_oxigenio >= 96:
            return 0

    def score_q_supl_o2(self):
        if self.qualquer_o2 == 'S':
            return 2
        else:
            return 0

    def score(self):
        soma = self.score_nivel_conciencia() + \
               self.score_temperatura() + \
               self.score_pa_sist() + \
               self.score_freq_card() + \
               self.score_freq_resp() + \
               self.score_sat_oxi() + \
               self.score_q_supl_o2()
        return soma

    def __str__(self):
        return str(self.criado_em)

    def maior(self):
        if self.score_freq_card() == 3 \
                or self.score_freq_resp() == 3 \
                or self.score_nivel_conciencia() == 3 \
                or self.score_pa_sist() == 3 \
                or self.score_q_supl_o2() ==  3 \
                or self.score_sat_oxi() == 3 \
                or self.score_temperatura() == 3:
            return True
        else:
            return False



class Action(Base):

    escore_news = models.IntegerField('Escore_news', null=False, blank=False)
    frequencia = models.CharField('Frequencia de controle', max_length=255, null=False, blank=False)
    resposta = models.CharField('Resposta Clinica', max_length=512, null=False, blank=False)

# class Perfil(Base):
#
#
#     SEXO_CHOICES = (
#         ('M', 'Masculino'),
#         ('F', 'Feminino'),
#     )
#
#     CARGO = (
#         ('M', 'MEDICO'),
#         ('E', 'EMFERMEIRO'),
#         ('T', 'TECNICO'),
#     )
#
#     sexo = models.CharField('Sexo', max_length=16, choices=SEXO_CHOICES, blank=False, null=False)
#     telefone = models.CharField(max_length = 15, null = False, blank=False)
#     cargo = models.CharField(max_length = 255, null = False, blank=False)
#     data_nascimento = models.DateField(null=False, blank=False)
#     usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
#
#     class Meta:
#         verbose_name = 'Perfil'
#         verbose_name_plural = 'Perfis'
#
#     def __str__(self):
#         return "%s %s" % (self.nome(), self.sobrenome())
#
#     def nome(self):
#         return self.usuario.first_name
#
#     def sobrenome(self):
#         return self.usuario.last_name