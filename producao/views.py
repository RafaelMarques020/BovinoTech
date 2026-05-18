from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum, Avg, Max
from .models import *
from .forms import *
from datetime import date, timedelta, datetime

def index(request):
    alertas = Alerta.objects.filter(lido=False).order_by('-data_alerta')[:5]
    total_alertas_nao_lidos = Alerta.objects.filter(lido=False).count()
    return render(request, 'producao/index.html', {'alertas': alertas, 'total_alertas': total_alertas_nao_lidos})

# RF2: Gerenciar Animais
def lista_animais(request):
    animais = Animal.objects.all()
    return render(request, 'producao/animais.html', {'animais': animais})

def criar_animal(request):
    if request.method == 'POST':
        form = AnimalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_animais')
    else:
        form = AnimalForm()
    return render(request, 'producao/criar_animal.html', {'form': form})

def editar_animal(request, pk):
    animal = get_object_or_404(Animal, pk=pk)
    if request.method == 'POST':
        form = AnimalForm(request.POST, instance=animal)
        if form.is_valid():
            form.save()
            return redirect('lista_animais')
    else:
        form = AnimalForm(instance=animal)
    return render(request, 'producao/editar_animal.html', {'form': form, 'animal': animal})

def deletar_animal(request, pk):
    animal = get_object_or_404(Animal, pk=pk)
    if request.method == 'POST':
        animal.delete()
        return redirect('lista_animais')
    return render(request, 'producao/deletar_animal.html', {'animal': animal})

# RF3: Lançamentos Diários de Ordenha
def lançar_producao(request):
    if request.method == 'POST':
        form = ProducaoLeiteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('historico_producao')
    else:
        # Sugerir a data de hoje por padrão
        form = ProducaoLeiteForm(initial={'data': date.today()})
    return render(request, 'producao/lancar_producao.html', {'form': form})

# RF4: Controle Individual de Produção (Foco Mensal)
def controle_individual(request):
    hoje = date.today()
    primeiro_dia_mes = hoje.replace(day=1)
    
    # Total produzido por cada vaca no mês atual
    animais = Animal.objects.annotate(
        total_produzido_mes=Sum('producoes__quantidade_litros', filter=models.Q(producoes__data__gte=primeiro_dia_mes))
    ).order_by('-total_produzido_mes')
    
    # Maior produção individual registrada no mês atual
    maior_producao_mes = ProducaoLeite.objects.filter(data__gte=primeiro_dia_mes).aggregate(Max('quantidade_litros'))['quantidade_litros__max']
    
    context = {
        'animais': animais,
        'maior_producao_mes': maior_producao_mes,
        'mes_atual': hoje.strftime('%B/%Y')
    }
    return render(request, 'producao/controle_individual.html', context)

# RF5: Histórico de Produção
def historico_producao(request):
    animal_id = request.GET.get('animal')
    if animal_id:
        historico = ProducaoLeite.objects.filter(animal_id=animal_id).order_by('-data')
    else:
        historico = ProducaoLeite.objects.all().order_by('-data')
    return render(request, 'producao/historico_producao.html', {'historico': historico})

def editar_producao(request, pk):
    producao = get_object_or_404(ProducaoLeite, pk=pk)
    if request.method == 'POST':
        form = ProducaoLeiteForm(request.POST, instance=producao)
        if form.is_valid():
            form.save()
            return redirect('historico_producao')
    else:
        form = ProducaoLeiteForm(instance=producao)
    return render(request, 'producao/editar_producao.html', {'form': form, 'producao': producao})

def deletar_producao(request, pk):
    producao = get_object_or_404(ProducaoLeite, pk=pk)
    if request.method == 'POST':
        producao.delete()
        return redirect('historico_producao')
    return render(request, 'producao/deletar_producao.html', {'producao': producao})

# RF6: Vacinação
def vacinacao(request):
    vacinas = Vacinacao.objects.all().order_by('-data_aplicacao')
    return render(request, 'producao/vacinacao.html', {'vacinas': vacinas})

def criar_vacinacao(request):
    if request.method == 'POST':
        form = VacinacaoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('vacinacao')
    else:
        form = VacinacaoForm(initial={'data_aplicacao': date.today()})
    return render(request, 'producao/criar_vacinacao.html', {'form': form})

def editar_vacinacao(request, pk):
    vacinacao = get_object_or_404(Vacinacao, pk=pk)
    if request.method == 'POST':
        form = VacinacaoForm(request.POST, instance=vacinacao)
        if form.is_valid():
            form.save()
            return redirect('vacinacao')
    else:
        form = VacinacaoForm(instance=vacinacao)
    return render(request, 'producao/editar_vacinacao.html', {'form': form, 'vacinacao': vacinacao})

def deletar_vacinacao(request, pk):
    vacinacao = get_object_or_404(Vacinacao, pk=pk)
    if request.method == 'POST':
        vacinacao.delete()
        return redirect('vacinacao')
    return render(request, 'producao/deletar_vacinacao.html', {'vacinacao': vacinacao})

# RF7: Medicamentos
def medicamentos(request):
    meds = Medicamento.objects.all().order_by('-data_inicio')
    return render(request, 'producao/medicamentos.html', {'medicamentos': meds, 'today': date.today()})

