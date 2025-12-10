# empleados/utils.py

def formatear_rut(rut):
    """
    Formatea un RUT chileno a la nomenclatura estándar: 12.345.678-K
    """
    if not rut:
        return ""
    # Limpia puntos y guion
    # Validación mínima
    rut = rut.upper().replace(".", "").replace("-", "")  
    if len(rut) < 2:  
        return rut
    # Separa cuerpo y dígito verificador
    cuerpo, dv = rut[:-1], rut[-1]                       
    
    # Agrega puntos cada 3 dígitos desde la derecha
    cuerpo_formateado = ""
    while len(cuerpo) > 3:
        cuerpo_formateado = "." + cuerpo[-3:] + cuerpo_formateado
        cuerpo = cuerpo[:-3]
    cuerpo_formateado = cuerpo + cuerpo_formateado
    return f"{cuerpo_formateado}-{dv}"
