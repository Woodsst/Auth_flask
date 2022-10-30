registrtion_dict = {
  "parameters": [
    {
      "name": "Authorization",
      "in": "path",
      "type": "string",
      "required": "true",
    },
  ],
  "responses": {
    "201": {
      "description": "message: registration complete, status: succeeded",
    },
    "400": {
      "description": "message: wrong token format, status: fail",
    },
  }
}
