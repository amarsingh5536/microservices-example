from fastapi import APIRouter, Request, Response, Depends, status
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get('/v2/api/health/', status_code=status.HTTP_200_OK)
async def health_check():
    """
    Health check endpoint to ensure the service is running
    """
    return JSONResponse(
        content={"status": "healthy", "message": "Api Gateway Service is up and running."},
        status_code=status.HTTP_200_OK
    )