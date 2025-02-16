from fastapi.exceptions import HTTPException
from fastapi import status

class InvalidToken(HTTPException):
    def __init__(self, detail = "Invalid Token"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)

class InvalidCredentials(HTTPException):
    def __init__(self, detail = "Invalid credentials"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
        
class ResourceNotFound(HTTPException):
    def __init__(self, resource = "Resource"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=f"{resource} not found")

class ResourceAlreadyInUse(HTTPException):
    def __init__(self, resource = "Resource"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=f"{resource} already in use")



class UserNotFound(HTTPException):
    def __init__(self, detail = "User not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class SourceNotFound(HTTPException):
    def __init__(self, detail = "Source not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class DestinationNotFound(HTTPException):
    def __init__(self, detail = "Destination not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class UsernameAlreadyInUse(HTTPException):
    def __init__(self, detail = "The username is already in use"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)

class ZipCodeAlreadyInUse(HTTPException):
    def __init__(self, detail = "The zip code is already in use"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)

class InlandTransportNotFound(HTTPException):
    def __init__(self, detail = "The zip code is already in use"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)