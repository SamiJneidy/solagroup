from fastapi.exceptions import HTTPException
from fastapi import status

class InvalidToken(HTTPException):
    def __init__(self, status_code=status.HTTP_401_UNAUTHORIZED, detail = "Invalid Token"):
        super().__init__(status_code=status_code, detail=detail)

class InvalidCredentials(HTTPException):
    def __init__(self, status_code=status.HTTP_404_NOT_FOUND, detail = "Invalid credentials"):
        super().__init__(status_code=status_code, detail=detail)
        
class ResourceNotFound(HTTPException):
    def __init__(self, status_code=status.HTTP_404_NOT_FOUND, resource = "Resource"):
        super().__init__(status_code=status_code, detail=f"{resource} not found")

class ResourceAlreadyInUse(HTTPException):
    def __init__(self, status_code=status.HTTP_409_CONFLICT, resource = "Resource"):
        super().__init__(status_code=status_code, detail=f"{resource} already in use")

class ForeignKeyConstraintViolation(HTTPException):
    def __init__(self, status_code=status.HTTP_409_CONFLICT, detail=f"Deletion failed, this record is referenced by another table and cannot be removed"):
        super().__init__(status_code=status_code, detail=detail)

def classify_foreign_key_violation(error_message: str, resource: str = "Resource") -> ForeignKeyConstraintViolation:
    if "unique constraint" in error_message.lower():
        return ForeignKeyConstraintViolation(status.HTTP_409_CONFLICT, f"{resource} already in use")
    elif "foreign key" in error_message.lower():
        return ForeignKeyConstraintViolation(status.HTTP_400_BAD_REQUEST, f"Foreign key constraint violation, the data sent does not exist in the related table")
    else:
        return ForeignKeyConstraintViolation(status.HTTP_400_BAD_REQUEST, f"Foreign key constraint violation")  