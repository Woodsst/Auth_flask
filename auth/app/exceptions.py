class PasswordException(Exception):
    def __init__(self, text: str):
        self.text = text