import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from model_bakery import baker
from apps.farmers.models import Harvest, Farm, Farmer
from validate_docbr import CPF

@pytest.mark.django_db
class TestHarvestViewSet:

    def setup_method(self):
        self.client = APIClient()
        self.farmer = Farmer.objects.create(
            name="Produtor",
            document_type="CPF",
            document_number=CPF().generate()
        )
        self.farm = Farm.objects.create(
            name="Fazenda Modelo",
            city="Uberlândia",
            state="MG",
            total_area=100,
            arable_area=70,
            vegetation_area=30,
            farmer=self.farmer
        )

    def test_create_harvest(self):
        url = reverse("harvest-list")
        data = {
            "farm": self.farm.id,
            "year": 2025
        }
        response = self.client.post(url, data, format="json")
        assert response.status_code == 201
        assert Harvest.objects.count() == 1

    def test_list_harvests(self):
        baker.make(Harvest, farm=self.farm, _quantity=2, year=2025)
        url = reverse("harvest-list")
        response = self.client.get(url)
        assert response.status_code == 200
        assert len(response.data) == 2

    def test_retrieve_harvest(self):
        harvest = baker.make(Harvest, farm=self.farm, year=2024)
        url = reverse("harvest-detail", args=[harvest.id])
        response = self.client.get(url)
        assert response.status_code == 200
        assert response.data["year"] == 2024

    def test_update_harvest(self):
        harvest = baker.make(Harvest, farm=self.farm, year=2023)
        url = reverse("harvest-detail", args=[harvest.id])
        data = {
            "farm": self.farm.id,
            "year": 2026
        }
        response = self.client.put(url, data, format="json")
        assert response.status_code == 200
        harvest.refresh_from_db()
        assert harvest.year == 2026

    def test_delete_harvest(self):
        harvest = baker.make(Harvest, farm=self.farm)
        url = reverse("harvest-detail", args=[harvest.id])
        response = self.client.delete(url)
        assert response.status_code == 204
        assert Harvest.objects.count() == 0
