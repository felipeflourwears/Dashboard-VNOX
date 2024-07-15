import requests
import random
import string

from .entities.User import User

class ModelUser():
    @classmethod
    def login(self, db, user):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT u.id, u.username, u.email, u.password, u.idRol, u.fullname, c.vnnox, c.zkong, c.hexnode, c.magicInfo, c.pisignage, c.kosStudio, c.idCustomer FROM user u JOIN customers c ON u.idCustomer = c.idCustomer WHERE email = '{}'""".format(user.email)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row is not None:
                user = User(row[0], row[1], row[2], User.check_password(row[3], user.password), row[4], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[5])
                return user
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def get_by_id(self, db, id):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT u.id, u.username, u.email, u.password, u.idRol, u.fullname, c.vnnox, c.zkong, c.hexnode, c.magicInfo, c.pisignage, c.kosStudio, c.idCustomer FROM user u JOIN customers c ON u.idCustomer = c.idCustomer WHERE id = '{}'".format(id)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row is not None:
                return User(row[0], row[1], row[2], None, row[3], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[5])
            return None
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod  
    def code_verification(cls, email):
        # Generar un código de verificación aleatorio
        code = ''.join(random.choices(string.digits, k=6))  # Genera un código de 6 dígitos

        endpoint = 'https://retailmibeex.net/apiVnnox/authCode.php'
        headers = {
            'Content-Type': 'application/json',
        }
        body = {
            'correo': email,
            'token': code  # Envía el código de verificación en lugar de un token
        }

        try:
            # Realizar la petición POST
            response = requests.post(endpoint, headers=headers, json=body)

            # Verificar si la petición fue exitosa (código 200)
            if response.status_code == 200:
                print("Verification code sent successfully")
                return code  # Devuelve el código generado para su posterior validación
            else:
                # La petición no fue exitosa, mostrar un mensaje de error
                print(f"Error en la petición: {response.status_code}")
                return None

        except Exception as e:
            # Ocurrió un error durante la petición
            print(f"Error: {e}")
            return None
        
    @classmethod
    def email_exists(cls, db, email):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT COUNT(*) FROM user WHERE email = %s"
            cursor.execute(sql, (email,))
            count = cursor.fetchone()[0]
            #print("Email count for {}: {}".format(email, count))  # Agregar un mensaje de registro
            return count > 0
        except Exception as ex:
            print("Error checking email existence:", ex)  # Agregar un mensaje de registro para cualquier excepción
            raise Exception("Error checking email existence: {}".format(ex))
