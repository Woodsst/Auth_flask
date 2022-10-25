class PasswordException(Exception):
    """Исключение получаемое при некорректном пароле"""

    def __init__(self, text: str):
        self.text = text


class LoginException(Exception):
    pass
