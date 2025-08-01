import pytest
from apps.farmers.models import Farmer, Farm, Harvest, Crop
from validate_docbr import CPF

@pytest.mark.django_db
def test_create_farmer():
    farmer = Farmer.objects.create(
        document_type="CPF",
        document_number=CPF().generate(),
        name="João Agricultor"
    )
    assert Farmer.objects.count() == 1
    assert farmer.name == "João Agricultor"

@pytest.mark.django_db
def test_create_farm_linked_to_farmer():
    farmer = Farmer.objects.create(
        document_type="CPF",
        document_number=CPF().generate(),
        name="Produtora Maria"
    )
    farm = Farm.objects.create(
        farmer=farmer,
        name="Fazenda Nova",
        city="Londrina",
        state="PR",
        total_area=120,
        arable_area=80,
        vegetation_area=40
    )
    assert farm.farmer == farmer
    assert farmer.farms.count() == 1
