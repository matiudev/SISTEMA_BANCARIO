def create_table():
    from db.init_db import get_connection
    
    with get_connection() as connection:
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuario(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                rut TEXT UNIQUE NOT NULL,
                nombre TEXT NOT NULL,
                apellido TEXT NOT NULL,
                fecha_nacimiento DATE,
                direccion TEXT,
                telefono TEXT,
                correo TEXT,
                password TEXT NOT NULL
        )""")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cliente(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
    
            FOREIGN KEY(usuario_id) REFERENCES usuario(id)
        )""")

        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sucursal(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            direccion TEXT NOT NULL,
            telefono TEXT
        )""")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS empleado(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            id_sucursal INTEGER,

            FOREIGN KEY(usuario_id) REFERENCES usuario(id)
            FOREIGN KEY(id_sucursal) REFERENCES sucursal(id)
        )""")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tipo_cuenta(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo_cuenta TEXT NOT NULL
        )""")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cuentas(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_cliente INTEGER NOT NULL,
            id_tipo_cuenta INTEGER NOT NULL,
            numero_cuenta TEXT NOT NULL,
            saldo DECIMAL(10, 2) DEFAULT 0.0,
            estado TEXT DEFAULT 'Activa',                       
            FOREIGN KEY (id_cliente) REFERENCES cliente(id),
            FOREIGN KEY (id_tipo_cuenta) REFERENCES tipo_cuenta(id)
        )""")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tarjetas(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_cuenta INTEGER NOT NULL,
            numero_tarjeta TEXT NOT NULL,
            fecha_vencimiento TEXT,
            cvv INTEGER,
            estado TEXT DEFAULT 'ACTIVA',

            FOREIGN KEY (id_cuenta) REFERENCES cuentas(id)
        )""")
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS movimientos(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_cuenta_origen INTEGER NOT NULL,
            id_cuenta_destino INTEGER, -- Solo se usa en transferencias, puede ser NULL
            tipo_movimiento TEXT NOT NULL, -- 'DEPOSITO', 'RETIRO', 'TRANSFERENCIA'
            monto INTEGER NOT NULL, -- Valor en CLP
            fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
            glosa TEXT,
            FOREIGN KEY (id_cuenta_origen) REFERENCES cuentas(id),
            FOREIGN KEY (id_cuenta_destino) REFERENCES cuentas(id)
        )""")

        print("✅ Tablas Creadas correctamente")