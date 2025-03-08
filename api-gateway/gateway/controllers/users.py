from fastapi import APIRouter, Request, Response, Depends, status, File, UploadFile, Form
from fastapi.responses import JSONResponse
from gateway.controllers.schemas.users import UserDocumentUploadForm
from gateway.network import make_request
from gateway.auth import extract_authorization_headers
from conf import settings

router = APIRouter()
SERVICE_URL = settings.USERS_SERVICE_URL

# This function will handle fetching the user details based on ID
@router.get('/api/accounts/users/{id}/', status_code=status.HTTP_200_OK)
async def get_users(id: int, request: Request, response: Response):
    url = f"{SERVICE_URL}/api/accounts/users/{id}/"
    headers = extract_authorization_headers(request.headers)
    response_data, response_status = await make_request(
        url=url,
        method='get',
        headers=headers
    )
    return JSONResponse(status_code=response_status, content=response_data)

# This function handles the file upload
@router.post('/api/accounts/user-documents/', status_code=status.HTTP_201_CREATED)
async def upload_file(request: Request, form_data: UserDocumentUploadForm = Depends(UserDocumentUploadForm.as_form)):
    headers = extract_authorization_headers(request.headers)
    
    # Make a request to the external service for file upload
    response_data, response_status = await make_request(
        url=f"{SERVICE_URL}{request.url.path}",
        method='post',
        headers=headers,
        form_data=form_data
    )
    return response_data
