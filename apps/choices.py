from django.db import models

class FarmerDocumentTypesChoices(models.TextChoices):
    CPF = "cpf", "cpf"
    CNPJ = "cnpj", "cnpj"
