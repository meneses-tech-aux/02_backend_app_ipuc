import requests
from core.config import settings

def obtener_token_temporal() -> str:
    """
    Paso 1: Genera el token temporal para el servicio wsmatricula
    usando el token maestro configurado en settings.MOODLE_WS_TOKEN.
    """
    params = {
        "wstoken": settings.MOODLE_WS_TOKEN,
        "wsfunction": "tool_token_get_token",
        "moodlewsrestformat": "json",
        "service": "wsmatricula",
        "idtype": "username",
        "idvalue": "wsusermatricula"
    }

    response = requests.post(settings.URL_PAIDEIA, data=params, timeout=10)
    response.raise_for_status()
    data = response.json()

    if isinstance(data, dict) and "token" in data:
        return data["token"]

    raise Exception(f"No se pudo generar el token temporal: {data}")


def verificar_usuario_paideia(username: str) -> dict | None:
    """
    Paso 2: Usa el token temporal generado para consultar el usuario por DNI/código.
    """
    try:
        # 1. Obtener token temporal
        token_temporal = obtener_token_temporal()

        # 2. Consultar usuario con el token temporal
        params = {
            "wstoken": token_temporal,
            "wsfunction": "core_user_get_users_by_field",
            "moodlewsrestformat": "json",
            "field": "username",
            "values[0]": str(username).strip()
        }

        response = requests.post(settings.URL_PAIDEIA, data=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if isinstance(data, list) and len(data) > 0:
            return data[0]

        return None

    except Exception as e:
        print(f"Error en Paideia: {e}")
        return None