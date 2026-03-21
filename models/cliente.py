from db.init_db import get_connection
import getpass
import bcrypt
from utils.utils import validar_rut


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
    


    # --------- MÉTODOS DE CLASE (cls) ---------
    @classmethod
    def obtener_clientes(cls):        
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
    def registrar_cliente(cls,data):

        cliente = cls.buscar_por_rut(data["rut"])
        
        if cliente:
            return None, "❌ El cliente ya existe"
        
        # 🔐 Encriptar contraseña
        password_hash = bcrypt.hashpw(data["password"].encode('utf-8'), bcrypt.gensalt())

        with get_connection() as connection:
            cursor = connection.cursor()
            
            # COMANDO SQL
            insert_query = """
                INSERT INTO usuario (rut, nombre, apellido, fecha_nacimiento, direccion, telefono, correo, password)
                VALUES (?,?,?,?,?,?,?,?);
            """

            usuario_data = (data["rut"], data["nombres"], data["apellidos"], data["fecha_nacimiento"], data["direccion"], data["telefono"], data["correo"], password_hash)
            cursor.execute(insert_query, usuario_data)

            usuario_id = cursor.lastrowid

            insert_query = """INSERT INTO cliente (usuario_id) VALUES (?);"""

            cursor.execute(insert_query, (usuario_id,))
            connection.commit()

            return cursor.lastrowid, None
        
    @classmethod
    def buscar_por_rut(cls, rut):
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