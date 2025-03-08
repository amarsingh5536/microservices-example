import aiohttp
import async_timeout
from typing import Optional
from fastapi import UploadFile
from conf import settings
from fastapi import UploadFile as FastAPIUploadFile
from starlette.datastructures import UploadFile as StarletteUploadFile, FormData

async def make_request(
    url: str,
    method: str,
    form_data: Optional[aiohttp.FormData] = None, 
    data: dict = None,
    headers: dict = None,
):
    """
    Args:
        url: is the url for one of the in-network services
        method: is the lower version of one of the HTTP methods: GET, POST, PUT, DELETE
        data: is the payload (optional)
        headers: is the header to put additional headers into request
        file: is the file to upload (optional)

    Returns:
        service result coming / non-blocking http request (coroutine)
    """
    if not data:
        data = {}

    with async_timeout.timeout(settings.GATEWAY_TIMEOUT):
        async with aiohttp.ClientSession() as session:
            request = getattr(session, method)
            file_fields = {}

            # Ensure form_data is aiohttp.FormData if it is a dictionary
            if form_data:
                _form_data = aiohttp.FormData(quote_fields=False)  # Ensure correct format

                for key, value in form_data.items():  # Use multi_items() to extract files correctly
                    if isinstance(value, (StarletteUploadFile, FastAPIUploadFile)):
                        file_content = await value.read()  # Read file as bytes

                        _form_data.add_field(
                            name=key,
                            value=file_content,  # Send file as actual bytes
                            filename=value.filename,
                            content_type=value.content_type or "application/octet-stream"
                        )
                    else:
                        _form_data.add_field(name=key, value=str(value))  # Convert non-file values to strings
                async with request(url, data=_form_data, headers=headers) as response:
                    response_data = await response.json()
                    return response_data, response.status
            else:  # Default to JSON payload if no file
                async with request(url, json=data, headers=headers) as response:
                    response_data = await response.json()
                    return response_data, response.status
