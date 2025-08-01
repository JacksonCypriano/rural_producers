from rest_framework import serializers
from apps.choices import FarmerDocumentTypesChoices
from .models import Farmer, Farm, Harvest, Crop
from validate_docbr import CPF, CNPJ
from datetime import datetime


class FarmerSerializer(serializers.ModelSerializer):
    def validate_document_type(self, value):
        value_lower = value.lower()
        valid_choices = [choice.value for choice in FarmerDocumentTypesChoices]
        if value_lower not in valid_choices:
            raise serializers.ValidationError(f"Tipo de documento inválido. Escolha entre {valid_choices}.")
        return value_lower

    def validate_document_number(self, value: str) -> str:
        document_type = self.initial_data.get("document_type")
        validator = CPF() if document_type == "CPF" else CNPJ()
        if not validator.validate(value):
            raise serializers.ValidationError(f"O número de documento '{value}' é inválido para o tipo {document_type}.")
        return value

    def validate_name(self, value: str) -> str:
        if not value.strip():
            raise serializers.ValidationError("O nome não pode estar vazio.")
        return value

    class Meta:
        model = Farmer
        fields = '__all__'


class FarmSerializer(serializers.ModelSerializer):
    def validate(self, data: dict) -> dict:
        arable_area = data.get('arable_area')
        vegetation_area = data.get('vegetation_area')
        total_area = data.get('total_area')

        if arable_area and vegetation_area and total_area:
            if (arable_area + vegetation_area) > total_area:
                raise serializers.ValidationError('A soma da área agricultável e da vegetação não pode exceder a área total.')
        return data

    def validate_name(self, value: str) -> str:
        if not value.strip():
            raise serializers.ValidationError("O nome da fazenda não pode estar vazio.")
        return value

    class Meta:
        model = Farm
        fields = '__all__'


class HarvestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Harvest
        fields = '__all__'


class CropSerializer(serializers.ModelSerializer):
    def validate_name(self, value: str) -> str:
        if not value.strip():
            raise serializers.ValidationError("O nome da cultura não pode estar vazio.")
        return value

    class Meta:
        model = Crop
        fields = '__all__'
