from django.contrib import admin
from .models import *

class AlertaInline(admin.TabularInline):
    model = Alerta
    extra = 0
    fields = ('tipo', 'mensagem', 'lido', 'data_alerta')
    readonly_fields = ('data_alerta',)

class ProducaoLeiteInline(admin.TabularInline):
    model = ProducaoLeite
    extra = 1
    fields = ('data', 'periodo', 'quantidade_litros')

class VacinacaoInline(admin.TabularInline):
    model = Vacinacao
    extra = 1

class MedicamentoInline(admin.TabularInline):
    model = Medicamento
    extra = 1

class ControleSanitarioInline(admin.TabularInline):
    model = ControleSanitario
    extra = 1

class ControleReprodutivoInline(admin.TabularInline):
    model = ControleReprodutivo
    extra = 1

@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ('identificacao', 'raca', 'data_nascimento', 'sexo')
    list_filter = ('sexo', 'raca')
    search_fields = ('identificacao',)
    inlines = [
        ProducaoLeiteInline, 
        VacinacaoInline, 
        MedicamentoInline, 
        ControleSanitarioInline, 
        ControleReprodutivoInline,
        AlertaInline
    ]

@admin.register(Vacinacao)
class VacinacaoAdmin(admin.ModelAdmin):
    list_display = ('animal', 'tipo_vacina', 'data_aplicacao', 'proxima_dose')
    list_filter = ('tipo_vacina', 'data_aplicacao')
    inlines = [AlertaInline]

@admin.register(Medicamento)
class MedicamentoAdmin(admin.ModelAdmin):
    list_display = ('animal', 'nome_medicamento', 'dosagem', 'data_inicio')
    list_filter = ('nome_medicamento', 'data_inicio')
    inlines = [AlertaInline]

@admin.register(ControleSanitario)
class ControleSanitarioAdmin(admin.ModelAdmin):
    list_display = ('animal', 'exame_clinico', 'data_registro')
    list_filter = ('data_registro',)
    inlines = [AlertaInline]

@admin.register(ControleReprodutivo)
class ControleReprodutivoAdmin(admin.ModelAdmin):
    list_display = ('animal', 'tipo', 'data_evento', 'diagnostico_gestacao')
    list_filter = ('tipo', 'diagnostico_gestacao')

@admin.register(Alerta)
class AlertaAdmin(admin.ModelAdmin):
    list_display = ('tipo', 'animal', 'lido', 'data_alerta')
    list_filter = ('tipo', 'lido', 'data_alerta')
    fields = ('animal', 'tipo', 'mensagem', 'lido')

@admin.register(ProducaoLeite)
class ProducaoLeiteAdmin(admin.ModelAdmin):
    list_display = ('animal', 'data', 'periodo', 'quantidade_litros')
    list_filter = ('data', 'periodo', 'animal')
