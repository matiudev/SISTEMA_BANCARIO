from db.init_db import get_connection
from utils.utils import validar_rut
from models.cliente import Cliente
from utils.utils import generar_numero_cuenta

class Cuenta:
    def __init__(self, id_cliente, id_tipo_cuenta, saldo=0.0, estado="Activa", id_cuenta=None):
        self.id_cuenta = id_cuenta
        self.id_cliente = id_cliente
        self.id_tipo_cuenta = id_tipo_cuenta
        self.saldo = saldo
        self.estado = estado


    @staticmethod
    def crear_cuenta():
        
        print("\n=== APERTURA DE NUEVA CUENTA ===")
        
        with get_connection() as connection:
            cursor = connection.cursor()
            
            # 1. MOSTRAR LISTA DE CLIENTES DISPONIBLES
            # Hacemos un JOIN con la tabla usuario para mostrar datos legibles
            query_clientes = """
                SELECT c.id, u.rut, u.nombre, u.apellido 
                FROM cliente c
                JOIN usuario u ON c.usuario_id = u.id
            """
            cursor.execute(query_clientes)
            clientes = cursor.fetchall()

            if not clientes:
                print("❌ No hay clientes registrados en el sistema. Debe crear uno primero.")
                return

            print(f"{'ID':<4} | {'RUT':<12} | {'NOMBRE COMPLETO'}")
            print("-" * 45)
            for cl in clientes:
                nombre_full = f"{cl[2]} {cl[3]}"
                print(f"{cl[0]:<4} | {cl[1]:<12} | {nombre_full}")
            
            # 2. SELECCIÓN DEL DUEÑO
            id_cliente = int(input("\nIngrese el ID del cliente de la lista superior: "))
            
            # 3. SELECCIÓN DE TIPO (Usando los IDs de tu tabla tipo_cuenta)
            print("\nTipos de cuenta: 1. Corriente | 2. Ahorro | 3. Vista")
            id_tipo = int(input("Seleccione el tipo de cuenta: "))
            nuevo_numero = Cuenta.generar_numero_cuenta(id_tipo)
            print(f"Número de cuenta: {nuevo_numero}")
            # 4. MONTO INICIAL
            try:
                monto_inicial = int(input("Monto de apertura (CLP): $"))
            except ValueError:
                print("❌ Monto inválido. Debe ser un número entero.")
                return
            
            # GENERAR NUMERO DE CUENTA
            num_cuenta = generar_numero_cuenta()

            # 5. EJECUCIÓN DE LA APERTURA
            try:
                # Insertar la cuenta
                query_insert = """
                    INSERT INTO cuentas (id_cliente, id_tipo_cuenta, numero_cuenta, saldo, estado)
                    VALUES (?, ?, ?, ?, 'ACTIVA')
                """
                cursor.execute(query_insert, (id_cliente, id_tipo, num_cuenta, monto_inicial))
                
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
                print(f"\n✅ Cuenta N°{id_nueva_cuenta} creada con éxito.")
                print(f"💰 Saldo inicial: {Cuenta.formato_clp(monto_inicial)}")
            
            except Exception as e:
                connection.rollback()
                print(f"❌ Error al crear la cuenta: {e}")

    @staticmethod
    def consultar_saldo(usuario_logueado):
        """
        usuario_logueado: Es el diccionario que devuelve tu Auth.login
        Contiene: usuario["id"], usuario["rol"], etc.
        """
        print("\n=== CONSULTA DE SALDO ===")
        
        with get_connection() as connection:
            cursor = connection.cursor()
            
            # Si es CLIENTE, primero le mostramos sus cuentas para que elija
            if usuario_logueado["rol"] == "cliente":
                query_lista = """
                    SELECT cta.id, tc.tipo_cuenta, cta.saldo 
                    FROM cuentas cta
                    JOIN tipo_cuenta tc ON cta.id_tipo_cuenta = tc.id
                    JOIN cliente c ON cta.id_cliente = c.id
                    WHERE c.usuario_id = ?
                """
                cursor.execute(query_lista, (usuario_logueado["id"],))
                mis_cuentas = cursor.fetchall()
                
                if not mis_cuentas:
                    print("❌ No tienes cuentas asociadas.")
                    return

                print("\nSeleccione una de sus cuentas:")
                for c in mis_cuentas:
                    print(f"ID Cuenta: {c[0]} | Tipo: {c[1]}")
                
                id_cta = input("\nIngrese el ID de la cuenta a detallar: ")
            
            else:
                id_cliente = input("Ingrese el ID del cliente: ")

                query_lista = """
                    SELECT cta.id, tc.tipo_cuenta, cta.saldo
                    FROM cuentas cta
                    JOIN tipo_cuenta tc ON cta.id_tipo_cuenta = tc.id
                    JOIN cliente c ON cta.id_cliente = c.id
                    WHERE cta.id_cliente = ?
                    """
                cursor.execute(query_lista, (id_cliente,))
                cuentas_cliente = cursor.fetchall()

                if not cuentas_cliente:
                    print("❌ El cliente no tiene cuentas.")
                    return

                print("\nCuentas del cliente:")
                for c in cuentas_cliente:
                    print(f"ID Cuenta: {c[0]} | Tipo: {c[1]}")

                id_cta = input("\nIngrese el ID de la cuenta a consultar: ")

            # Consulta final con JOIN para traer el nombre del tipo de cuenta
            query_detalle = """
                SELECT cta.saldo, tc.tipo_cuenta, cta.estado 
                FROM cuentas cta
                JOIN tipo_cuenta tc ON cta.id_tipo_cuenta = tc.id
                WHERE cta.id = ?
            """
            cursor.execute(query_detalle, (id_cta,))
            row = cursor.fetchone()

            if row:
                
                saldo_final = Cuenta.formato_clp(row[0])
                
                print(f"\n✅ Detalle Cuenta N°: {id_cta}")
                print(f"   Tipo: {row[1]}")
                print(f"   Estado: {row[2]}")
                print(f"   Saldo Actual: ${saldo_final}")
            else:
                print("❌ Cuenta no encontrada o no tiene permisos.")

    def obtener_cuentas_cliente(usuario_id):
        """
        Retorna una lista de las cuentas que pertenecen al usuario logueado.
        usuario_id: proviene del objeto 'usuario' obtenido en el login.
        """
        with get_connection() as connection:
            cursor = connection.cursor()
            #Buscamos las cuentas vinculando usuario -> cliente -> cuentas
            query = """
                SELECT cta.id, tc.tipo_cuenta, cta.saldo, cta.estado
                FROM cuentas cta
                JOIN tipo_cuenta tc ON cta.id_tipo_cuenta = tc.id
                JOIN cliente c ON cta.id_cliente = c.id
                WHERE c.usuario_id = ?
            """
            cursor.execute(query, (usuario_id,))
            return cursor.fetchall()
        
    @staticmethod

    def registrar_movimiento(connection, id_origen, tipo, monto, id_destino=None, glosa=""):
        """
        Registra un movimiento usando la misma conexión activa.
        """

        cursor = connection.cursor()

        query = """
        INSERT INTO movimientos
        (id_cuenta_origen, id_cuenta_destino, tipo_movimiento, monto, glosa)
            VALUES (?, ?, ?, ?, ?)
        """

        cursor.execute(query, (id_origen, id_destino, tipo, monto, glosa))

    @staticmethod
    def transferir_a_terceros(usuario_id):        
        with get_connection() as connection:
            cursor = connection.cursor()
            
            # 1. BUSCAR CUENTAS PERMITIDAS (Agregamos cta.estado al SELECT)
            query_origen = """
                SELECT cta.id, tc.tipo_cuenta, cta.saldo, cta.estado
                FROM cuentas cta
                JOIN tipo_cuenta tc ON cta.id_tipo_cuenta = tc.id
                JOIN cliente c ON cta.id_cliente = c.id
                WHERE c.usuario_id = ? AND tc.tipo_cuenta IN ('Corriente', 'Vista')
            """
            cursor.execute(query_origen, (usuario_id,))
            cuentas_disponibles = cursor.fetchall()

            if not cuentas_disponibles:
                print("\n❌ No posees cuentas (Corriente o Vista) habilitadas para transferir.")
                return

            print("\n=== SELECCIONE CUENTA DE ORIGEN ===")
            for i, c in enumerate(cuentas_disponibles, 1):
                print(f"{i}. {c[1]} - Saldo: ${c[2]:,.0f}".replace(",", "."))
            
            opcion = input("\nSeleccione una cuenta (o '0' para cancelar): ")
            if opcion == "0" or not opcion.isdigit() or int(opcion) > len(cuentas_disponibles):
                return

            cuenta_origen = cuentas_disponibles[int(opcion) - 1]
            id_origen = cuenta_origen[0]
            saldo_origen = cuenta_origen[2]
            estado_origen = cuenta_origen[3] # Guardamos el estado

            # --- VALIDACIÓN DE ESTADO AGREGADA ---
            if estado_origen != 'ACTIVA':
                print(f"\n❌ Operación cancelada. La cuenta seleccionada está {estado_origen}.")
                return
            # -------------------------------------

            # 2. IDENTIFICAR DESTINATARIO POR RUT
            print("\n--- DATOS DEL DESTINATARIO ---")
            rut_destino = validar_rut("Ingrese el RUT del destinatario: ")
            
            query_destinatario = """
                SELECT cta.id, u.nombre, u.apellido 
                FROM cuentas cta
                JOIN cliente c ON cta.id_cliente = c.id
                JOIN usuario u ON c.usuario_id = u.id
                WHERE u.rut = ? LIMIT 1
            """
            cursor.execute(query_destinatario, (rut_destino,))
            datos_destinio = cursor.fetchone()

            if not datos_destinio:
                print("❌ El RUT ingresado no existe en el sistema.")
                return

            id_cta_destino = datos_destinio[0]
            nombre_destinatario = f"{datos_destinio[1]} {datos_destinio[2]}"

            # 3. INGRESO Y VALIDACIÓN DE MONTO
            print(f"Destinatario: {nombre_destinatario}")
            monto = int(input("Ingrese monto a transferir (CLP): $"))

            if monto > saldo_origen:
                print(f"\n❌ Saldo insuficiente. Tu saldo es de ${saldo_origen:,.0f}".replace(",", "."))
                print("Volviendo al menú...")
                return

            # 4. EJECUCIÓN DE LA TRANSACCIÓN (Atómica)
            try:
                # Descontar de origen
                cursor.execute("UPDATE cuentas SET saldo = saldo - ? WHERE id = ?", (monto, id_origen))
                # Sumar a destino
                cursor.execute("UPDATE cuentas SET saldo = saldo + ? WHERE id = ?", (monto, id_cta_destino))
                # Obtener el rut del remitente
                cursor.execute("SELECT rut FROM usuario WHERE id = ?", (usuario_id,))
                rut_remitente = cursor.fetchone()[0]
                
                # Registrar el movimiento para el remitente
                Cuenta.registrar_movimiento(
                    connection,
                    id_origen,
                    'TRANSFERENCIA ENVIADA',
                    monto,
                    id_destino=id_cta_destino,
                    glosa=f"Transferencia a {nombre_destinatario}"
                )
                
                # Registrar el movimiento para el receptor
                Cuenta.registrar_movimiento(
                    connection,
                    id_cta_destino,
                    'TRANSFERENCIA RECIBIDA',
                    monto,
                    id_destino=id_origen,
                    glosa=f"Recibiste transferencia de RUT: {rut_remitente}"
                )

                connection.commit()
                print(f"\n✅ Transferencia exitosa de {Cuenta.formato_clp(monto)} a {nombre_destinatario}.")
            
            except Exception as e:
                connection.rollback()
                print(f"❌ Error procesando la transacción: {e}")
                
    
    @staticmethod
    def formato_clp(monto):
        return f"${monto:,.0f}".replace(",", ".")
    
    
    @staticmethod
    def ver_historial_cliente(usuario_id):        
        with get_connection() as connection:
            cursor = connection.cursor()
            
            # 1. LISTAR LAS CUENTAS DEL CLIENTE PARA QUE ELIJA
            query_cuentas = """
                SELECT cta.id, tc.tipo_cuenta, cta.saldo 
                FROM cuentas cta
                JOIN tipo_cuenta tc ON cta.id_tipo_cuenta = tc.id
                JOIN cliente c ON cta.id_cliente = c.id
                WHERE c.usuario_id = ?
            """
            cursor.execute(query_cuentas, (usuario_id,))
            mis_cuentas = cursor.fetchall()

            if not mis_cuentas:
                print("\n❌ No tienes cuentas asociadas para ver historial.")
                return

            print("\n=== SELECCIONE CUENTA PARA VER HISTORIAL ===")
            for i, c in enumerate(mis_cuentas, 1):
                print(f"{i}. {c[1]} (ID: {c[0]})")
            
            opcion = input("\nSeleccione una cuenta (o '0' para volver): ")
            if opcion == "0" or not opcion.isdigit() or int(opcion) > len(mis_cuentas):
                return

            # Obtenemos el ID de la cuenta elegida
            cuenta_seleccionada = mis_cuentas[int(opcion) - 1]
            id_cta_elegida = cuenta_seleccionada[0]
            nombre_tipo_cta = cuenta_seleccionada[1]

            # 2. MOSTRAR MOVIMIENTOS SOLO DE ESA CUENTA
            print(f"\n=== HISTORIAL: {nombre_tipo_cta.upper()} (ID: {id_cta_elegida}) ===")
            
            query_movimientos = """
                SELECT fecha, tipo_movimiento, monto, glosa
                FROM movimientos
                WHERE id_cuenta_origen = ?
                ORDER BY fecha DESC
            """
            cursor.execute(query_movimientos, (id_cta_elegida,))
            movimientos = cursor.fetchall()

            if not movimientos:
                print("No hay movimientos registrados en esta cuenta.")
                return

            print(f"{'FECHA':<20} | {'TIPO':<15} | {'MONTO':<12} | {'GLOSA'}")
            print("-" * 75)

            for m in movimientos:
                fecha = m[0]
                tipo = m[1]
                monto_clp = Cuenta.formato_clp(m[2])
                glosa = m[3] if m[3] else "---"
                
                print(f"{fecha:<20} | {tipo:<15} | {monto_clp:<12} | {glosa}")
            
            print("=" * 75)

    def obtener_cuentas_por_rut(rut):
        from utils.utils import validar_rut
        rut = validar_rut()

        with get_connection() as connection:
            cursor = connection.cursor()

            query = """
            SELECT cu.id, cu.saldo, cu.estado
            FROM cuentas cu
            JOIN cliente c ON cu.id_cliente = c.id
            JOIN usuario u ON c.usuario_id = u.id
            WHERE u.rut = ?
            """

            cursor.execute(query, (rut,))
            return cursor.fetchall()
        
    def mostrar_cliente_y_cuentas_por_rut(rut):
        rut = validar_rut()

        cliente = Cliente.buscar_por_rut(rut)

        if not cliente:
            print("Cliente no encontrado")
            return

        print("\n=== DATOS DEL CLIENTE ===")
        print(f"RUT: {cliente.rut}")
        print(f"Nombre: {cliente.nombres} {cliente.apellidos}")
        print(f"Teléfono: {cliente.telefono}")
        print(f"Correo: {cliente.correo}")

        cuentas = Cuenta.obtener_cuentas_por_rut(rut)

        print("\n=== CUENTAS ===")

        if cuentas:
         for c in cuentas:
            print(f"""
         Cuenta ID: {c[0]}
         Saldo: ${c[1]}
         Estado: {c[2]}
         ------------------------
         """)
        else:
            print("No tiene cuentas registradas")

