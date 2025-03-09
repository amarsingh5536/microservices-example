from fastapi import FastAPI
from swagger import get_custom_openapi
from gateway.controllers import router as routers
from gateway.middleware.request_gateway import router as gateway_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()  # Initialize FastAPI application

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the routes from the routes module
app.include_router(routers)

# Request gateway for all microservices routes.
app.include_router(gateway_router)

# Set the custom OpenAPI schema directly
app.openapi = get_custom_openapi 

@app.get("/docs", include_in_schema=False)
async def custom_docs():
    """ Return custom Swagger UI at the default '/docs' endpoint """
    return JSONResponse({"swagger_url": "/docs"})
