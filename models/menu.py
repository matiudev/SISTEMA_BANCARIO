from models.cliente import Cliente
from models.cuentas import Cuenta
from models.auth import Auth
import getpass


class Menu:


    def menu_principal(self):
        while True:
            print("\n==============================")
            print("      SISTEMA BANCARIOoooo")
            print("==============================")

            print("\n--- AUTENTICACIÓN ---")

            rut = input("Introduzca su Rut: ")
            password = getpass.getpass("Ingrese su Contraseña: ")

            usuario = Auth.login(rut, password)

            if not usuario:
                print("❌ RUT o contraseña incorrectos")
                continue

            print("✅ Inicio de sesión Exitoso!")
            print("Bienvenido...")

            rol = usuario["rol"]

            if rol == "cliente":
                self.menu_cliente()
            elif rol == "empleado":
                self.menu_empleado()
            
            # elif rol == "gerente":
            #     Menu.menu_gerente()


    def menu_empleado(self):
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
                    Cliente.registrar_cliente()
                case "2":
                    Cuenta.crear_cuenta()
                case "3":
                    Cuenta.consultar_saldo()
                case "4":
                    print("Función en desarrollo...")
                case "5":
                    print("Función en desarrollo...")
                case "6":
                    print("Función en desarrollo...")
                case "7":
                    clientes = Cliente.listar_clientes()
                    for cliente in clientes:
                        print(cliente)
                case "0":
                    return
                case _:
                    print("❌ Opcion Invalida")


    def menu_cliente(self):
        while True:
            print("\n--- MENU CLIENTE ---")
            print("1. Consultar Saldo")
            print("2. Ver Historial de movimientos")
            print("3. Transferir a otras cuentas")
            print("0. Cerrar Sesión")

            opcion = input("\nSeleccione una opción: ")

            match opcion:
                case "1":
                    print("Función en desarrollo...")
                case "2":
                    print("Función en desarrollo...")
                case "3":
                    print("Función en desarrollo...")
                case "0":
                    return
                case _:
                    print("❌ Opcion Invalida")

