add_role_dict = {
  "parameters": [
    {
      "name": "Authorization",
      "in": "path",
      "type": "string",
      "required": "true",
    },
    {
      "name": "role",
      "in": "path",
      "type": "string",
      "required": "true",
    },
    {
      "name": "description",
      "in": "path",
      "type": "string",
      "required": "true",
    }
  ],
  "responses": {
    "200": {
      "description": "message: role created, status: succeeded",
    },
    "400": {
      "description": "message: bad request, status: fail",
    },
  }
}

delete_role_dict = {
  "parameters": [
    {
      "name": "Authorization",
      "in": "path",
      "type": "string",
      "required": "true",
    },
    {
      "name": "role",
      "in": "path",
      "type": "string",
      "required": "true",
    },
  ],
  "responses": {
    "200": {
      "description": "message: role removed, status: succeeded",
    },
    "400": {
      "description": "message: bad request, status: fail",
    },
  }
}

change_role_dict = {
  "parameters": [
    {
      "name": "Authorization",
      "in": "path",
      "type": "string",
      "required": "true",
    },
    {
      "name": "role",
      "in": "path",
      "type": "string",
      "required": "true",
    },
    {
      "name": "change_description",
      "in": "path",
      "type": "string",
      "required": "true",
    },
    {
      "name": "change_role",
      "in": "path",
      "type": "string",
      "required": "true",
    },
  ],
  "responses": {
    "200": {
      "description": "message: role change, status: succeeded",
    },
    "400": {
      "description": "message: bad request, status: fail",
    },
  }
}

roles_dict = {
  "definitions": {
    "RoleObject": {
      "type": "object",
      "properties": {
        "result": {
          "type": "array",
          "items": {
            "$ref": "#/definitions/Role",
          }
        }
      }
    },
    "Role": {
      "type": "object",
      "properties": {
        "role": {
          "type": "string",
        },
        "description": {
          "type": "string",
        },
      }
    }
  },
  "responses": {
    "200": {
      "description": "Список ролей",
      "schema": {
        "$ref": "#/definitions/RoleObject"
      },
    }
  }
}

set_role_dict = {
  "parameters": [
    {
      "name": "Authorization",
      "in": "path",
      "type": "string",
      "required": "true",
    },
    {
      "name": "user_id",
      "in": "path",
      "type": "uuid",
      "required": "true",
    },
    {
      "name": "role",
      "in": "path",
      "type": "string",
      "required": "true",
    },
  ],
  "responses": {
    "200": {
      "description": "message: role change, status: succeeded",
    },
    "400": {
      "description": "message: bad request, status: fail",
    }
  }
}
