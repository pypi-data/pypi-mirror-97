import mimetypes
from urllib.parse import quote

from django.http import HttpResponse


def create_attachment_response(filename, content: bytes):
    """
        Creates response to download file with correct headers
         for given content and filename
    """
    response = HttpResponse(content=content)
    safe_filename = quote(filename)
    response['Content-Disposition'] = f'inline; filename="{safe_filename}"'

    mime_type, encoding = mimetypes.guess_type(filename)
    if mime_type is None:
        mime_type = 'application/octet-stream'
    response['Content-Type'] = mime_type

    response['Access-Control-Expose-Headers'] = 'Content-Disposition'

    if encoding is not None:
        response['Content-Encoding'] = encoding

    return response
