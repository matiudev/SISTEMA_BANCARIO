from db.db import get_connection
import getpass
from utils.sanitizador import sanitizar_rut
import bcrypt


class Cliente:
    def __init__(self, rut, nombres, apellidos, fecha_nacimiento, direccion, telefono, correo, id = None):
        self._id = id

        self.rut = rut
        self.nombres = nombres
        self.apellidos = apellidos
        self.fecha_nacimiento = fecha_nacimiento
        self.direccion = direccion
        self.telefono = telefono
        self.correo = correo

        # --------- MÉTODOS DE INSTANCIA (self) ---------

    def __str__(self):
        return f"{self._id}. {self.rut} - {self.nombres} {self.apellidos} | Direccion: {self.direccion} | Correo: {self.correo} - {self.telefono} | Nacimiento: {self.fecha_nacimiento}"
    
    @staticmethod
    def registrar_cliente():
        print("\n=== REGISTRAR CLIENTE ===")
        rut = input("Ingrese su Rut: ")
        rut = sanitizar_rut(rut)
        nombres = input("Nombres: ")
        apellidos = input("Apellidos: ")
        fecha_nacimiento = input("Fecha nacimiento (YYYY-MM-DD): ")
        direccion = input("Dirección: ")
        telefono = input("Teléfono: ")
        correo = input("Correo: ")
        password = getpass.getpass("Ingrese su Contraseña: ")

        # 🔐 Encriptar contraseña
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password_bytes, salt)

        with get_connection() as connection:
            cursor = connection.cursor()
            
            # COMANDO SQL
            insert_query = """
                INSERT INTO usuario (rut, nombre, apellido, fecha_nacimiento, direccion, telefono, correo, password)
                VALUES (?,?,?,?,?,?,?,?);
            """

            usuario_data = (rut, nombres, apellidos, fecha_nacimiento, direccion, telefono, correo, password_hash)
            cursor.execute(insert_query, usuario_data)

            usuario_id = cursor.lastrowid

            insert_query = """INSERT INTO cliente (usuario_id) VALUES (?);"""

            cursor.execute(insert_query, (usuario_id,))
            connection.commit()
        


    @classmethod
    def listar_clientes(cls):
        print("\n=== LISTADO CLIENTES ===")
        
        with get_connection() as connection:
            cursor = connection.cursor()

            # COMANDO SQL
            select_query = """
            SELECT c.id, u.rut, u.nombre, u.apellido, u.fecha_nacimiento, u.direccion, u.telefono, u.correo
            FROM cliente c
            JOIN usuario u ON c.usuario_id = u.id
            """

            cursor.execute(select_query)
            rows = cursor.fetchall()
            clientes = []

            for row in rows:
                    cliente = cls(
                        row[1],      # rut
                        row[2],      # nombres
                        row[3],      # apellidos
                        row[4],      # fecha_nacimiento
                        row[5],      # direccion
                        row[6],      # telefono
                        row[7],      # correo
                        id=row[0]
                    )
                    clientes.append(cliente)

            return clientes
        
    @classmethod
    def buscar_por_rut(cls, rut):
    
        rut = sanitizar_rut(rut)

        with get_connection() as connection:
            cursor = connection.cursor()

            query = """
            SELECT c.id, u.rut, u.nombre, u.apellido, u.telefono, u.correo
            FROM cliente c
            JOIN usuario u ON c.usuario_id = u.id
            WHERE u.rut = ?
            """

            cursor.execute(query, (rut,))
            row = cursor.fetchone()

            if row:
                cliente = cls(
                    rut=row[1],
                    nombres=row[2],
                    apellidos=row[3],
                    fecha_nacimiento=None,
                    direccion=None, 
                    telefono=row[4],
                    correo=row[5]
                )
                cliente._id = row[0]
                return cliente
            else:
                return None