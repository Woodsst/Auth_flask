BAD_REQUEST = {"result": {"message": "bad request", "status": "fail"}}
ROLE_EXISTS = {"message": "role already exists", "status": "fail"}
ROLE_CREATE = {"message": "role created", "status": "succeeded"}
DEFAULT_ROLE_NOT_DELETE = {
    "result": {
        "message": "default roles cannot be deleted",
        "status": "fail",
    }
}
ROLE_DELETE = {"message": "role removed", "status": "succeeded"}
ROLE_NOT_EXIST = {
    "result": {"message": "the role does not exist", "status": "fail"}
}
ROLE_CHANGE = {"result": {"message": "role change", "status": "succeeded"}}
SHORT_PASSWORD = {"message": "password too short", "status": "fail"}
WRONG_EMAIL = {"message": "The email address is not valid", "status": "fail"}
WRONG_LOGIN = {"message": "login too short or not exist", "status": "fail"}
REGISTRATION_COMPLETE = {
    "result": {"message": "registration complete", "status": "succeeded"}
}
REGISTRATION_FAILED = {
    "result": {
        "message": "login or email already registered",
        "status": "fail",
    }
}
TOKEN_MISSING = {"message": "token is missing", "status": "fail"}
TOKEN_WRONG_FORMAT = {"message": "wrong token format", "status": "fail"}
LOGOUT = {"message": "logout", "status": "succeeded"}
USER_NOT_FOUND = {
    "status": "fail",
    "message": "The user with such login and password was not found",
}
PASSWORD_NOT_MATCH = {
    "status": "fail",
    "message": "the password does not match the user's password",
}
PASSWORD_CHANGE = {"message": "password changed", "status": "succeeded"}
PASSWORDS_EQUALS = {"message": "passwords equals", "status": "fail"}
TOKEN_CORRECT = {"message": "correct token", "status": "succeeded"}
TOKEN_OUTDATED = {"message": "token is outdated", "status": "fail"}
ACCESS_DENIED = {"result": {"message": "access denied", "status": "fail"}}
EMAIL_CHANGE = {"message": "email changed", "status": "succeeded"}
