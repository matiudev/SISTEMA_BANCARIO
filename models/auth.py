from db.db import get_connection
import bcrypt

class Auth:
    
    @staticmethod
    def login(rut, password):
        with get_connection() as connection:
            cursor = connection.cursor()
            select_query = "SELECT id, password FROM usuario WHERE rut = ?"

            cursor.execute(select_query, (rut,))
            usuario = cursor.fetchone()

            if not usuario:
                return None
            
            usuario_id, hashed_db = usuario

            if not hashed_db:
                print("❌ Usuario sin contraseña válida en BD.")
                return None

            # Asegurarnos de que sea bytes
            if isinstance(hashed_db, str):
                hashed_db = hashed_db.encode('utf-8')

            # Verificar contraseña
            try:
                if not bcrypt.checkpw(password.encode('utf-8'), hashed_db):
                    return None
            except ValueError:
                print("❌ Hash de contraseña inválido.")
                return None

            # verificar rol
            cursor.execute("SELECT id FROM cliente WHERE usuario_id = ?", (usuario_id,))
            if cursor.fetchone():
                return {"id": usuario_id, "rol": "cliente"}

            cursor.execute("SELECT id FROM empleado WHERE usuario_id = ?", (usuario_id,))
            if cursor.fetchone():
                return {"id": usuario_id, "rol": "empleado"}

            cursor.execute("SELECT id FROM gerente WHERE usuario_id = ?", (usuario_id,))
            if cursor.fetchone():
                return {"id": usuario_id, "rol": "gerente"}
            
            return none