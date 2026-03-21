from models.cliente import Cliente
from models.cuentas import Cuenta
from models.auth import Auth
from utils.utils import validar_rut, validar_input_entero, validar_input_fecha, validar_input_texto
from models.cliente import Cliente
from models.cuentas import Cuenta
import getpass
from utils.utils import seleccionar_cuenta, formato_clp


class Menu:
    def menu_principal(self):
        while True:
            print("\n==============================")
            print("      SISTEMA BANCARIO")
            print("==============================")

            print("\n--- AUTENTICACIÓN ---")

            try:
                rut = validar_rut()
                password = getpass.getpass("Ingrese su Contraseña: ")
            except (KeyboardInterrupt, EOFError):
                continue


            usuario = Auth.login(rut, password)

            if not usuario:
                print("❌ RUT o contraseña incorrectos")
                continue
            
            print("✅ Inicio de sesión Exitoso!")
            print(f"Bienvenido {usuario['nombre']}")

            rol = usuario["rol"]

            if rol == "cliente":
                self.menu_cliente(usuario)
            elif rol == "empleado":
                self.menu_empleado(usuario)
            
            # elif rol == "gerente":
            #     Menu.menu_gerente()


    def menu_empleado(self, usuario):
        while True:
            print("\n--- MENU EMPLEADO ---")
            print("1. Registrar Cliente")
            print("2. Crear Cuenta")
            print("3. Consultar Saldo")
            print("4. Listar Clientes")
            print("5. Consulta cliente y cuenta")
            print("0. Cerrar Sesión")

            opcion = validar_input_entero("Seleccione una opción: ", 0, 5)

            match opcion:
                case 1:
                    self.registrar_cliente()
                case 2:
                    self.crear_cuenta()
                case 3:
                    self.consultar_saldo(usuario)
                case 4:
                    clientes = Cliente.obtener_clientes()

                    if not clientes:
                        print("❌ No hay clientes")

                    self.listar_clientes(clientes)
                case 5:
                    self.info_cliente()
                case 0:
                    return


    def menu_cliente(self, usuario):
        while True:
            print("\n--- MENU CLIENTE ---")
            print("1. Consultar Saldo")
            print("2. Ver Historial de movimientos")
            print("3. Transferir a otras cuentas")
            print("0. Cerrar Sesión")

            opcion = validar_input_entero("Seleccione una opción: ", 0, 3)

            match opcion:
                case 1:
                    self.consultar_saldo(usuario)
                case 2:
                    self.ver_historial(usuario)
                case 3:
                    self.transferir_a_terceros(usuario)
                case 0:
                    return



    # --------- MÉTODOS PARA LISTAR ---------

    def listar_clientes(self, clientes):
        print("\n=== LISTADO CLIENTES ===")
        print("\n" + "="*80)
        print(f"{'ID':<4} | {'RUT':<12} | {'NOMBRE COMPLETO':<25} | {'CORREO'}")
        print("-" * 80)
        for c in clientes:
            # Accedemos a los atributos del objeto que creó tu compañero
            nombre_full = f"{c.nombres} {c.apellidos}"
            print(f"{c._id:<4} | {c.rut:<12} | {nombre_full:<25} | {c.correo}")   
            print("="*80)    


    def listar_cuentas(self, cuentas):
        print("\n" + "="*60)
        print(f"{'ID':<5} | {'Tipo de Cuenta':<15} | {'N° Cuenta':<15} | {'Saldo':<10}")
        print("-" * 60)
        for c in cuentas:
            print(f"{c.id:<5} | {c.tipo_cuenta:<15} | {c.numero_cuenta:<15} | ${c.saldo:<10}")
            print("="*60)


    def listar_movimientos(self, movimientos):
        print("\n" + "=" * 110)
        print(f"{'Fecha':<20} | {'Tipo':<25} | {'Monto':<12} | {'Glosa'}")
        print("-" * 110)
        for m in movimientos:
            fecha = m[0]
            tipo = m[1]
            monto_clp = formato_clp(m[2])
            glosa = m[3] if m[3] else "---"
            print(f"{fecha:<20} | {tipo:<25} | {monto_clp:<12} | {glosa}")
        print("=" * 110)



    # <---------- FUNCIONES ------------->  
    def consultar_saldo(self, usuario):

        if usuario["rol"] == "empleado":
            clientes = Cliente.obtener_clientes()

            if not clientes:
                print("❌ No hay clientes")

            self.listar_clientes(clientes)

            cliente_id = validar_input_entero("Ingrese ID cliente: ")
        else:
            cliente_id = usuario["id"]

        cuentas = Cuenta.obtener_cuentas_cliente(cliente_id)

        if not cuentas:
                print("❌ No hay cuentas")
                return

        self.listar_cuentas(cuentas)

        cuenta = seleccionar_cuenta(cuentas, titulo="Seleccione una cuenta (o '0' para cancelar): ")
        if not cuenta:
            return

        print(f"\n✅ Detalle Cuenta N°: {cuenta.numero_cuenta}")
        print(f"   Tipo: {cuenta.tipo_cuenta}")
        print(f"   Estado: {cuenta.estado}")
        print(f"   Saldo Actual: {formato_clp(cuenta.saldo)}")

    

    def ver_historial(self, usuario):
        cuentas = Cuenta.obtener_cuentas_cliente(usuario["id"])

        if not cuentas:
            print("❌ No tienes cuentas asociadas para ver historial")
            return
                    
        self.listar_cuentas(cuentas)

        cuenta = seleccionar_cuenta(cuentas, titulo="Seleccione una cuenta (o '0' para cancelar): ")
        if not cuenta:
            return
                                        
        movimientos = Cuenta.obtener_historial_cliente(cuenta.id)
        if not movimientos:
            print("❌ No hay movimientos registrados en esta cuenta.")
            return
                    
        self.listar_movimientos(movimientos)



    def transferir_a_terceros(self, usuario):
        cuentas = Cuenta.obtener_cuentas_cliente(usuario["id"])
    
        if not cuentas:
            print("❌ No posees cuentas (Corriente o Vista) habilitadas para transferir.")
            return

        print("\n=== SELECCIONE CUENTA DE ORIGEN ===")
        self.listar_cuentas(cuentas)

        cuenta = seleccionar_cuenta(cuentas, titulo="Seleccione una cuenta (o '0' para cancelar): ")
        if not cuenta:
            return
        
        rut_destino = validar_rut("Ingrese el RUT del destinatario: ")
        cuenta_destino_info = Cuenta.buscar_cuenta(rut_destino)

        if not cuenta_destino_info:
            print("❌ El RUT ingresado no existe en el sistema.")
            return

        cliente_id_destino = cuenta_destino_info[0] 
        cuentas_destino = Cuenta.obtener_cuentas_cliente(cliente_id_destino)

        if not cuentas_destino:
            print("❌ El destinatario no tiene cuentas activas.")
            return

        nombre_destinatario = f"{cuenta_destino_info[1]} {cuenta_destino_info[2]}"

        print("\n--- DATOS DEL DESTINATARIO ---")
        print(f"Destinatario: {nombre_destinatario}")
        print("\n=== SELECCIONE CUENTA DE DESTINO ===")
        self.listar_cuentas(cuentas_destino)

        cuenta_destino = seleccionar_cuenta(cuentas_destino, titulo="Seleccione cuenta destino (o '0' para cancelar): ")
        if not cuenta_destino:
            return

        monto = validar_input_entero("Ingrese monto a transferir (CLP): $", minimo=1)

        if monto > cuenta.saldo:
            print(f"\n❌ Saldo insuficiente. Tu saldo es de {formato_clp(cuenta.saldo)}")
            return

        Cuenta.transferir_a_terceros(usuario["id"], cuenta.id, cuenta_destino.id, monto, cuenta.rut, nombre_destinatario)
        print(f"\n✅ Transferencia exitosa de {formato_clp(monto)} a {nombre_destinatario}.")



    def registrar_cliente(self):
        print("\n=== REGISTRAR CLIENTE ===")
        data = {
            "rut": validar_rut("Ingrese rut de cliente: "),
            "nombres": validar_input_texto("Nombres: "),
            "apellidos": validar_input_texto("Apellidos: "),
            "fecha_nacimiento": validar_input_fecha("Fecha nacimiento (YYYY-MM-DD): "),
            "direccion": validar_input_texto("Dirección: "),
            "telefono": validar_input_texto("Teléfono: "),
            "correo": validar_input_texto("Correo: "),
            "password": getpass.getpass("Ingrese su Contraseña: ")
        }

        cliente_id, error = Cliente.registrar_cliente(data)

        if error:
            print(error)

        if cliente_id:
            print("✅ Cliente registrado correctamente")
            print("\n=== APERTURA DE NUEVA CUENTA ===")
            print("Tipos de cuenta: 1. Corriente | 2. Ahorro | 3. Vista")
            id_tipo_cuenta = validar_input_entero("Seleccione tipo (1-3): ", minimo=1, maximo=3)
            monto_inicial  = validar_input_entero("Monto de apertura (CLP): $", minimo=0)

            cuenta = Cuenta.crear_cuenta(cliente_id, id_tipo_cuenta, monto_inicial)

            print(f"\n✅ Cuenta N° {cuenta["numero_cuenta"]} creada con éxito.")
            print(f"Saldo inicial: {formato_clp(monto_inicial)}")



    def crear_cuenta(self):
        clientes = Cliente.obtener_clientes()

        if not clientes:
            print("❌ No hay clientes registrados.")
            return
        
        self.listar_clientes(clientes)

        rut = validar_rut("Ingrese el RUT del cliente: ")
        cliente = Cliente.buscar_por_rut(rut)

        if not cliente:
            print("❌ Cliente no encontrado.")
            return

        print(f"\nCliente: {cliente.nombres} {cliente.apellidos}")
        print("\n=== APERTURA DE NUEVA CUENTA ===")
        print("Tipos de cuenta: 1. Corriente | 2. Ahorro | 3. Vista")
        
        id_tipo_cuenta = validar_input_entero("Seleccione tipo de cuenta: ", 1, 3)
        monto_inicial = validar_input_entero("Monto de apertura (CLP): $", 0)

        cuenta = Cuenta.crear_cuenta(cliente._id, id_tipo_cuenta, monto_inicial)

        if cuenta:
            print(f"\n✅ Cuenta N° {cuenta['numero_cuenta']} creada con éxito.")
            print(f"Saldo inicial: {formato_clp(monto_inicial)}")



    def info_cliente(self):
        rut = validar_rut()
        cliente = Cliente.buscar_por_rut(rut)

        if not cliente:
            print("❌ Cliente no encontrado")
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
                print(f"Cuenta ID: {c[0]} | Saldo: ${c[1]:,.0f} | N°: {c[3]} | Estado: {c[2]}".replace(",", "."))
        else:
            print("❌ No hay cuentas registradas.")