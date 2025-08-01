from django.db import models
from django.core.exceptions import ValidationError

from apps.choices import FarmerDocumentTypesChoices


class Farmer(models.Model):
    document_type: str = models.CharField(verbose_name="Tipo de documento", max_length=20, choices=FarmerDocumentTypesChoices, default=FarmerDocumentTypesChoices.CPF)
    document_number: str = models.CharField(max_length=20, unique=True)
    name: str = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


class Farm(models.Model):
    farmer: Farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name='farms')
    name: str = models.CharField(max_length=100)
    city: str = models.CharField(max_length=100)
    state: str = models.CharField(max_length=2)
    total_area: float = models.DecimalField(max_digits=10, decimal_places=2)
    arable_area: float = models.DecimalField(max_digits=10, decimal_places=2)
    vegetation_area: float = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        return self.name


class Harvest(models.Model):
    year: int = models.PositiveIntegerField()

    def __str__(self) -> str:
        return f'Harvest {self.year}'


class Crop(models.Model):
    name: str = models.CharField(max_length=100)
    farm: Farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='crops')
    harvest: Harvest = models.ForeignKey(Harvest, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.name} ({self.harvest.year})'
