import json
import pytest
import requests
from faker import Faker

fake = Faker('es_ES')

# URL base del backend
URL_BASE = "https://phplaravel-1214481-5270819.cloudwaysapps.com/api"

#Datos necesarios
LISTADO = {"fullType": "L"}
GUARDIA_A_CREAR = {
    "ci": str(fake.random_number(digits=6)),
    "name": fake.first_name(),
    "middle_name": fake.first_name(),
    "last_name": fake.last_name(),
    "mother_last_name": fake.last_name(),
    "prefix_phone": "+591",
    "phone": "77441122",
    "address": fake.address(),
    "email": fake.email()
}
GUARDIA_A_ACTUALIZAR = {
    "name": fake.first_name(),
    "middle_name": fake.first_name(),
    "last_name": fake.last_name(),
    "mother_last_name": fake.last_name(),
    "address": fake.address(),
    "phone": "77441122",
    "email": fake.email()
}

#Token para funciones de CRUD
def obtenerToken():
    response = requests.post(f"{URL_BASE}/adm-login", json={"email": "123456", "password": "12345678"})
    response.raise_for_status()
    datos = response.json()
    return datos['data']['token']

#Prueba para listar a las guardias
def test_listar_guardias():
    try:
        token = obtenerToken()
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{URL_BASE}/guards", headers=headers, params=LISTADO)
        response.raise_for_status()
        assert response.status_code == 200
        datos = response.json()
        assert "message" in datos, "La respuesta no contiene la clave 'message'"
        print("El GET funciona correctamente")
        print(json.dumps(datos['data'], indent=4))
    except requests.exceptions.HTTPError as e:
        pytest.fail(f"listar_guardias: Prueba fallida - {e}")

#Prueba para crear una guardia
@pytest.fixture(scope="module")

def crear_guardia():
    token = obtenerToken()
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{URL_BASE}/guards", headers=headers, json=GUARDIA_A_CREAR)
    response.raise_for_status()
    datos = response.json()
    assert datos['message'] == "Registro creado con éxito", "El guardia falló al crearse"
    print(f"Guardia creado con ID: {datos['data']}")
    return datos['data']

def test_llamar_guardia(crear_guardia):
    try:
        token = obtenerToken()
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{URL_BASE}/guards/{crear_guardia}", headers=headers)
        response.raise_for_status()
        datos = response.json()
        assert datos['message'] == "Show", "El guardia no fue localizado"
        print("Guardia creada y encontrada correctamente.")
    except requests.exceptions.HTTPError as e:
        pytest.fail(f"crear_guarderia: Prueba fallida - {e}")

#Prueba para actualizar una guardia
def test_editar_guardia(crear_guardia):
    try:
        token = obtenerToken()
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.put(f"{URL_BASE}/guards/{crear_guardia}", headers=headers, json=GUARDIA_A_ACTUALIZAR)
        response.raise_for_status()
        datos = response.json()
        assert datos['message'] == "Registro actualizado con éxito", "El guardia falló al actualizarse"
        print(f"Guardia actualizada con ID: {crear_guardia}")
    except requests.exceptions.HTTPError as e:
        pytest.fail(f"editar_guardia: Prueba fallida - {e}")

#Prueba para eliminar una guardia
def test_eliminar_guardia(crear_guardia):
    try:
        token = obtenerToken()
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.delete(f"{URL_BASE}/guards/{crear_guardia}", headers=headers)
        response.raise_for_status()
        datos = response.json()
        assert response.status_code == 200
        assert datos['message'] == "Guardia Desvinculado", "El guardia falló al eliminarse"
    except requests.exceptions.HTTPError as e:
        pytest.fail(f"eliminar_guardia: Prueba fallida - {e}")