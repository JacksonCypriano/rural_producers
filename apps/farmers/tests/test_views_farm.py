import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from model_bakery import baker
from apps.farmers.models import Farm, Farmer
from validate_docbr import CPF

@pytest.mark.django_db
class TestFarmViewSet:

    def setup_method(self):
        self.client = APIClient()
        self.farmer = Farmer.objects.create(
            name="Produtor 1",
            document_type="CPF",
            document_number=CPF().generate()
        )

    def test_create_farm_valid(self):
        url = reverse("farm-list")
        data = {
            "farmer": self.farmer.id,
            "name": "Fazenda Modelo",
            "city": "Limeira",
            "state": "SP",
            "total_area": 100,
            "arable_area": 60,
            "vegetation_area": 40
        }
        response = self.client.post(url, data, format="json")
        assert response.status_code == 201
        assert Farm.objects.count() == 1

    def test_list_farms(self):
        baker.make(Farm, farmer=self.farmer, _quantity=2)
        url = reverse("farm-list")
        response = self.client.get(url)
        assert response.status_code == 200
        assert len(response.data) == 2
