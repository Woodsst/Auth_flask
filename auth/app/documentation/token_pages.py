update_token_dict = {
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
      "description": "access_token, refresh_token",
    },
    "400": {
      "description": "message: wrong token format, status: fail",
    },
  }
}

check_token_dict = {
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
      "description": "message: correct token, status: succeeded",
    },
    "400": {
      "description": "message: wrong token format, status: fail",
    },
  }
}