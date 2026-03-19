# SOLO DE PRUEBA NO EJECUTAR
# SOLO DE PRUEBA NO EJECUTAR

from db.db import get_connection
import bcrypt

with get_connection() as connection:
    cursor = connection.cursor()

    insert_query = """
    INSERT INTO usuario (
        rut, nombre, apellido, fecha_nacimiento, direccion, telefono, correo, password
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """

    hashed = bcrypt.hashpw("olasoymatias".encode('utf-8'), bcrypt.gensalt())
    hashed2 = bcrypt.hashpw("olasoyemilio".encode('utf-8'), bcrypt.gensalt())

    datos = [(
        "22215023-K",
        "Matias Alberto",
        "Garcia Pomatanta",
        "2006-09-22",  # formato ISO
        "San Emilio 2020",
        "56922222222",
        "correo@correo.com",
        hashed
    ),(
        "21061232-7",
        "Emilio Jose",
        "Asencio Soto",
        "2001-01-01",
        "San Emilio 2021",
        "56911111111",
        "correo@correo.com",
        hashed2
    )]

    cursor.executemany(insert_query, datos)

    cursor.execute("INSERT INTO sucursal (nombre, direccion, telefono) VALUES (?, ?, ?)", 
                ("Sucursal Sector Sur", "Francisco Bilbao 3051", "91837465"))
    cursor.execute("INSERT INTO sucursal (nombre, direccion, telefono) VALUES (?, ?, ?)", 
                ("Sucursal Sector Norte", "Emilio Bilbao 3051", "59614873"))

    # Suponiendo que los usuarios fueron insertados y tienen IDs 1 y 2
    cursor.execute("INSERT INTO cliente (usuario_id) VALUES (?)", (2,))
    cursor.execute("INSERT INTO empleado (usuario_id, id_sucursal) VALUES (?, ?)", (1, 1))

    print("Usuarios Insertados ✅")
    connection.commit()