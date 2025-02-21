import json
import pytest
import requests
from faker import Faker

fake = Faker('es_ES')

# URL base del backend
URL_BASE = "https://phplaravel-1214481-5270819.cloudwaysapps.com/api"

#Datos necesarios
LISTADO = {"fullType": "L"}
RESIDENTE_A_CREAR = {
    "ci": str(fake.random_number(digits=6)),
    "name": fake.first_name(),
    "middle_name": fake.first_name(),
    "last_name": fake.last_name(),
    "mother_last_name": fake.last_name(),
    "phone": "77441122",
    "address": fake.address(),
    "birthday": str(fake.date_of_birth()),
    "gender": fake.random_element(elements=("M", "F")),
    "email": fake.email(),
    "preunidad": "1",
    "client_id": 1
}
RESIDENTE_A_ACTUALIZAR = {
    "name": fake.first_name(),
    "middle_name": fake.first_name(),
    "last_name": fake.last_name(),
    "mother_last_name": fake.last_name(),
    "phone": "77441122",
    "email": fake.email()
}

#Token para funciones de CRUD
def obtenerToken():
    response = requests.post(f"{URL_BASE}/adm-login", json={"email": "123456", "password": "12345678"})
    response.raise_for_status()
    datos = response.json()
    return datos['data']['token']

#Prueba para listar a los usuarios
def test_listar_propietario():
    try:
        token = obtenerToken()
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{URL_BASE}/owner", headers=headers, params=LISTADO)
        response.raise_for_status()
        datos = response.json()
        assert "message" in datos, "La respuesta no contiene la clave 'message'"
        print("El GET funciona correctamente")
        print(json.dumps(datos['data'], indent=4))
    except requests.exceptions.HTTPError as e:
        pytest.fail(f"listar_usuarios: Prueba fallida - {e}")

#Prueba para crear un usuario
@pytest.fixture(scope="module")
def crear_propietario():
    token = obtenerToken()
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(f"{URL_BASE}/owner", json=RESIDENTE_A_CREAR, headers=headers)
        response.raise_for_status()
        datos = response.json()
        assert datos['message'] == "Registro creado con éxito", "El usuario falló al crearse"
        print(f"Usuario creado con ID: {datos['data']}")
        return datos['data']
    except requests.exceptions.HTTPError as e:
        pytest.fail(f"crear_usuario: Prueba fallida - {e}")

def test_llamar_propietario(crear_propietario):
    try:
        token = obtenerToken()
        params = {"fullType": "DET", "searchBy": crear_propietario}
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{URL_BASE}/owner", headers=headers, params=params)
        response.raise_for_status()
        datos = response.json()
        assert "data" in datos, "La respuesta no pudo traer los datos del usuario"
        print(json.dumps(datos['data'], indent=4))
    except requests.exceptions.HTTPError as e:
        pytest.fail(f"llamar_usuario: Prueba fallida - {e}")

#Prueba para actualizar un usuario
def test_actualizar_propietario(crear_propietario):
    try:
        token = obtenerToken()
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.put(f"{URL_BASE}/owner/{crear_propietario}", json=RESIDENTE_A_ACTUALIZAR, headers=headers)
        print(f"{URL_BASE}/users/{crear_propietario}")
        response.raise_for_status()
        datos = response.json()
        assert datos['message'] == "Registro actualizado con éxito", "El usuario falló al actualizarse"
        print(f"Usuario actualizado con ID: {crear_propietario}")
    except requests.exceptions.HTTPError as e:
        pytest.fail(f"actualizar_usuario: Prueba fallida - {e}")

#Prueba para eliminar un usuario

def test_eliminar_propietario(crear_propietario):
    try:
        token = obtenerToken()
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.delete(f"{URL_BASE}/owner/{crear_propietario}", headers=headers)
        response.raise_for_status()
        datos = response.json()
        assert datos['message'] == "Registro eliminado con éxito", "El usuario falló al eliminarse"
        print(f"Usuario eliminado con ID: {crear_propietario}")
    except requests.exceptions.HTTPError as e:
        pytest.fail(f"eliminar_usuario: Prueba fallida - {e}")