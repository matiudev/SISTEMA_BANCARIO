from db.db import get_connection

#djawfhjawfajwfjaw
#erawjfdajwfjawfa
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
        nombres = input("Nombres: ")
        apellidos = input("Apellidos: ")
        fecha_nacimiento = input("Fecha nacimiento (YYYY-MM-DD): ")
        direccion = input("Dirección: ")
        telefono = input("Teléfono: ")
        correo = input("Correo: ")

        with get_connection() as connection:
            cursor = connection.cursor()
            
            # COMANDO SQL
            insert_query = """
                INSERT INTO clientes (rut, nombres, apellidos, fecha_nacimiento, direccion, telefono, correo)
                VALUES (?,?,?,?,?,?,?);
            """

            client_data = (rut, nombres, apellidos, fecha_nacimiento, direccion, telefono, correo)
            cursor.execute(insert_query, client_data)
            connection.commit()


    @classmethod
    def listar_clientes(cls):
        print("\n=== LISTADO CLIENTES ===")
        
        with get_connection() as connection:
            cursor = connection.cursor()

            # COMANDO SQL
            select_query = """
                SELECT * FROM clientes
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