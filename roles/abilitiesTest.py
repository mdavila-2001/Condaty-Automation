import json
import pytest
import requests
from faker import Faker

fake = Faker('es_MX')

# Definir constantes
URL_BASE = "https://phplaravel-1214481-5270819.cloudwaysapps.com/api"

#Datos necesarios
LISTADO = {
    "fullType": "L",
    "page": 1,
    "perPage": -1
}

PERMISO = {
    "name": fake.word(),
    "description": "UsuarioE",
}

PERMISO_EDITADO = {
    "name": fake.word(),
    "description": "Test",
}

def obtenerToken():
    response = requests.post(f"{URL_BASE}/adm-login", json={"email": "123456", "password": "12345678"})
    response.raise_for_status()
    datos = response.json()
    return datos['data']['token']

# Pruebas para la lectura de permisos
def test_listar_permisos():
    try:
        token = obtenerToken()
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{URL_BASE}/abilities", headers=headers, params=LISTADO)
        response.raise_for_status()
        datos = response.json()
        assert response.status_code == 200
        print(f"Permisos obtenidos: {json.dumps(datos['data'], indent=4)}")
    except requests.exceptions.HTTPError as err:
        print(f"Prueba fallida - {err}")

# Prueba para crear un permiso
@pytest.fixture(scope="module")

def crear_permiso():
    try:
        token = obtenerToken()
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(f"{URL_BASE}/abilities", json=PERMISO, headers=headers)
        response.raise_for_status()
        datos = response.json()
        assert datos['message'] == "Registro creado con éxito", "El permiso falló al crearse"
        print(f"Permiso creado con ID: {datos['data']}")
        return datos['data']
    except requests.exceptions.HTTPError as err:
        pytest.fail(f"crear_permiso: Prueba fallida - {err}")

# Prueba para llamar al permiso
def test_llamar_permiso(crear_permiso):
    try:
        token = obtenerToken()
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{URL_BASE}/abilities/{crear_permiso}", headers=headers)
        response.raise_for_status()
        datos = response.json()
        print(f"Permiso encontrado: \n {json.dumps(datos['data'], indent=4)}")
    except requests.exceptions.HTTPError as err:
        pytest.fail(f"llamar_permiso: Prueba fallida - {err}")

# Prueba para editar un permiso

def test_actualizar_permiso(crear_permiso):
    try:
        token = obtenerToken()
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.put(f"{URL_BASE}/abilities/{crear_permiso}", json=PERMISO_EDITADO, headers=headers)
        response.raise_for_status()
        datos = response.json()
        assert datos['message'] == "Registro actualizado con éxito", "El permiso falló al actualizarse"
        print(f"Permiso actualizado con ID: {datos['data']}")
    except requests.exceptions.HTTPError as err:
        pytest.fail(f"actualizar_permiso: Prueba fallida - {err}")

# Prueba para eliminar un permiso
def test_eliminar_permiso(crear_permiso):
    try:
        token = obtenerToken()
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.delete(f"{URL_BASE}/abilities/{crear_permiso}", headers=headers)
        response.raise_for_status()
        datos = response.json()
        assert datos['message'] == "Registro eliminado con éxito", "El permiso falló al eliminarse"
        print(f"Permiso eliminado con ID: {crear_permiso}")
    except requests.exceptions.HTTPError as err:
        pytest.fail(f"eliminar_permiso: Prueba fallida - {err}")