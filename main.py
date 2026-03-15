from db.db import init_db
from models.cliente import Cliente

#Hola
def menu():
    while True:
        print("\n=== SISTEMA BANCARIO ===")
        print("1 Registrar cliente")
        print("2 LISTAR CLIENTE")
        print("3 Consultar saldo")
        print("4 Depósito")
        print("5 Retiro")
        print("6 Transferencia")
        print("0 Salir")

        op = input("Seleccione: ")

        if op == "1":
            Cliente.registrar_cliente()
        elif op == "2":
            clientes = Cliente.listar_clientes()
            for c in clientes:
                print(c)
            # crear_cuenta()
            pass
        elif op == "3":
            # consultar_saldo()
            pass
        elif op == "4":
            # deposito()
            pass
        elif op == "5":
            # retiro()
            pass
        elif op == "6":
            # transferencia()
            pass
        elif op == "0":
            break
        else:
            print("Opción inválida")



init_db()
menu()

