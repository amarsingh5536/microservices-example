from pydantic import BaseModel, Field
from typing import Optional, List

class CommonQueryParams(BaseModel):
    page: Optional[int] = Field(1, ge=1, description="Page number for pagination, starting from 1")
    page_limit: Optional[int] = Field(10, le=100, description="Maximum number of results per page (up to 100)")
