import bcrypt

class SecurityController:
    def cifrar_contrasenia(password_str)->str:
        pwd_byter=password_str.encode('utf-8')
        salt=bcrypt.gensalt()

        return bcrypt.hashpw(pwd_byter,salt).decode('utf-8')