import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from model_bakery import baker
from validate_docbr import CPF
from apps.farmers.models import Farmer

@pytest.mark.django_db
class TestFarmerViewSet:

    def setup_method(self):
        self.client = APIClient()

    def test_list_farmers(self):
        baker.make(Farmer, _quantity=3)
        url = reverse("farmer-list")
        response = self.client.get(url)
        assert response.status_code == 200
        assert len(response.data) == 3

    def test_create_farmer_valid(self):
        url = reverse("farmer-list")
        data = {
            "document_type": "CPF",
            "document_number": CPF().generate(),
            "name": "Novo Produtor"
        }
        response = self.client.post(url, data, format="json")
        assert response.status_code == 201
        assert Farmer.objects.count() == 1

    def test_create_farmer_invalid_cpf(self):
        url = reverse("farmer-list")
        data = {
            "document_type": "CPF",
            "document_number": "12345678900",  # CPF inválido
            "name": "Produtor Inválido"
        }
        response = self.client.post(url, data, format="json")
        assert response.status_code == 400
        assert "document_number" in response.data

    def test_retrieve_farmer(self):
        farmer = baker.make(Farmer)
        url = reverse("farmer-detail", args=[farmer.id])
        response = self.client.get(url)
        assert response.status_code == 200
        assert response.data["id"] == farmer.id

    def test_update_farmer(self):
        farmer = baker.make(Farmer)
        url = reverse("farmer-detail", args=[farmer.id])
        data = {
            "document_type": farmer.document_type,
            "document_number": farmer.document_number,
            "name": "Nome Atualizado"
        }
        response = self.client.put(url, data, format="json")
        assert response.status_code == 200
        farmer.refresh_from_db()
        assert farmer.name == "Nome Atualizado"

    def test_delete_farmer(self):
        farmer = baker.make(Farmer)
        url = reverse("farmer-detail", args=[farmer.id])
        response = self.client.delete(url)
        assert response.status_code == 204
        assert Farmer.objects.count() == 0
