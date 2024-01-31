class Config():
    SECRET_KEY = 'b97a6d5e52eb344c598e743'
    def print_secret_key(self):
        print(f"SECRET_KEY: {self.SECRET_KEY}")

class DevelopmentConfig(Config):
    DEBUG = True

    MYSQL_HOST = '82.180.172.63'
    MYSQL_USER = 'u958030263_popbeex24'
    MYSQL_PASSWORD = 'a&8[U2FF&8K'
    MYSQL_DB = 'u958030263_bd_vnoxx'


    """ MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'root'
    MYSQL_DB = 'kiosk' """

config = {
    'development': DevelopmentConfig
}
