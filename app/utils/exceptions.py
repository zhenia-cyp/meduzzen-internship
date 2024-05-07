from fastapi import HTTPException

class CredentialsException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )

class TokenExpiredException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=401,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"}
        )

class TokenDecodingError(HTTPException):
    def __init__(self ):
        super().__init__(
            status_code=401,
            detail="Failed to decode the token",
            headers={"WWW-Authenticate": "Bearer"}
        )


class EmailUpdateNotAllowed(HTTPException):
    def __init__(self):
        super().__init__(status_code=400,
                         detail="Updating email is not allowed"
                         )

class NotFoundException(HTTPException):
    def __init__(self):
        super().__init__(status_code=400,detail=f"Object with such ID not found")



class UpdateException(HTTPException):
    def __init__(self,key):
        super().__init__(status_code=400,detail=f"Update {key} is not allowed!")



class CompanyAlreadyExistsException(HTTPException):
    def __init__(self, company_name: str):
        super().__init__(status_code=400, detail=f"Company with the name '{company_name}' already exists")