from datetime import datetime
from pydantic import BaseModel, Field
from fastapi import UploadFile, File, Form
from typing import Optional, List
from .common import CommonQueryParams

class UserQueryParams(CommonQueryParams):
    filter: Optional[str] = Field(None, description="Filter to apply to the user data (optional)")

class UserDocumentUploadForm(BaseModel):
    document_type: str
    user: str

    @classmethod
    def as_form(
        cls,
        document_type: str = Form(...),
        user: str = Form(...),
        document: UploadFile = File(...)
    ):
        return {"user": user, "document_type": document_type, "document": document}  # Return dictionary
