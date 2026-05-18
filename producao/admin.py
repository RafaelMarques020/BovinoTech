from django.contrib import admin
from .models import *
from django.contrib import admin


admin.site.register(ProducaoLeite)
admin.site.register(Vacinacao)
admin.site.register(Medicamento)
admin.site.register(ControleSanitario)
admin.site.register(Alerta)

