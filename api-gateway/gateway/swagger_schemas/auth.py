CREATE_TOKEN_SCHEMA = {
    "/api/auth/token/": {
        "post": {
            "tags": ["Auth"],
            "description": "API to 'LOGIN'",
            "requestBody": {
                "description": "User login credentials",
                "required": True,
                "content": {
                    "application/json": {
                        "schema": {
                            "type": "object",
                            "properties": {
                                "username": {"type": "string", "example": "user@example.com"},
                                "password": {"type": "string", "example": "password123"},
                            },
                            "required": ["username", "password"]
                        }
                    }
                }
            },
            "responses": {
                "200": {
                    "description": "Successful login",
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "access_token": {"type": "string"},
                                    "refresh_token": {"type": "string",}
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}

LOGOUT_SCHEMA = {
    "/api/auth/logout/": {
        "post": {
            "tags": ["Auth"],
            "description": "API to 'LOGOUT'",
            "requestBody": {
                "description": "Logout request",
                "required": True,
                "content": {
                    "application/json": {
                        "schema": {
                            "type": "object",
                            "properties": {
                                "refresh_token": {"type": "string", "example": "your_refresh_token"}
                            },
                            "required": ["refresh_token"]
                        }
                    }
                }
            },
            "responses": {
                "200": {
                    "description": "Successful logout"
                }
            }
        }
    }
}

# Export the schemas
AUTH_SCHEMAS = {
    **CREATE_TOKEN_SCHEMA,
    **LOGOUT_SCHEMA
}
