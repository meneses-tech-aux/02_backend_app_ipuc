import requests
from core.config import settings

def verificar_usuario_paideia(username: str) -> dict | None:
    """
    Verifica si un usuario (DNI o código) existe en Paideia utilizando el wstoken.
    Retorna los datos del usuario si existe, o None si no existe o hay error.
    """
    url = settings.URL_PAIDEIA
    
    params = {
        "wstoken": settings.MOODLE_WS_TOKEN,
        "wsfunction": "core_user_get_users_by_field",
        "moodlewsrestformat": "json",
        "field": "username",
        "values[0]": username.strip()
    }

    try:
        response = requests.post(url, data=params, timeout=10)
        data = response.json()
        
        # Moodle devuelve una lista con los usuarios encontrados: [{'id': 123, 'username': '70055505', ...}]
        if isinstance(data, list) and len(data) > 0:
            return data[0]  # Retorna el primer usuario coincidente
            
        # Si devuelve un dict con 'exception' o 'errorcode', falló la llamada
        if isinstance(data, dict) and "exception" in data:
            print(f"Error devuelto por Moodle WS: {data.get('message')}")
            return None
            
        return None
        
    except Exception as e:
        print(f"Error al conectar con el WebService de Paideia: {e}")
        return None