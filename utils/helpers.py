from datetime import date

def formatear_fecha(fecha: date) -> str:
    """Retorna la fecha en formato DD/MM/YYYY"""
    if not fecha:
        return ""
    return fecha.strftime("%d/%m/%Y")