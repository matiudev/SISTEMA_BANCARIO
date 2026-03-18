from models.cliente import Cliente
from models.cuentas import Cuenta
from models.auth import Auth
import getpass


class Menu:


    def menu_principal(self):
        while True:
            print("\n==============================")
            print("      SISTEMA BANCARIO")
            print("==============================")

            print("\n--- AUTENTICACIÓN ---")

            rut = input("Introduzca su Rut: ")
            password = getpass.getpass("Ingrese su Contraseña: ")

            usuario = Auth.login(rut, password)

            if not usuario:
                print("❌ RUT o contraseña incorrectos")
                continue

            print("✅ Inicio de sesión Exitoso!")
            print(f"Bienvenido {usuario['nombre']}...")

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
            print("4. Depositar")
            print("5. Retirar")
            print("6. Transferencia")
            print("7. Listar Clientes")
            print("0. Cerrar Sesión")

            opcion = input("\nSeleccione una opción: ")

            match opcion:
                case "1":
                    clientes = Cliente.listar_clientes()
                    for c in clientes:
                        print(f"ID: {c.id} - Nombre: {c.nombres} {c.apellidos}")
                case "2":
                    Cuenta.crear_cuenta()
                case "3":
                    Cuenta.consultar_saldo()
                case "4" | "5":
                    print("Recuerda realizar los depósitos/retiros vía INSERT por ahora.")
                case "6":
                    print("Función delegada a módulos de cliente o manual.")
                case "7":
                    print("\n" + "="*80)
                    print(f"{'ID':<4} | {'RUT':<12} | {'NOMBRE COMPLETO':<25} | {'CORREO'}")
                    print("-" * 80)
                    
                    clientes = Cliente.listar_clientes()
                    
                    for c in clientes:
                        # Accedemos a los atributos del objeto que creó tu compañero
                        nombre_full = f"{c.nombres} {c.apellidos}"
                        print(f"{c.id:<4} | {c.rut:<12} | {nombre_full:<25} | {c.correo}")
                    
                    print("="*80)
                case "0":
                    return
                case _:
                    print("❌ Opcion Invalida")


    def menu_cliente(self, usuario):
        while True:
            print("\n--- MENU CLIENTE ---")
            print("1. Consultar Saldo")
            print("2. Ver Historial de movimientos")
            print("3. Transferir a otras cuentas")
            print("0. Cerrar Sesión")

            opcion = input("\nSeleccione una opción: ")

            match opcion:
                case "1":
                    Cuenta.consultar_saldo(usuario)
                case "2":
                    Cuenta.ver_historial_cliente(usuario["id"])
                case "3":
                    Cuenta.transferir_a_terceros(usuario["id"])
                case "0":
                    return
                case _:
                    print("❌ Opcion Invalida")

