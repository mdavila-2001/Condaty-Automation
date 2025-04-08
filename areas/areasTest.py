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
    "title": fake.name(),
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

#Token para funciones de CRUD con los headers
def obtenerToken():
    response = requests.post(f"{URL_BASE}/adm-login", json={"email": "123456", "password": "12345678"})
    response.raise_for_status()
    datos = response.json()
    return datos['data']['token']

def test_listar_area():
    try:
        token = obtenerToken()
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{URL_BASE}/areas", headers=headers, params=LISTADO)
        response.raise_for_status()
        datos = response.json()
        assert "message" in datos, "La respuesta no contiene la clave 'message'"
        print("El GET funciona correctamente")
        print(json.dumps(datos['data'], indent=4))
    except requests.exceptions.HTTPError as e:
        pytest.fail(f"listar_areas: Prueba fallida - {e}")

@pytest.fixture(scope="module")
def crear_area():
    try:
        token = obtenerToken()
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(f"{URL_BASE}/areas", headers=headers, json=AREA_A_CREAR)
        response.raise_for_status()
        datos = response.json()
        assert datos['message'] == "Registro creado con éxito", "El area falló al crearse correctamente"
        print(f"Area creada con ID: {datos['data']}")
        return datos['data']
    except requests.exceptions.HTTPError as e:
        pytest.fail(f"crear_area: Prueba fallida - {e}")

def test_actualizar_area(crear_area):
    try:
        token = obtenerToken()
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.put(f"{URL_BASE}/areas/{crear_area}", headers=headers, json=AREA_A_EDITAR)
        response.raise_for_status()
        datos = response.json()
        assert datos['message'] == "Registro actualizado con éxito", "El area falló al actualizarse"
        print(json.dumps(datos['data'], indent=4))
        print(f"Area actualizada con ID: {crear_area}")
    except requests.exceptions.HTTPError as e:
        pytest.fail(f"actualizar_area: Prueba fallida - {e}")

def test_eliminar_area(crear_area):
    try:
        token = obtenerToken()
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.delete(f"{URL_BASE}/areas/{crear_area}", headers=headers)
        response.raise_for_status()
        datos = response.json()
        assert datos['message'] == "Registro eliminado con éxito", "El area falló al eliminarse"
        print(f"Area eliminada con ID: {crear_area}")
    except requests.exceptions.HTTPError as e:
        pytest.fail(f"eliminar_area: Prueba fallida - {e}")