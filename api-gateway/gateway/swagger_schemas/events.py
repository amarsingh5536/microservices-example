GET_EVENT_SCHEMA = {
    "/api/events/": {
        "get": {
            "tags": ["Events"],
            "description": "Get events details",
            "parameters": [],
            "responses": {
                "200": {
                    "description": "Event details retrieved",
                    "content": {
                        "application/json": {
                            "schema": {}
                            
                        }
                    }
                }
            }
        }
    }
}

# Export the schemas
EVENT_SCHEMAS = {
    **GET_EVENT_SCHEMA,
}