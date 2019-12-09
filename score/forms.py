from django.forms import ModelForm, Select, NumberInput, DateTimeInput, TextInput, SelectDateWidget

from score.models import Paciente, Score

class PacienteForms(ModelForm):

    class Meta:

        model = Paciente
        fields = ('nome','data_nascimento','telefone','nome_mae','leito',)
        widgets = {
            'nome': TextInput(attrs={'class': 'form-control'}),
            'data_nascimento': DateTimeInput(attrs= {'class': 'form-control', 'type': 'date'}),
            'telefone': TextInput(attrs= {'class': 'form-control', 'placeholder': '(99) 99999999', 'data-mask':"(99) 99999999"}),
            'nome_mae': TextInput(attrs={'class': 'form-control'}),
            'leito': NumberInput(attrs={'class': 'form-control', 'type': 'number'}),
        }

class ScoreForms(ModelForm):

     class Meta:

         model = Score
         fields= ('nivel_conciencia','temperatura','frequencia_cardiaca','pa_sistolica', 'frequencia_respiratoria', 'saturacao_oxigenio', 'qualquer_o2','paciente',)
         widgets = {
             'nivel_conciencia': Select(attrs={'class': 'form-control'}),
             'temperatura': NumberInput(attrs={'class': 'form-control'}),
             'frequencia_cardiaca': NumberInput(attrs={'class': 'form-control'}),
             'pa_sistolica': NumberInput(attrs={'class': 'form-control'}),
             'frequencia_respiratoria': NumberInput(attrs={'class': 'form-control'}),
             'saturacao_oxigenio': NumberInput(attrs={'class': 'form-control'}),
             'qualquer_o2': Select(attrs={'class': 'form-control'}),
             }