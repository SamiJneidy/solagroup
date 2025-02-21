from fastapi.exceptions import HTTPException
from fastapi import status

class InvalidToken(HTTPException):
    def __init__(self, status_code=status.HTTP_401_UNAUTHORIZED, detail = "Invalid Token"):
        super().__init__(status_code=status_code, detail=detail)

class InvalidCredentials(HTTPException):
    def __init__(self, status_code=status.HTTP_404_NOT_FOUND, detail = "Invalid credentials"):
        super().__init__(status_code=status_code, detail=detail)
        
class ResourceNotFound(HTTPException):
    def __init__(self, resource = "Resource", status_code=status.HTTP_404_NOT_FOUND):
        super().__init__(status_code=status_code, detail=f"{resource} not found")

class ResourceAlreadyInUse(HTTPException):
    def __init__(self, resource = "Resource", status_code=status.HTTP_409_CONFLICT):
        super().__init__(status_code=status_code, detail=f"{resource} already in use")