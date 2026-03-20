import re
import random

# ======================================

def validar_rut(titulo = "Ingrese rut: "):
    """
    Normaliza y valida un RUT chileno.
    Retorna el RUT en formato 12345678-K
    """

    while True:
        rut = input(titulo)

        if not rut:
            print("❌ El RUT no puede estar vacío")
            continue

        # limpiar
        rut = rut.strip().replace(".", "").replace(" ", "").upper()

        # agregar guion si no existe
        if "-" not in rut and len(rut) > 1:
            rut = rut[:-1] + "-" + rut[-1]

        # validar formato (números + guion + dígito o K)
        if not re.match(r"^\d{7,8}-[\dK]$", rut):
            print("❌ Formato de RUT inválido. Ej: 12345678-K")
            continue

        return rut
# ======================================

def generar_numero_cuenta(id_tipo_cuenta):
    from db.init_db import get_connection
        
    # Mapeo de prefijos según el ID del tipo de cuenta
    prefijos = {
        1: "100", # Corriente
        2: "200", # Vista
        3: "300"  # Ahorro
    }
        
    # Obtenemos el prefijo o usamos uno genérico (900) si el ID no coincide
    prefijo = prefijos.get(id_tipo_cuenta, "900")
        
    with get_connection() as connection:
        cursor = connection.cursor()
            
    while True:
            # Generamos 7 dígitos aleatorios para completar 10
            aleatorio = "".join([str(random.randint(0, 9)) for _ in range(7)])
            numero_propuesto = prefijo + aleatorio
                
            # Verificación de unicidad en la base de datos
            cursor.execute("SELECT 1 FROM cuentas WHERE numero_cuenta = ?", (numero_propuesto,))
                
            if not cursor.fetchone():
                return numero_propuesto