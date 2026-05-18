from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    
    # RF2: Animais
    path('animais/', views.lista_animais, name='lista_animais'),
    path('animais/criar/', views.criar_animal, name='criar_animal'),
    path('animais/<int:pk>/editar/', views.editar_animal, name='editar_animal'),
    path('animais/<int:pk>/deletar/', views.deletar_animal, name='deletar_animal'),
    
    # RF3: Lançar Produção
    path('producao/lancar/', views.lançar_producao, name='lancar_producao'),
    
    # RF4: Controle Individual
    path('controle-individual/', views.controle_individual, name='controle_individual'),
    
    # RF5: Histórico de Produção
    path('historico-producao/', views.historico_producao, name='historico_producao'),
    path('historico-producao/<int:pk>/editar/', views.editar_producao, name='editar_producao'),
    path('historico-producao/<int:pk>/deletar/', views.deletar_producao, name='deletar_producao'),
    
    # RF6: Vacinação
    path('vacinacao/', views.vacinacao, name='vacinacao'),
    path('vacinacao/criar/', views.criar_vacinacao, name='criar_vacinacao'),
    path('vacinacao/<int:pk>/editar/', views.editar_vacinacao, name='editar_vacinacao'),
    path('vacinacao/<int:pk>/deletar/', views.deletar_vacinacao, name='deletar_vacinacao'),
    
    # RF7: Medicamentos
    path('medicamentos/', views.medicamentos, name='medicamentos'),
    path('medicamentos/criar/', views.criar_medicamento, name='criar_medicamento'),
    path('medicamentos/<int:pk>/editar/', views.editar_medicamento, name='editar_medicamento'),
    path('medicamentos/<int:pk>/deletar/', views.deletar_medicamento, name='deletar_medicamento'),
    
    # RF8: Controle Sanitário
    path('sanitario/', views.controle_sanitario, name='sanitario'),
    path('sanitario/criar/', views.criar_sanitario, name='criar_sanitario'),
    path('sanitario/<int:pk>/editar/', views.editar_sanitario, name='editar_sanitario'),
    path('sanitario/<int:pk>/deletar/', views.deletar_sanitario, name='deletar_sanitario'),
    
    # RF9: Controle Reprodutivo
    path('reprodutivo/', views.controle_reprodutivo, name='reprodutivo'),
    path('reprodutivo/criar/', views.criar_reprodutivo, name='criar_reprodutivo'),
    path('reprodutivo/<int:pk>/editar/', views.editar_reprodutivo, name='editar_reprodutivo'),
    path('reprodutivo/<int:pk>/deletar/', views.deletar_reprodutivo, name='deletar_reprodutivo'),
    
    # RF10: Relatórios
    path('relatorios/', views.relatorios, name='relatorios'),
    
    # RF11: Alertas
    path('alertas/', views.lista_alertas, name='lista_alertas'),
    path('alertas/<int:pk>/lido/', views.marcar_alerta_como_lido, name='marcar_alerta_lido'),
]
