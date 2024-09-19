from django.db import models
from django.core.validators import RegexValidator

class Medico(models.Model):
    nome_medico = models.CharField(max_length=200)
    especializacao = models.CharField(max_length=200)
    crm = models.CharField(max_length=10)
    email = models.EmailField(max_length=50)
    telefone = models.CharField(
        max_length=15,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Número de telefone inválido")])
