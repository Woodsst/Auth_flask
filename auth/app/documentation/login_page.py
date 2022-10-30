login_dict = {
  "parameters": [
    {
      "name": "login",
      "in": "path",
      "type": "string",
      "required": "true",
    },
    {
      "name": "password",
      "in": "path",
      "type": "string",
      "required": "true",
    },
  ],
  "responses": {
    "200": {
      "description": "access-token: token, refresh-token: token",
    },
    "400": {
      "description": "message: login too short or not exist, status: fail",
    },
    "400": {
      "description": "message: password too short, status: fail",
    }
  }
}

logout_dict = {
  "parameters": [
    {
      "name": "Authorization",
      "in": "path",
      "type": "string",
      "required": "true",
    },
  ],
  "responses": {
    "200": {
      "description": "message: logout, status: succeeded",
    },
    "400": {
      "description": "message: token is missing, status: fail",
    },
  }
}

