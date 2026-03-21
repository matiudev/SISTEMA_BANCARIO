import re
# ======================================

def validar_rut(titulo="Ingrese rut: "):
    while True:
        rut = input(titulo)

        if not rut:
            print("❌ El RUT no puede estar vacío")
            continue

        # Limpiar
        rut = rut.strip().replace(".", "").replace(" ", "").upper()

        # Agregar guion si no existe
        if "-" not in rut and len(rut) > 1:
            rut = rut[:-1] + "-" + rut[-1]

        # Validar formato
        if not re.match(r"^\d{7,8}-[\dK]$", rut):
            print("❌ Formato de RUT inválido. Ej: 12345678-K")
            continue

        # Validar dígito verificador
        cuerpo, dv = rut.split("-")
        if not _verificar_dv(int(cuerpo), dv):
            print("❌ RUT inválido. El dígito verificador no corresponde.")
            continue

        return rut
    
def _verificar_dv(cuerpo, dv):
    suma = 0
    multiplo = 2

    while cuerpo != 0:
        suma += (cuerpo % 10) * multiplo
        cuerpo //= 10
        multiplo = multiplo + 1 if multiplo < 7 else 2

    resultado = 11 - (suma % 11)

    if resultado == 11:
        dv_calculado = "0"
    elif resultado == 10:
        dv_calculado = "K"
    else:
        dv_calculado = str(resultado)

    return dv == dv_calculado
# ======================================
# VALIDADORES
def validar_input_entero(mensaje, minimo=None, maximo=None):
    while True:
        try:
            valor = int(input(mensaje))
            if minimo is not None and valor < minimo:
                print(f"❌ Debe ser mayor o igual a {minimo}.")
                continue
            if maximo is not None and valor > maximo:
                print(f"❌ Debe ser menor o igual a {maximo}.")
                continue
            return valor
        except ValueError:
            print("❌ Debe ingresar un número entero.")

def validar_input_texto(mensaje, min_largo=1, max_largo=100):
    while True:
        valor = input(mensaje).strip()
        if len(valor) < min_largo:
            print(f"❌ Debe tener al menos {min_largo} caracteres.")
            continue
        if len(valor) > max_largo:
            print(f"❌ No puede superar {max_largo} caracteres.")
            continue
        return valor

def validar_input_fecha(mensaje):
    from datetime import datetime
    while True:
        valor = input(mensaje).strip()
        try:
            datetime.strptime(valor, "%Y-%m-%d")
            return valor
        except ValueError:
            print("❌ Formato inválido. Use YYYY-MM-DD (ej: 1999-05-14).")


# ======================================
def seleccionar_cuenta(cuentas, titulo="Seleccione cuenta: "):
    id_cta = input(titulo)
    
    if id_cta == "0":  # ← comparas string con string, no hay problema
        return None
    
    cuenta_valida = next((c for c in cuentas if str(c.id) == str(id_cta)), None)
    
    if not cuenta_valida:
        print("❌ Cuenta no válida o no te pertenece")
        return None
    
    return cuenta_valida


# ======================================
@staticmethod
def formato_clp(monto):
        return f"${monto:,.0f}".replace(",", ".")