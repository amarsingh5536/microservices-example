import os
import aiohttp
from fastapi import APIRouter, Request, Response, status, HTTPException, status
from fastapi.responses import JSONResponse 
from gateway.network import make_request
from gateway.routes import ROUTES
router = APIRouter()


@router.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def gateway(path: str, request: Request):
    # Iterate through the routes to find a match
    service_url = None
    for route, target_url in ROUTES.items():
        if path == route:
            service_url = target_url

    if not service_url:
        raise HTTPException(status_code=404, detail="Route not found")

    # Prepare body and headers
    body = await request.json() if request.method in ["POST", "PUT", "PATCH"] else None
    headers = dict(request.headers)

    # Check if there is form data in the request
    form_data = None
    if "multipart/form-data" in headers.get("content-type", ""):
        form_data = await request.form()

    # Determine HTTP method as a string
    method = request.method.lower()

    try:

        # Make request to the selected microservice
        response_data, status_code = await make_request(service_url, method, form_data,  body, headers)
        # Return the response
        return JSONResponse(status_code=status_code, content=response_data)

    except aiohttp.client_exceptions.ClientConnectorError:
        # This error occurs when there is a network-related issue
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service is unavailable.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    except aiohttp.client_exceptions.ContentTypeError:
        # This error occurs when the service responds with an invalid content type
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Service error. Invalid content type received.",
            headers={"WWW-Authenticate": "Bearer"},
        )
