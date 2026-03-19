def sanitizar_rut(rut: str) -> str:
    """
    Normaliza un RUT chileno.

    Convierte:
        12.345.678-k
        12345678k
        12345678-K
        12345678k
        12345678 k

    En:
        12345678-K
    """

    if not rut:
        return ""

    # quitar espacios al inicio y final
    rut = rut.strip()

    # eliminar puntos y espacios internos
    rut = rut.replace(".", "").replace(" ", "")

    # convertir a mayúscula (k -> K)
    rut = rut.upper()

    # agregar guion si no existe
    if "-" not in rut and len(rut) > 1:
        rut = rut[:-1] + "-" + rut[-1]

    return rut