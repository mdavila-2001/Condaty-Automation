import json
import pytest
import requests
from faker import Faker

fake = Faker('es_ES')

# URL base del backend
URL_BASE = "https://phplaravel-1214481-5270819.cloudwaysapps.com/api"

#Datos necesarios
LISTADO = {"fullType": "L"}
AREA_A_CREAR = {
    "title": fake.place_name(),
    "description": fake.sentence(),
    "max_capacity": 50,
    "days": "0111110",
    "is_free": fake.random_element(elements=("Y", "N")),
    "cancellation_policy": "Las cancelaciones deben hacerse con al menos 24 horas de anticipación.",
    "min_booking": 1,
    "max_cancel": 3,
    "penalty_fee": 20.00,
    "max_per_unit": 2,
    "usage_rules": fake.sentence(),
    "approval": fake.random_element(elements=("Y", "N"))
}
AREA_A_EDITAR = {
    "title": fake.first_name()
}

#Token para funciones de CRUD
def obtenerToken():
    response = requests.post(f"{URL_BASE}/adm-login", json={"email": "123456", "password": "12345678"})
    response.raise_for_status()
    datos = response.json()
    return datos['data']['token']