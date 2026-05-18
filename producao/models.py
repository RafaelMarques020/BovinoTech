from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import timedelta

class PerfilUsuario(models.Model):
    PERFIL_CHOICES = [
        ('ADM', 'Administrador'),
        ('VET', 'Veterinário'),
        ('OPE', 'Operador'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    perfil = models.CharField(max_length=3, choices=PERFIL_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.get_perfil_display()}"

class Animal(models.Model):
    SEXO_CHOICES = [('M', 'Macho'), ('F', 'Fêmea')]
    identificacao = models.CharField(max_length=100, unique=True, verbose_name="Brinco/Nome")
    raca = models.CharField(max_length=100, verbose_name="Raça")
    data_nascimento = models.DateField(verbose_name="Data de Nascimento")
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES, verbose_name="Sexo")

    def __str__(self):
        return self.identificacao

class ProducaoLeite(models.Model):
    PERIODO_CHOICES = [('M', 'Manhã'), ('T', 'Tarde')]
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='producoes')
    data = models.DateField(verbose_name="Data da Coleta")
    periodo = models.CharField(max_length=1, choices=PERIODO_CHOICES, verbose_name="Período", default='M')
    quantidade_litros = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Quantidade (Litros)")

    def __str__(self):
        return f"{self.animal.identificacao} - {self.data} ({self.get_periodo_display()}) - {self.quantidade_litros}L"

class Vacinacao(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    tipo_vacina = models.CharField(max_length=100)
    lote = models.CharField(max_length=50)
    data_aplicacao = models.DateField()
    proxima_dose = models.DateField(null=True, blank=True)
    tem_carencia = models.BooleanField(default=False, verbose_name="Possui Carência?")
    dias_carencia = models.IntegerField(default=0, verbose_name="Dias de Carência")

    def __str__(self):
        return f"{self.animal.identificacao} - {self.tipo_vacina}"

class Medicamento(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    nome_medicamento = models.CharField(max_length=100)
    dosagem = models.CharField(max_length=50)
    data_inicio = models.DateField()
    tem_carencia = models.BooleanField(default=True, verbose_name="Possui Carência?")
    periodo_carencia_dias = models.IntegerField(default=0, help_text="Dias sem poder consumir o leite")
    data_fim_carencia = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.animal.identificacao} - {self.nome_medicamento}"

class ControleSanitario(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    exame_clinico = models.CharField(max_length=200)
    ocorrencia_doenca = models.TextField(blank=True)
    medidas_preventivas = models.TextField(blank=True)
    data_registro = models.DateField()
    tem_carencia = models.BooleanField(default=False, verbose_name="Possui Carência?")
    dias_carencia = models.IntegerField(default=0, verbose_name="Dias de Carência")

    def __str__(self):
        return f"{self.animal.identificacao} - {self.data_registro}"

class ControleReprodutivo(models.Model):
    TIPO_CHOICES = [('INS', 'Inseminação'), ('COB', 'Cobertura')]
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, limit_choices_to={'sexo': 'F'})
    tipo = models.CharField(max_length=3, choices=TIPO_CHOICES)
    data_evento = models.DateField()
    diagnostico_gestacao = models.BooleanField(default=False)
    previsao_parto = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.animal.identificacao} - {self.get_tipo_display()} - {self.data_evento}"

class Alerta(models.Model):
    TIPO_ALERTA = [
        ('VAC', 'Vacinação'),
        ('PAR', 'Parto'),
        ('PRO', 'Queda de Produção'),
        ('CAR', 'Carência'),
        ('SAN', 'Sanitário'),
    ]
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=3, choices=TIPO_ALERTA)
    mensagem = models.TextField()
    data_alerta = models.DateField(auto_now_add=True)
    lido = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.animal.identificacao}"


@receiver(post_save, sender=Vacinacao)
def alerta_vacinacao(sender, instance, created, **kwargs):
    if created:
        if instance.proxima_dose:
            Alerta.objects.create(
                animal=instance.animal,
                tipo='VAC',
                mensagem=f"Próxima dose da vacina {instance.tipo_vacina} agendada para {instance.proxima_dose.strftime('%d/%m/%Y')}."
            )
        if instance.tem_carencia and instance.dias_carencia > 0:
            data_liberacao = instance.data_aplicacao + timedelta(days=instance.dias_carencia)
            Alerta.objects.create(
                animal=instance.animal,
                tipo='CAR',
                mensagem=f"Animal em carência (Vacina: {instance.tipo_vacina}). Leite liberado em: {data_liberacao.strftime('%d/%m/%Y')}."
            )

@receiver(post_save, sender=Medicamento)
def alerta_medicamento(sender, instance, created, **kwargs):
    if created:
        if instance.tem_carencia and instance.periodo_carencia_dias > 0:
            data_liberacao = instance.data_inicio + timedelta(days=instance.periodo_carencia_dias)
            Alerta.objects.create(
                animal=instance.animal,
                tipo='CAR',
                mensagem=f"Animal em carência (Medicamento: {instance.nome_medicamento}). Leite liberado em: {data_liberacao.strftime('%d/%m/%Y')}."
            )

@receiver(post_save, sender=ControleSanitario)
def alerta_sanitario(sender, instance, created, **kwargs):
    if created:
        if instance.ocorrencia_doenca:
            Alerta.objects.create(
                animal=instance.animal,
                tipo='SAN',
                mensagem=f"Ocorrência de doença registrada: {instance.ocorrencia_doenca}."
            )
        if instance.tem_carencia and instance.dias_carencia > 0:
            data_liberacao = instance.data_registro + timedelta(days=instance.dias_carencia)
            Alerta.objects.create(
                animal=instance.animal,
                tipo='CAR',
                mensagem=f"Animal em carência (Tratamento Sanitário). Leite liberado em: {data_liberacao.strftime('%d/%m/%Y')}."
            )

@receiver(post_save, sender=ControleReprodutivo)
def alerta_reprodutivo(sender, instance, created, **kwargs):
    if created or instance.diagnostico_gestacao:
        if instance.diagnostico_gestacao and instance.previsao_parto:
            Alerta.objects.create(
                animal=instance.animal,
                tipo='PAR',
                mensagem=f"Gestação confirmada! Previsão de parto para {instance.previsao_parto.strftime('%d/%m/%Y')}."
            )
