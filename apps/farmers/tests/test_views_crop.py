import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from model_bakery import baker
from apps.farmers.models import Crop, Harvest, Farm, Farmer
from validate_docbr import CPF

@pytest.mark.django_db
class TestCropViewSet:

    def setup_method(self):
        self.client = APIClient()
        self.farmer = Farmer.objects.create(
            name="Produtor",
            document_type="CPF",
            document_number=CPF().generate()
        )
        self.farm = Farm.objects.create(
            name="Fazenda Nova",
            city="Ribeirão Preto",
            state="SP",
            total_area=120,
            arable_area=90,
            vegetation_area=30,
            farmer=self.farmer
        )
        self.harvest = Harvest.objects.create(
            farm=self.farm,
            year=2025
        )

    def test_create_crop(self):
        url = reverse("crop-list")
        data = {
            "harvest": self.harvest.id,
            "name": "Soja",
            "area": 50
        }
        response = self.client.post(url, data, format="json")
        assert response.status_code == 201
        assert Crop.objects.count() == 1

    def test_list_crops(self):
        baker.make(Crop, harvest=self.harvest, _quantity=3)
        url = reverse("crop-list")
        response = self.client.get(url)
        assert response.status_code == 200
        assert len(response.data) == 3

    def test_retrieve_crop(self):
        crop = baker.make(Crop, harvest=self.harvest, name="Milho")
        url = reverse("crop-detail", args=[crop.id])
        response = self.client.get(url)
        assert response.status_code == 200
        assert response.data["name"] == "Milho"

    def test_update_crop(self):
        crop = baker.make(Crop, harvest=self.harvest, name="Feijão")
        url = reverse("crop-detail", args=[crop.id])
        data = {
            "harvest": self.harvest.id,
            "name": "Feijão Preto",
            "area": crop.area
        }
        response = self.client.put(url, data, format="json")
        assert response.status_code == 200
        crop.refresh_from_db()
        assert crop.name == "Feijão Preto"

    def test_delete_crop(self):
        crop = baker.make(Crop, harvest=self.harvest)
        url = reverse("crop-detail", args=[crop.id])
        response = self.client.delete(url)
        assert response.status_code == 204
        assert Crop.objects.count() == 0
