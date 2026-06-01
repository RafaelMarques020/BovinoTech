from django.contrib import admin
from .models import *

class AlertaInline(admin.TabularInline):
    model = Alerta
    extra = 0
    fields = ('tipo', 'mensagem', 'lido', 'data_alerta')
    readonly_fields = ('data_alerta',)

@admin.register(Vacinacao)
class VacinacaoAdmin(admin.ModelAdmin):
    inlines = [AlertaInline]

@admin.register(Medicamento)
class MedicamentoAdmin(admin.ModelAdmin):
    inlines = [AlertaInline]

@admin.register(ControleSanitario)
class ControleSanitarioAdmin(admin.ModelAdmin):
    inlines = [AlertaInline]

@admin.register(Alerta)
class AlertaAdmin(admin.ModelAdmin):
    fields = ('animal', 'tipo', 'mensagem', 'lido')
    list_display = ('tipo', 'animal', 'lido', 'data_alerta')

admin.site.register(ProducaoLeite)
admin.site.register(Animal)
admin.site.register(ControleReprodutivo)