from db.db import init_db
from models.cliente import Cliente

def menu():

    while True:

        print("\n==============================")
        print("      SISTEMA BANCARIO")
        print("==============================")

        print("\n--- AUTENTICACIÓN ---")
        print("1. Iniciar sesión")
        print("2. Registrar usuario")

        print("\n--- CLIENTES (CRUD) ---")
        print("3. Registrar cliente")
        print("4. Listar clientes")
        print("5. Actualizar cliente")
        print("6. Eliminar cliente")

        print("\n--- CUENTAS ---")
        print("7. Crear cuenta")
        print("8. Consultar saldo")

        print("\n--- TRANSACCIONES ---")
        print("9. Depositar dinero")
        print("10. Retirar dinero")
        print("11. Transferencia entre cuentas")

        print("\n0. Salir")

        opcion = input("\nSeleccione una opción: ")
"""
        if opcion == "1":
            iniciar_sesion()
        pass
        elif opcion == "2":
            registrar_usuario()
    
        elif opcion == "3":
            registrar_cliente()

        elif opcion == "4":
            listar_clientes()

        elif opcion == "5":
            actualizar_cliente()

        elif opcion == "6":
            eliminar_cliente()

        elif opcion == "7":
            crear_cuenta()

        elif opcion == "8":
            consultar_saldo()

        elif opcion == "9":
            deposito()

        elif opcion == "10":
            retiro()

        elif opcion == "11":
            transferencia()

        elif opcion == "0":
            print("Saliendo del sistema...")
            break

        else:
            print("Opción inválida, intente nuevamente.")
"""
init_db()
menu()

#ola