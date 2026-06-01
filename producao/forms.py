from django import forms
from .models import (
    Animal, ProducaoLeite, Vacinacao, Medicamento, 
    ControleSanitario, ControleReprodutivo, Alerta
)
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegistroForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class AnimalForm(forms.ModelForm):
    class Meta:
        model = Animal
        fields = ['identificacao', 'raca', 'data_nascimento', 'sexo']
        widgets = {
            'identificacao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Brinco ou Nome do Animal'}),
            'raca': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Holandesa'}),
            'data_nascimento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'sexo': forms.Select(attrs={'class': 'form-select'}),
        }

class ProducaoLeiteForm(forms.ModelForm):
    class Meta:
        model = ProducaoLeite
        fields = ['animal', 'data', 'periodo', 'quantidade_litros']
        widgets = {
            'animal': forms.Select(attrs={'class': 'form-select'}),
            'data': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'periodo': forms.Select(attrs={'class': 'form-select'}),
            'quantidade_litros': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantidade em litros', 'step': '0.01'}),
        }

class VacinacaoForm(forms.ModelForm):
    class Meta:
        model = Vacinacao
        fields = ['animal', 'tipo_vacina', 'lote', 'data_aplicacao', 'proxima_dose', 'tem_carencia', 'dias_carencia']
        widgets = {
            'animal': forms.Select(attrs={'class': 'form-select'}),
            'tipo_vacina': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Aftosa'}),
            'lote': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número do lote'}),
            'data_aplicacao': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'proxima_dose': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'tem_carencia': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'dias_carencia': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Dias'}),
        }

class MedicamentoForm(forms.ModelForm):
    class Meta:
        model = Medicamento
        fields = ['animal', 'nome_medicamento', 'dosagem', 'data_inicio', 'tem_carencia', 'periodo_carencia_dias', 'data_fim_carencia']
        widgets = {
            'animal': forms.Select(attrs={'class': 'form-select'}),
            'nome_medicamento': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do medicamento'}),
            'dosagem': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 500mg'}),
            'data_inicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'tem_carencia': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'periodo_carencia_dias': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Dias'}),
            'data_fim_carencia': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class ControleSanitarioForm(forms.ModelForm):
    class Meta:
        model = ControleSanitario
        fields = ['animal', 'exame_clinico', 'ocorrencia_doenca', 'medidas_preventivas', 'data_registro', 'tem_carencia', 'dias_carencia']
        widgets = {
            'animal': forms.Select(attrs={'class': 'form-select'}),
            'exame_clinico': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Resultado do exame'}),
            'ocorrencia_doenca': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Descreva a doença'}),
            'medidas_preventivas': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Medidas tomadas'}),
            'data_registro': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'tem_carencia': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'dias_carencia': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Dias'}),
        }

class ControleReprodutivForm(forms.ModelForm):
    class Meta:
        model = ControleReprodutivo
        fields = ['animal', 'tipo', 'data_evento', 'diagnostico_gestacao', 'previsao_parto']
        widgets = {
            'animal': forms.Select(attrs={'class': 'form-select'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'data_evento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'diagnostico_gestacao': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'previsao_parto': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
