from fastapi import APIRouter, Request, Response, status
from fastapi.responses import JSONResponse
from gateway.controllers.schemas.authentication import LoginSerializer
from gateway.network import make_request
from gateway.auth import extract_authorization_headers
from conf import settings

router = APIRouter()
SERVICE_URL = settings.USERS_SERVICE_URL

# Define the login endpoint using FastAPI's built-in POST decorator
@router.post('/api/auth/token/', status_code=status.HTTP_201_CREATED)
async def login(data: LoginSerializer, request: Request, response: Response):
    """
    Endpoint to authenticate a user and obtain a token.
    """
    # Construct the service URL dynamically
    url = f"{SERVICE_URL}{request.url.path}"
    
    # Prepare the headers for the request
    headers = extract_authorization_headers(request.headers)
    
    # Make the request to the external authentication service
    response_data, response_status = await make_request(
        url=url,
        method='post',
        headers=headers,
        data=data.dict()  
    )
    
    # Return the response data from the external service
    return JSONResponse(status_code=response_status, content=response_data)
