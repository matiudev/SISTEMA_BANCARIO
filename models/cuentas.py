from db.init_db import get_connection
from utils.utils import validar_rut
from models.cliente import Cliente
import random
class Cuenta:
    def __init__(self, id_cliente, tipo_cuenta, numero_cuenta, saldo=0.0, estado="Activa", id=None, rut=None):
        self.id = id
        self.id_cliente = id_cliente
        self.rut = rut
        self.tipo_cuenta = tipo_cuenta
        self.numero_cuenta = numero_cuenta
        self.saldo = saldo
        self.estado = estado

    
    # --------- MÉTODOS DE INSTANCIA (self) ---------
    def __str__(self):
        return f"ID:{self.id} | {self.id_cliente} | {self.tipo_cuenta} | {self.numero_cuenta} | Saldo: ${self.saldo}"



    # --------- MÉTODOS DE ESTATICOS (staticmethod) ---------
    @staticmethod
    def obtener_cuentas_cliente(cliente_id):
        with get_connection() as connection:
            cursor = connection.cursor()

            query = """
                SELECT cta.id, cta.id_cliente, u.rut, tc.tipo_cuenta, cta.numero_cuenta, cta.saldo, cta.estado
                FROM cuentas cta
                JOIN tipo_cuenta tc ON cta.id_tipo_cuenta = tc.id
                JOIN cliente c ON cta.id_cliente = c.id
                JOIN usuario u ON c.usuario_id = u.id
                WHERE cta.id_cliente = ? AND cta.estado = "Activa"
            """
            cursor.execute(query, (cliente_id,))
            rows = cursor.fetchall()

            cuentas = []

            for row in rows:
                cuenta = Cuenta(
                    id=row[0],
                    id_cliente=row[1],   # id de la cuenta → espera, revisa tu query
                    rut=row[2],
                    tipo_cuenta=row[3],
                    numero_cuenta=row[4],
                    saldo=row[5],
                    estado=row[6],
                )
                cuentas.append(cuenta)

            return cuentas


    @staticmethod
    def crear_cuenta(cliente_id, id_tipo_cuenta, monto_inicial):
        with get_connection() as connection:
            cursor = connection.cursor()            
            numero_cuenta = Cuenta.generar_numero_cuenta(id_tipo_cuenta)
                # Insertar la cuenta
            query_insert = """
                    INSERT INTO cuentas (id_cliente, id_tipo_cuenta, numero_cuenta, saldo, estado)
                    VALUES (?, ?, ?, ?, 'Activa')
                """
            cursor.execute(query_insert, (cliente_id, id_tipo_cuenta, numero_cuenta, monto_inicial))
                
            id_nueva_cuenta = cursor.lastrowid

            # Registrar el movimiento inicial si hay dinero
            if monto_inicial > 0:
                # Usamos tu función auxiliar registrar_movimiento
                Cuenta.registrar_movimiento(
                        connection,
                        id_nueva_cuenta,
                        'DEPOSITO',
                        monto_inicial,
                        glosa="Apertura de cuenta"
                )

            connection.commit()
            return {"numero_cuenta": numero_cuenta, "monto": monto_inicial}
    
    
    @staticmethod
    def registrar_movimiento(connection, id_origen, tipo, monto, id_destino=None, glosa=""):
        cursor = connection.cursor()

        query = """
        INSERT INTO movimientos
        (id_cuenta_origen, id_cuenta_destino, tipo_movimiento, monto, glosa)
            VALUES (?, ?, ?, ?, ?)
        """

        cursor.execute(query, (id_origen, id_destino, tipo, monto, glosa))



    @staticmethod
    def buscar_cuenta(rut_destino):
        with get_connection() as connection:
            cursor = connection.cursor()

            query_destinatario = """
                SELECT cta.id, u.nombre, u.apellido, u.rut
                FROM cuentas cta
                JOIN cliente c ON cta.id_cliente = c.id
                JOIN usuario u ON c.usuario_id = u.id
                WHERE u.rut = ? LIMIT 1
            """

            cursor.execute(query_destinatario, (rut_destino,))
            cuenta_destino = cursor.fetchone()

        return cuenta_destino

    @staticmethod
    def transferir_a_terceros(usuario_id, id_cuenta_origen, id_cuenta_destino, monto, rut_remitente, nombre_destinatario):        
        with get_connection() as connection:
            cursor = connection.cursor()
            try:
                # Descontar de origen
                cursor.execute("UPDATE cuentas SET saldo = saldo - ? WHERE id = ?", (monto, id_cuenta_origen))
                # Sumar a destino
                cursor.execute("UPDATE cuentas SET saldo = saldo + ? WHERE id = ?", (monto, id_cuenta_destino))
                
                # Registrar el movimiento para el remitente
                Cuenta.registrar_movimiento(
                    connection, id_cuenta_origen, 'TRANSFERENCIA ENVIADA', 
                    monto, id_cuenta_destino, glosa=f"Transferencia a {nombre_destinatario}"
                )
                
                # Registrar el movimiento para el receptor
                Cuenta.registrar_movimiento(
                    connection, id_cuenta_destino, 'TRANSFERENCIA RECIBIDA',
                    monto, id_cuenta_origen, glosa=f"Recibiste transferencia de RUT: {rut_remitente}"
                )

                connection.commit()
            
            except Exception as e:
                connection.rollback()
    
    @staticmethod
    def obtener_historial_cliente(id_cuenta):        
        with get_connection() as connection:
            cursor = connection.cursor()
            
            query_movimientos = """
                SELECT fecha, tipo_movimiento, monto, glosa
                FROM movimientos
                WHERE id_cuenta_origen = ?
                ORDER BY fecha DESC
            """
            cursor.execute(query_movimientos, (id_cuenta,))
            movimientos = cursor.fetchall()

        return movimientos

    def obtener_cuentas_por_rut(rut):
        with get_connection() as connection:
            cursor = connection.cursor()

            query = """
            SELECT cu.id, cu.saldo, cu.estado, cu.numero_cuenta
            FROM cuentas cu
            JOIN cliente c ON cu.id_cliente = c.id
            JOIN usuario u ON c.usuario_id = u.id
            WHERE u.rut = ?
            """

            cursor.execute(query, (rut,))
            return cursor.fetchall()

    # --------- MÉTODOS DE INSTANCIA (self) ---------
    
    @staticmethod
    def generar_numero_cuenta(id_tipo):
        prefijos = {1: "CTE", 2: "AHO", 3: "VIS"}
        prefijo = prefijos.get(id_tipo, "CTA")

        with get_connection() as connection:
            cursor = connection.cursor()
            while True:
                numero = f"{prefijo}-{random.randint(10000000, 99999999)}"
                cursor.execute("SELECT id FROM cuentas WHERE numero_cuenta = ?", (numero,))
                if not cursor.fetchone():  # si no existe, es único
                    return numero
    