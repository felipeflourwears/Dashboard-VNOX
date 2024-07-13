from werkzeug.security import check_password_hash
from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, id, username, email, password, idRol, vnnox, zkong, hexnode, magicInfo, pisignage, idCustomer, fullname=""):
        self.id = id
        self.username = username
        self.password = password
        self.idRol = idRol
        self.fullname = fullname
        self.email = email
        self.vnnox = vnnox
        self.zkong = zkong
        self.hexnode = hexnode
        self.magicInfo = magicInfo
        self.pisignage = pisignage
        self.idCustomer = idCustomer

    @classmethod
    def check_password(self, hashed_password, password):
        return check_password_hash(hashed_password, password)
