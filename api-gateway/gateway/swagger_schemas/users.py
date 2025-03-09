GET_USER_SCHEMA = {
    "/api/users/{user_id}/": {
        "get": {
            "tags": ["Users"],
            "description": "Get user details",
            "parameters": [
                {
                    "name": "user_id",
                    "in": "path",
                    "required": True,
                    "schema": {
                        "type": "string",
                        "example": "123"
                    }
                }
            ],
            "responses": {
                "200": {
                    "description": "User details retrieved",
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "user_id": {"type": "string"},
                                    "username": {"type": "string"},
                                    "email": {"type": "string"}
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}

CREATE_USER_SCHEMA = {
    "/api/users/": {
        "post": {
            "tags": ["Users"],
            "description": "Create a new user",
            "requestBody": {
                "description": "New user details",
                "required": True,
                "content": {
                    "application/json": {
                        "schema": {
                            "type": "object",
                            "properties": {
                                "username": {"type": "string", "example": "new_user"},
                                "email": {"type": "string", "example": "new_user@example.com"},
                                "password": {"type": "string", "example": "password123"}
                            },
                            "required": ["username", "email", "password"]
                        }
                    }
                }
            },
            "responses": {
                "201": {
                    "description": "User successfully created"
                }
            }
        }
    }
}

# Export the schemas
USER_SCHEMAS = {
    **GET_USER_SCHEMA,
    **CREATE_USER_SCHEMA
}
