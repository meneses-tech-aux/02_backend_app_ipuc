import requests
from core.config import settings

def verificar_credenciales_paideia(username: str, password: str) -> bool:
    """
    Intenta obtener un token de usuario desde Moodle. 
    Si Moodle devuelve un token, la contraseña es correcta.
    Si devuelve un error, las credenciales son inválidas.
    """
    # Moodle siempre tiene este endpoint para apps externas
    # Asumiendo que settings.URL_PAIDEIA es "https://paideia.pucp.edu.pe"
    base_url = settings.URL_PAIDEIA.replace('/webservice/rest/server.php', '')
    url = f"{base_url}/login/token.php"
    
    params = {
        'username': username,
        'password': password,
        'service': 'moodle_mobile_app' # Servicio estándar de Moodle para apps
    }

    try:
        response = requests.post(url, data=params, timeout=10)
        data = response.json()
        
        # Si Moodle genera un token, el usuario es real y su clave es correcta
        if "token" in data:
            return True
        return False
    except Exception as e:
        print(f"Error al conectar con Paideia: {e}")
        return False