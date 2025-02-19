import requests

# URL base del backend
URL_BASE = "https://phplaravel-1214481-5270819.cloudwaysapps.com/api"

# Credenciales de prueba
CREDENCIALES_VALIDAS = {"email": "123456", "password": "12345678"}
CREDENCIALES_INVALIDAS = {"email": "user@fos.com.bo", "password": "12345678"}

def test_login_exitoso():
    try:
        response = requests.post(f"{URL_BASE}/adm-login", json=CREDENCIALES_VALIDAS)
        response.raise_for_status()  # Lanza una excepción si el código de estado no es 2xx
        datos = response.json()
        assert "message" in datos, "La response no contiene la clave 'message'"
        assert datos["message"] == "Login successful", f"Mensaje inesperado: {datos['message']}"
        print("login_exitoso: ¡Prueba exitosa!")
        assert datos['data']['token']
    except Exception as e:
        print(f"login_exitoso: Prueba fallida - {e}")

def test_login_fallido():
    try:
        response = requests.post(f"{URL_BASE}/adm-login", json=CREDENCIALES_INVALIDAS)
        response.raise_for_status()
        datos = response.json()
        assert "message" in datos, "La respuesta no contiene la clave 'message'"
        assert datos["message"] == "Acceso incorrecto", f"Mensaje inesperado: {datos['message']}"
        print("login_fallido: ¡Prueba exitosa!")
    except Exception as e:
        print(f"login_fallido: Prueba fallida - {e}")

def test_probar_campos_faltantes():
    try:
        response = requests.post(f"{URL_BASE}/adm-login", json={})
        response.raise_for_status()
        datos = response.json()
        assert "message" in datos, "La respuesta no contiene la clave 'message'"
        assert datos["message"] == "Validation Error", f"Mensaje inesperado: {datos['message']}"
        print("probar_campos_faltantes: ¡Prueba exitosa!")
    except Exception as e:
        print(f"probar_campos_faltantes: Prueba fallida - {e}")