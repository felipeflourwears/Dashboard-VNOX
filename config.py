class Config():
    SECRET_KEY = 'b97a6d5e52eb344c598e743'
    MYSQL_HOST = None
    MYSQL_USER = None
    MYSQL_PASSWORD = None
    MYSQL_DB = None

    def print_secret_key(self):
        print(f"SECRET_KEY: {self.SECRET_KEY}")

    def print_database_config(self):
        print(f"Database Config: {self.MYSQL_HOST}, {self.MYSQL_USER}, {self.MYSQL_PASSWORD}, {self.MYSQL_DB}")

class DevelopmentConfig(Config):
    DEBUG = True

    MYSQL_HOST = '82.180.172.63'
    MYSQL_USER = 'u958030263_popbeex24'
    MYSQL_PASSWORD = 'a&8[U2FF&8K'
    MYSQL_DB = 'u958030263_bd_vnoxx'

config = {
    'development': DevelopmentConfig
}
