# swagger.py
from fastapi.openapi.models import OpenAPI
from gateway.swagger_schemas import ALL_SCHEMAS  # Assuming your path schema is in this
from conf import settings

# Define the base OpenAPI schema
OPENAPI_SCHEMA = {
    "openapi": "3.0.3",
    "info": {
        "title": "Microservices-Example APIs",
        "version": "1.0.0",
        "description": "API documentation for Microservices-Example"
    },
    "servers": [{"url": f"http://{settings.HOST}:{settings.PORT}"}],
    "tags": [{
            "name": "Auth",
            "name": "Users",
            "name": "Events"
        }],
    "paths": ALL_SCHEMAS,  # Your paths should be set here dynamically or predefined
    "components": {
        "securitySchemes": {
            "jwt": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT"
            }
        }
    },
    "security": [{"jwt": []}]
}

SECURITY_SCHEMES = {
    "AuthHeader": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
        "description": "A custom header for additional information",
        "required": False  # Optional
    },
    "DeviceIDHeader": {
        "type": "apiKey",
        "in": "header",
        "name": "Device-ID",
        "description": "Device ID for identifying the device",
        "required": False  # Optional
    }
}

def get_custom_openapi() -> OpenAPI:
    """
    Returns the customized OpenAPI schema with added security schemes.
    """
    # Get the default original OpenAPI schema
    # openapi_schema = app.openapi()

    # Custom OpenAPI schema
    openapi_schema = OPENAPI_SCHEMA.copy()  # Avoid mutating the original schema
    
    # Ensure that 'components' exists in the schema
    openapi_schema.setdefault("components", {})
    
    # Add security schemes to the OpenAPI schema
    openapi_schema["components"]["securitySchemes"] = {
        **openapi_schema["components"].get("securitySchemes", {}),
        **SECURITY_SCHEMES
    }

    # Apply global security settings
    openapi_schema["security"] = [
        {"APIKeyHeader": []},
        {"AuthHeader": []},
        {"DeviceIDHeader": []}
    ]
    
    return openapi_schema
