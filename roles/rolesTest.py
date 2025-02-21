import json
import pytest
import requests
from faker import Faker

fake = Faker('es_MX')

# Definir constantes
URL_BASE = "https://phplaravel-1214481-5270819.cloudwaysapps.com/api"

#Datos necesarios
LISTADO = {"fullType": "L"}
PERMISOS = {"fullType": "EXTRA"}

def obtenerToken():
    response = requests.post(f"{URL_BASE}/adm-login", json={"email": "123456", "password": "12345678"})
    response.raise_for_status()
    datos = response.json()
    return datos['data']['token']

# Prueba para listar roles
def test_listado_roles():
    try:
        token = obtenerToken()
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{URL_BASE}/roles", headers=headers)
        response.raise_for_status()
        datos = response.json()
        assert "message" in datos, "La response no contiene la clave 'message'"
    except requests.exceptions.HTTPError as e:
        pytest.fail(f"listado_roles: Prueba fallida - {e}")

# Prueba para crear un rol
@pytest.fixture(scope="module")
def crear_rol():
    try:
        token = obtenerToken()
        headers = {"Authorization": f"Bearer {token}"}
        datos_rol = {
            "rolecategory_id": 1,
            "name": fake.word(),
            "description": "Rol de prueba",
            "abilities": "test:R|profile:C|roles:R|"
        }
        response = requests.post(f"{URL_BASE}/roles", json=datos_rol, headers=headers)
        response.raise_for_status()
        datos = response.json()
        assert datos['message'] == "Registro creado con éxito", "El permiso falló al crearse"
        print(f"Rol creado con ID: {datos['data']}")
        return datos["data"]
    except requests.exceptions.HTTPError as e:
        pytest.fail(f"crear_rol: Prueba fallida - {e}")

# Prueba para listar un rol en específico
def test_llamar_rol(crear_rol):
    try:
        token = obtenerToken()
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{URL_BASE}/roles/{crear_rol}", headers=headers)
        response.raise_for_status()
        datos = response.json()
        info = datos['data']
        assert "message" in datos, "La response no contiene la clave 'message'"
        print(json.dumps(info, indent=4))
    except requests.exceptions.HTTPError as e:
        pytest.fail(f"llamar_roles: Prueba fallida - {e}")

# Prueba para editar un rol
def test_editar_rol(crear_rol):
    try:
        token = obtenerToken()
        headers = {"Authorization": f"Bearer {token}"}
        datos_edicion = {"description": "Prueba de Edicion"}
        response = requests.put(f"{URL_BASE}/roles/{crear_rol}", json=datos_edicion, headers=headers)
        response.raise_for_status()
        datos = response.json()
        assert "Debug_Querys" in datos, "La response no contiene la clave'Debug_Querys'"
    except requests.exceptions.HTTPError as e:
        pytest.fail(f"editar_rol: Prueba fallida - {e}")

# Prueba para eliminar un rol
def test_eliminar_rol(crear_rol):
    try:
        token = obtenerToken()
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.delete(f"{URL_BASE}/roles/{crear_rol}", headers=headers)
        response.raise_for_status()
        datos = response.json()
        assert response.status_code == 200
        assert datos["message"] == "Registro eliminado con éxito", f"El mensaje de respuesta es: {datos['message']}"
        print(f"Rol eliminado con éxito")
    except requests.exceptions.HTTPError as e:
        pytest.fail(f"eliminar_rol: Prueba fallida - {e}")