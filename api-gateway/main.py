from fastapi import FastAPI
from gateway.routes import router as routers
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
