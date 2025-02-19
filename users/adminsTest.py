import json
import pytest
import requests
from faker import Faker

fake = Faker('es_ES')

# URL base del backend
URL_BASE = "https://phplaravel-1214481-5270819.cloudwaysapps.com/api"

#Datos necesarios
LISTADO = {"fullType": "L"}
ADMIN_A_CREAR = {
    "ci": str(fake.random_number(digits=6)),
    "name": fake.first_name(),
    "middle_name": fake.first_name(),
    "last_name": fake.last_name(),
    "mother_last_name": fake.last_name(),
    "phone": "77441122",
    "role_id": 1,
    "email": fake.email(),
    "password": "12345678",
    "address": fake.address(),
}
ADMIN_A_ACTUALIZAR = {
    "name": fake.first_name(),
    "middle_name": fake.first_name(),
    "last_name": fake.last_name(),
    "mother_last_name": fake.last_name(),
    "phone": "77441122",
    "email": fake.email(),
    "address": fake.address()
}

#Token para funciones de CRUD
def obtenerToken():
    response = requests.post(f"{URL_BASE}/adm-login", json={"email": "123456", "password": "12345678"})
    response.raise_for_status()
    datos = response.json()
    return datos['data']['token']

#Prueba para listar a los usuarios
def test_listar_admins():
    try:
        token = obtenerToken()
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{URL_BASE}/users", headers=headers, params=LISTADO)
        response.raise_for_status()
        datos = response.json()
        assert "message" in datos, "La respuesta no contiene la clave 'message'"
        print("El GET funciona correctamente")
        print(json.dumps(datos['data'], indent=4))
    except requests.exceptions.HTTPError as e:
        pytest.fail(f"listar_usuarios: Prueba fallida - {e}")

#Prueba para crear un usuario
@pytest.fixture(scope="module")
def crear_admin():
    token = obtenerToken()
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(f"{URL_BASE}/users", json=ADMIN_A_CREAR, headers=headers)
        response.raise_for_status()
        datos = response.json()
        assert datos['message'] == "Registro creado con éxito", "El usuario falló al crearse"
        print(f"Usuario creado con ID: {datos['data']}")
        return datos['data']
    except requests.exceptions.HTTPError as e:
        pytest.fail(f"crear_usuario: Prueba fallida - {e}")

def test_llamar_admin(crear_admin):
    try:
        token = obtenerToken()
        params = {"fullType": "DET", "searchBy": crear_admin}
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{URL_BASE}/users", headers=headers, params=params)
        response.raise_for_status()
        datos = response.json()
        assert "data" in datos, "La respuesta no pudo traer los datos del usuario"
        print(json.dumps(datos['data'], indent=4))
    except requests.exceptions.HTTPError as e:
        pytest.fail(f"llamar_usuario: Prueba fallida - {e}")

#Prueba para actualizar un usuario
def test_actualizar_admin(crear_admin):
    try:
        token = obtenerToken()
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.put(f"{URL_BASE}/users/{crear_admin}", json=ADMIN_A_ACTUALIZAR, headers=headers)
        print(f"{URL_BASE}/users/{crear_admin}")
        response.raise_for_status()
        datos = response.json()
        assert datos['message'] == "Registro actualizado con éxito", "El usuario falló al actualizarse"
        print(f"Usuario actualizado con ID: {crear_admin}")
    except requests.exceptions.HTTPError as e:
        pytest.fail(f"actualizar_usuario: Prueba fallida - {e}")

#Prueba para eliminar un usuario

def test_eliminar_admin(crear_admin):
    try:
        token = obtenerToken()
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.delete(f"{URL_BASE}/users/{crear_admin}", headers=headers)
        response.raise_for_status()
        datos = response.json()
        assert datos['message'] == "Administrador Desvinculado", "El usuario falló al eliminarse"
        print(f"Usuario eliminado con ID: {crear_admin}")
    except requests.exceptions.HTTPError as e:
        pytest.fail(f"eliminar_usuario: Prueba fallida - {e}")