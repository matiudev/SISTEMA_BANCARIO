import bcrypt

def seed_data():
    from db.init_db import get_connection

    with get_connection() as connection:
        cursor = connection.cursor()

        # USUARIOS
        insert_query = """INSERT OR IGNORE INTO usuario (id, rut, nombre, apellido, fecha_nacimiento, direccion, telefono, correo, password) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        hashed = bcrypt.hashpw("inacap-2026".encode('utf-8'), bcrypt.gensalt())

        datos = [(
            1,
            "22215023-K",
            "Matias Alberto",
            "Garcia Pomatanta",
            "2006-09-22",
            "San Emilio 2020",
            "56922222222",
            "correo@correo.com",
            hashed
        ),(
            2,
            "21061232-7",
            "Emilio Jose",
            "Asencio Soto",
            "2001-01-01",
            "San Emilio 2021",
            "56911111111",
            "correo@correo.com",
            hashed
        ),(
            3,
            "19876543-2",
            "Valentina Paz",
            "Rojas Castillo",
            "1999-05-14",
            "Los Pinos 456",
            "56933333333",
            "valentina@email.com",
            hashed
        ),]

        cursor.executemany(insert_query, datos)


        # SUCURSALES
        cursor.execute("INSERT OR IGNORE INTO sucursal (id, nombre, direccion, telefono) VALUES (?, ?, ?, ?)", 
                    (1, "Sucursal Sector Sur", "Francisco Bilbao 3051", "91837465"))
        cursor.execute("INSERT OR IGNORE INTO sucursal (id, nombre, direccion, telefono) VALUES (?, ?, ?, ?)", 
                    (2, "Sucursal Sector Norte", "Emilio Bilbao 3051", "59614873"))


        # ROL DE LOS USUARIOS
        cursor.execute("INSERT OR IGNORE INTO cliente (id, usuario_id) VALUES (?, ?)", (1, 2))
        cursor.execute("INSERT OR IGNORE INTO cliente (id, usuario_id) VALUES (?, ?)", (2, 3))
        cursor.execute("INSERT OR IGNORE INTO empleado (id, usuario_id, id_sucursal) VALUES (?, ?, ?)", (1, 1, 1))


        # TIPOS DE CUENTA
        tipos_a_insertar = [
            (1, 'Corriente'),
            (2, 'Ahorro'),
            (3, 'Vista')
        ]

        cursor.executemany("""INSERT OR IGNORE INTO tipo_cuenta (id, tipo_cuenta) VALUES (?, ?)""", tipos_a_insertar)


        # CUENTAS
        cursor.execute("""
            INSERT OR IGNORE INTO cuentas (id, id_cliente, id_tipo_cuenta, numero_cuenta, saldo, estado) VALUES (?, ?, ?, ?, ?, ?)
        """,(1, 1, 3, "AHO-87780486", 20000, 'Activa'))

        cursor.execute("""
            INSERT OR IGNORE INTO cuentas (id, id_cliente, id_tipo_cuenta, numero_cuenta, saldo, estado) VALUES (?, ?, ?, ?, ?, ?)
        """,(2, 2, 1, "CTE-17260308", 12000, 'Activa'))
        
        print("🌱 Datos iniciales insertados")