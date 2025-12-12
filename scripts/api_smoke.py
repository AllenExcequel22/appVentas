import requests
import json
import time

BASE = 'http://127.0.0.1:8000'

# Datos de prueba
USERNAME = 'apitest'
PASSWORD = 'Test1234!'
EMAIL = 'api@test.local'

session = requests.Session()

def request_with_retries(method, url, max_retries=6, delay=1, **kwargs):
    """Realiza una petición con reintentos para esperar a que el servidor esté listo."""
    for attempt in range(1, max_retries+1):
        try:
            resp = session.request(method, url, timeout=5, **kwargs)
            return resp
        except requests.exceptions.RequestException as e:
            if attempt == max_retries:
                raise
            print(f'Reintento {attempt}/{max_retries} — esperando servidor...')
            time.sleep(delay)


print('Esperando servidor y ejecutando pruebas...')

# 1) Registrar usuario (puede devolver error si ya existe)
print('--- REGISTER ---')
resp = request_with_retries('POST', f'{BASE}/api/v1/register/', json={'username': USERNAME, 'password': PASSWORD, 'email': EMAIL})
print(resp.status_code)
try:
    print(json.dumps(resp.json(), indent=2, ensure_ascii=False))
except Exception:
    print(resp.text)

# 2) Obtener token
print('\n--- TOKEN ---')
resp = request_with_retries('POST', f'{BASE}/api/v1/token/', data={'username': USERNAME, 'password': PASSWORD})
print(resp.status_code)
try:
    token_data = resp.json()
    print(json.dumps(token_data, indent=2, ensure_ascii=False))
except Exception:
    print(resp.text)
    token_data = {}

access = token_data.get('access')
if not access:
    print('\nNo se obtuvo token de acceso. Si el usuario ya existía prueba a iniciar sesión manualmente.')
else:
    headers = {'Authorization': f'Bearer {access}'}
    # 3) Listar clientes
    print('\n--- CLIENTES (protegido) ---')
    resp = request_with_retries('GET', f'{BASE}/api/v1/clientes/', headers=headers)
    print(resp.status_code)
    try:
        print(json.dumps(resp.json(), indent=2, ensure_ascii=False))
    except Exception:
        print(resp.text)

    # 4) Listar productos
    print('\n--- PRODUCTOS (protegido) ---')
    resp = request_with_retries('GET', f'{BASE}/api/v1/productos/', headers=headers)
    print(resp.status_code)
    try:
        print(json.dumps(resp.json(), indent=2, ensure_ascii=False))
    except Exception:
        print(resp.text)

print('\nPruebas finalizadas.')
