import json
import pytest
import requests
from faker import Faker

fake = Faker('es_MX')

# Definir constantes
URL_BASE = "https://phplaravel-1214481-5270819.cloudwaysapps.com/api"

#Datos necesarios
LISTADO = {"fullType": "L"}

AREA = {
    "name": "Ventas"
}

AREA_EDITADA = {
    "name": fake.job()
}

def obtenerToken():
    response = requests.post(f"{URL_BASE}/adm-login", json={"email": "123456", "password": "12345678"})
    response.raise_for_status()
    datos = response.json()
    return datos['data']['token']

# Pruebas para la lectura de áreas
def test_obtener_areas():
    try:
        token = obtenerToken()
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{URL_BASE}/rolecategories", headers=headers, params=LISTADO)
        response.raise_for_status()
        datos = response.json()
        assert response.status_code == 200
        print(f"Áreas obtenidas: {json.dumps(datos['data'], indent=4)}")
    except requests.exceptions.HTTPError as err:
        print(f"Prueba fallida - {err}")

# Prueba para crear un área
@pytest.fixture(scope="module")
def crear_area():
    try:
        token = obtenerToken()
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(f"{URL_BASE}/rolecategories", json=AREA, headers=headers)
        response.raise_for_status()
        datos = response.json()
        assert response.status_code == 200
        print(f"Área creada con el ID: {datos['data']}")
        return datos['data']
    except requests.exceptions.HTTPError as err:
        print(f"Prueba fallida - {err}")

def test_buscar_area(crear_area):
    try:
        token = obtenerToken()
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{URL_BASE}/rolecategories/{crear_area}", headers=headers)
        response.raise_for_status()
        datos = response.json()
        assert response.status_code == 200
        print(f"Área buscada: {json.dumps(datos['data'], indent=4)}")
    except requests.exceptions.HTTPError as err:
        print(f"Prueba fallida - {err}")

# Prueba para editar un área
def test_editar_area(crear_area):
    try:
        token = obtenerToken()
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.put(f"{URL_BASE}/rolecategories/{crear_area}", json=AREA_EDITADA, headers=headers)
        response.raise_for_status()
        datos = response.json()
        assert response.status_code == 200
        assert datos['message'] == "Registro actualizado con éxito", "No se logró actualizar la área"
        print(f"Área editada: {json.dumps(datos, indent=4)}")
    except requests.exceptions.HTTPError as err:
        print(f"Prueba fallida - {err}")

# Prueba para eliminar un área
def test_eliminar_area(crear_area):
    try:
        token = obtenerToken()
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.delete(f"{URL_BASE}/rolecategories/{crear_area}", headers=headers)
        response.raise_for_status()
        datos = response.json()
        assert response.status_code == 200
        assert datos['message'] == "Registro eliminado con éxito", "No se logró eliminar la área"
    except requests.exceptions.HTTPError as err:
        print(f"Prueba fallida - {err}")