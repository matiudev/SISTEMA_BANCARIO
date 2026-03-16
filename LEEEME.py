from db.db import get_connection
# IMPORTANTE QUE AL EJECUTAR CODIGO SQL EMPEZEMOS ASI:

with get_connection as connection:
    cursor = connection.cursor()

    # Comando SQL (select_query/insert_query/update_query)

    insert_query = """COMANDO SQL SEGUN LO QUE SE NECESITE"""
    cursor.execute(insert_query) # O EL NOMBRE DE LA VARIABLE QUE LE DIERON

    # SI ES UN UPDATE/DELETE/INSERT SE ESCRIBE LO SIGUIENTE
    connection.commit()


# AQUI UNOS EJEMPLOS:

with get_connection() as connection:
    cursor = connection.cursor()

    insert_query = """
    INSERT INTO clientes (rut, nombres, apellidos)
    VALUES (?, ?, ?)
    """

    datos = ("12345678-9", "Juan", "Perez") # SIEMPRE EN (), OSEA UNA TUPLA

    cursor.execute(insert_query, datos)

    connection.commit() # ES COMMIT PORQUE INSERTAMOS DATOS


# CONSULTA DE DATOS
with get_connection() as connection:
    cursor = connection.cursor()

    select_query = "SELECT * FROM clientes"

    cursor.execute(select_query)

    rows = cursor.fetchall()

    for row in rows:
        print(row)


#UPDATE DE DATOS
with get_connection() as connection:
    cursor = connection.cursor()

    update_query = """
    UPDATE clientes
    SET telefono = ?
    WHERE rut = ?
    """

    cursor.execute(update_query, ("999999999", "12345678-9")) # EL RUT Y EL TELEFONO ESTAN EN PARENTESIS COMO SEGUNDO ARGUMENTO PORQUE RECUERDEN QUE SIEMPRE ES UNA TUPLA LA QUE SE LE TIENE QUE PASAR, tmb podria haber sido una variable y quedaria asi:

    # update_data = ("999999999", "12345678-9")
    # cursor.execute(update_query, update_query)

    connection.commit()


# ELIMINAR DATOS
with get_connection() as connection:
    cursor = connection.cursor()

    delete_query = """
    DELETE FROM clientes
    WHERE rut = ?
    """

    cursor.execute(delete_query, ("12345678-9",))

    connection.commit()



# PARA CREAR TABLAS EN ESTE CASO SERIA EN EL ARCHIVO DB DE LA CARPETA DB. DENTRO DE LA FUNCION init_db QYUE CREA LAS TABLAS

# SIEMPRE EMPEZAR CON EL with get_connection() as connection, cursor y commit en caso que sea necesario
