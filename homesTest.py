import json
import pytest
import requests
from faker import Faker

fake = Faker('es_ES')

# URL base del backend
URL_BASE = "https://phplaravel-1214481-5270819.cloudwaysapps.com/api"

# Datos necesarios
LISTADO = {"fullType": "L"}

LISTADO_CON_TITULARES = {
    "fullType": "L",
    "filterBy": "C"
}

LISTADO_SIN_TITULARES = {
    "fullType": "L",
    "filterBy": "S"
}

DPTO_A_CREAR = {
    "nro": str(fake.random_number(digits=4)),
    "description": fake.text(),
    "expense_amount": fake.random_number(digits=2)+00,
    "dimension": fake.random_number(digits=3),
    "homeowner_id": ""
}

DPTO_A_EDITAR = {
    "nro": str(fake.random_number(digits=4)),
    "description": fake.text(),
    "expense_amount": fake.random_number(digits=2)+00,
    "dimension": fake.random_number(digits=3),
    "homeowner_id": ""
}

def obtenerToken():
    response = requests.post(f"{URL_BASE}/adm-login", json={"email": "123456", "password": "12345678"})
    response.raise_for_status()
    datos = response.json()
    return datos['data']['token']

def test_listar_dptos():
    try:
        token = obtenerToken()
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{URL_BASE}/dptos", params=LISTADO, headers=headers)
        response.raise_for_status()
        datos = response.json()
        assert len(datos['data']) > 0, "No se encontraron departamentos"
        print(f"Se encontraron {len(datos['data'])} departamentos")
        print(json.dumps(datos['data'], indent=4))
    except requests.exceptions.HTTPError as e:
        pytest.fail(f"listar_dptos: Prueba fallida - {e}")

@pytest.fixture(scope="module")
def crear_dpto():
    token = obtenerToken()
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{URL_BASE}/dptos", json=DPTO_A_CREAR, headers=headers)
    response.raise_for_status()
    datos = response.json()
    assert datos['message'] == "Registro creado con éxito", "El departamento falló al crearse"
    print(f"Departamento creado con ID: {datos['data']}")
    return datos['data']

def test_llamar_dpto(crear_dpto):
    try:
        token = obtenerToken()
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{URL_BASE}/dptos/{crear_dpto}", headers=headers)
        response.raise_for_status()
        datos = response.json()
        assert datos['message'] == "Show", "El departamento falló al obtenerse"
        print(f"Departamento obtenido con ID: {crear_dpto}")
        print(json.dumps(datos['data'], indent=4))
    except requests.exceptions.HTTPError as e:
        pytest.fail(f"llamar_dpto: Prueba fallida - {e}")

def test_listar_dptos_con_titulares():
    try:
        token = obtenerToken()
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{URL_BASE}/dptos", params=LISTADO_CON_TITULARES, headers=headers)
        response.raise_for_status()
        datos = response.json()
        assert len(datos['data']) > 0, "No se encontraron departamentos con titulares"
        print(f"Se encontraron {len(datos['data'])} departamentos con titulares")
        print(json.dumps(datos['data'], indent=4))
    except requests.exceptions.HTTPError as e:
        pytest.fail(f"listar_dptos_con_propietarios: Prueba fallida - {e}")

def test_listar_dptos_sin_titulares():
    try:
        token = obtenerToken()
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{URL_BASE}/dptos", params=LISTADO_SIN_TITULARES, headers=headers)
        response.raise_for_status()
        datos = response.json()
        assert len(datos['data']) > 0, "No se encontraron departamentos sin titulares"
        print(f"Se encontraron {len(datos['data'])} departamentos sin titulares.")
        print(json.dumps(datos['data'], indent=4))
    except requests.exceptions.HTTPError as e:
        pytest.fail(f"listar_dptos_sin_propietarios: Prueba fallida - {e}")

def test_actualizar_dpto(crear_dpto):
    try:
        token = obtenerToken()
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.put(f"{URL_BASE}/dptos/{crear_dpto}", json=DPTO_A_EDITAR, headers=headers)
        response.raise_for_status()
        datos = response.json()
        assert datos['message'] == "Registro actualizado con éxito", "El departamento falló al actualizarse"
        print(f"Departamento actualizado con ID")
    except requests.exceptions.HTTPError as e:
        pytest.fail(f"actualizar_dpto: Prueba fallida - {e}")

def test_eliminar_dpto(crear_dpto):
    try:
        token = obtenerToken()
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.delete(f"{URL_BASE}/dptos/{crear_dpto}", headers=headers)
        response.raise_for_status()
        datos = response.json()
        assert datos['message'] == "Casa desvinculada", "El departamento falló al eliminarse"
        print(f"Departamento eliminado con ID")
    except requests.exceptions.HTTPError as e:
        pytest.fail(f"eliminar_dpto: Prueba fallida - {e}")