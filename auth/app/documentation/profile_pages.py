user_dict = {
  "parameters": [
    {
      "name": "Authorization",
      "in": "path",
      "type": "string",
      "required": "true",
    },
  ],
  "definitions": {
    "User": {
      "type": "object",
      "properties": {
        "login": {
          "type": "string",
        },
        "email": {
          "type": "string",
        },
        "role": {
          "type": "string",
        },
      }
    }
  },
  "responses": {
    "200": {
      "description": "message: logout, status: succeeded",
      "schema": {
        "$ref": "#/definitions/User"
      },
},
    "400": {
      "description": "message: token is missing, status: fail",
    },
  }
}

device_dict = {
  "parameters": [
    {
      "name": "Authorization",
      "in": "path",
      "type": "string",
      "required": "true",
    },
  ],
  "definitions": {
    "UserDevice": {
      "type": "object",
      "properties": {
        "history": {
          "type": "array",
          "items": {
            "$ref": "#/definitions/Device"
          }
        },
      }
    },
    "Device": {
      "type": "object",
      "properties": {
        "device": {
          "type": "string",
        },
      }
    }
  },
  "responses": {
    "200": {
      "description": "message: logout, status: succeeded",
      "schema": {
        "$ref": "#/definitions/UserDevice"
      },
},
    "400": {
      "description": "message: token is missing, status: fail",
    },
  }
}

email_dict = {
  "parameters": [
    {
      "name": "Authorization",
      "in": "path",
      "type": "string",
      "required": "true",
    },
    {
      "name": "new_email",
      "in": "path",
      "type": "string",
      "required": "true",
    },
  ],
  "responses": {
    "200": {
      "description": "message: email changed, status: succeeded",
    },
    "400": {
      "description": "message: The email address is not valid, status: fail",
    },
  }
}

password_dict = {
  "parameters": [
    {
      "name": "Authorization",
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
    {
      "name": "new_password",
      "in": "path",
      "type": "string",
      "required": "true",
    },
  ],
  "responses": {
    "200": {
      "description": "message: password changed, status: succeeded",
    },
    "400": {
      "description": "message: password too short, status: fail",
    },
  }
}
