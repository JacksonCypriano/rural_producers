import pytest
from apps.farmers.serializers import FarmerSerializer, FarmSerializer
from apps.farmers.models import Farmer
from validate_docbr import CPF, CNPJ

@pytest.mark.django_db
class TestFarmerSerializer:
    def test_valid_cpf(self):
        cpf = CPF().generate()
        data = {
            "document_type": "CPF",
            "document_number": cpf,
            "name": "João da Silva"
        }
        serializer = FarmerSerializer(data=data)
        assert serializer.is_valid(), serializer.errors

    def test_invalid_cnpj(self):
        data = {
            "document_type": "CNPJ",
            "document_number": "12345678901234",
            "name": "Agro LTDA"
        }
        serializer = FarmerSerializer(data=data)
        assert not serializer.is_valid()
        assert "document_number" in serializer.errors

    def test_empty_name(self):
        cpf = CPF().generate()
        data = {
            "document_type": "CPF",
            "document_number": cpf,
            "name": "   "
        }
        serializer = FarmerSerializer(data=data)
        assert not serializer.is_valid()
        assert "name" in serializer.errors


@pytest.mark.django_db
class TestFarmSerializer:
    @pytest.fixture
    def farmer(self):
        return Farmer.objects.create(
            document_type="CPF",
            document_number=CPF().generate(),
            name="Maria Produtora"
        )

    def test_valid_farm(self, farmer):
        data = {
            "farmer": farmer.id,
            "name": "Fazenda Boa Vista",
            "city": "Uberlândia",
            "state": "MG",
            "total_area": 100.00,
            "arable_area": 60.00,
            "vegetation_area": 40.00
        }
        serializer = FarmSerializer(data=data)
        assert serializer.is_valid(), serializer.errors

    def test_invalid_area_sum(self, farmer):
        data = {
            "farmer": farmer.id,
            "name": "Fazenda Verde",
            "city": "Patos de Minas",
            "state": "MG",
            "total_area": 80.00,
            "arable_area": 60.00,
            "vegetation_area": 30.00
        }
        serializer = FarmSerializer(data=data)
        assert not serializer.is_valid()
        assert "non_field_errors" in serializer.errors