def criar_medicamento(request):
    if request.method == 'POST':
        form = MedicamentoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('medicamentos')
    else:
        form = MedicamentoForm(initial={'data_inicio': date.today()})
    return render(request, 'producao/criar_medicamento.html', {'form': form})

def editar_medicamento(request, pk):
    medicamento = get_object_or_404(Medicamento, pk=pk)
    if request.method == 'POST':
        form = MedicamentoForm(request.POST, instance=medicamento)
        if form.is_valid():
            form.save()
            return redirect('medicamentos')
    else:
        form = MedicamentoForm(instance=medicamento)
    return render(request, 'producao/editar_medicamento.html', {'form': form, 'medicamento': medicamento})

def deletar_medicamento(request, pk):
    medicamento = get_object_or_404(Medicamento, pk=pk)
    if request.method == 'POST':
        medicamento.delete()
        return redirect('medicamentos')
    return render(request, 'producao/deletar_medicamento.html', {'medicamento': medicamento})

# RF8: Controle Sanitário
def controle_sanitario(request):
    registros = ControleSanitario.objects.all().order_by('-data_registro')
    return render(request, 'producao/sanitario.html', {'registros': registros})

def criar_sanitario(request):
    if request.method == 'POST':
        form = ControleSanitarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sanitario')
    else:
        form = ControleSanitarioForm(initial={'data_registro': date.today()})
    return render(request, 'producao/criar_sanitario.html', {'form': form})

def editar_sanitario(request, pk):
    sanitario = get_object_or_404(ControleSanitario, pk=pk)
    if request.method == 'POST':
        form = ControleSanitarioForm(request.POST, instance=sanitario)
        if form.is_valid():
            form.save()
            return redirect('sanitario')
    else:
        form = ControleSanitarioForm(instance=sanitario)
    return render(request, 'producao/editar_sanitario.html', {'form': form, 'sanitario': sanitario})

def deletar_sanitario(request, pk):
    sanitario = get_object_or_404(ControleSanitario, pk=pk)
    if request.method == 'POST':
        sanitario.delete()
        return redirect('sanitario')
    return render(request, 'producao/deletar_sanitario.html', {'sanitario': sanitario})

# RF9: Controle Reprodutivo
def controle_reprodutivo(request):
    registros = ControleReprodutivo.objects.all().order_by('-data_evento')
    animais_femeas = Animal.objects.filter(sexo='F')
    return render(request, 'producao/reprodutivo.html', {
        'registros': registros,
        'animais_femeas': animais_femeas
    })

def criar_reprodutivo(request):
    animal_id = request.GET.get('animal')
    if request.method == 'POST':
        form = ControleReprodutivForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('reprodutivo')
    else:
        initial_data = {'data_evento': date.today()}
        if animal_id:
            initial_data['animal'] = animal_id
        form = ControleReprodutivForm(initial=initial_data)
    return render(request, 'producao/criar_reprodutivo.html', {'form': form})

def editar_reprodutivo(request, pk):
    reprodutivo = get_object_or_404(ControleReprodutivo, pk=pk)
    if request.method == 'POST':
        form = ControleReprodutivForm(request.POST, instance=reprodutivo)
        if form.is_valid():
            form.save()
            return redirect('reprodutivo')
    else:
        form = ControleReprodutivForm(instance=reprodutivo)
    return render(request, 'producao/editar_reprodutivo.html', {'form': form, 'reprodutivo': reprodutivo})

def deletar_reprodutivo(request, pk):
    reprodutivo = get_object_or_404(ControleReprodutivo, pk=pk)
    if request.method == 'POST':
        reprodutivo.delete()
        return redirect('reprodutivo')
    return render(request, 'producao/deletar_reprodutivo.html', {'reprodutivo': reprodutivo})

# RF10: Relatórios (Foco Mensal)
def relatorios(request):
    hoje = date.today()
    primeiro_dia_mes = hoje.replace(day=1)
    
    # Total produzido no mês atual
    total_mes = ProducaoLeite.objects.filter(data__gte=primeiro_dia_mes).aggregate(Sum('quantidade_litros'))['quantidade_litros__sum'] or 0
    
    # Ranking mensal
    ranking_mes = Animal.objects.annotate(
        total=Sum('producoes__quantidade_litros', filter=models.Q(producoes__data__gte=primeiro_dia_mes))
    ).filter(total__gt=0).order_by('-total')
    
    context = {
        'total_mes': total_mes,
        'mais_produtivas': ranking_mes[:5],
        'menos_produtivas': ranking_mes.reverse()[:5],
        'mes_atual': hoje.strftime('%B/%Y')
    }
    return render(request, 'producao/relatorios.html', context)

# RF11: Alertas
def lista_alertas(request):
    alertas = Alerta.objects.all().order_by('-data_alerta')
    return render(request, 'producao/alertas.html', {'alertas': alertas})

def marcar_alerta_como_lido(request, pk):
    alerta = get_object_or_404(Alerta, pk=pk)
    alerta.lido = True
    alerta.save()
    return redirect('lista_alertas')
