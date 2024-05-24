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
    def __init__(self,key=None):
        if key is not None:
            detail = f"Object {key} with such ID not found"
        else:
            detail = "Object with such ID not found"
        super().__init__(status_code=400, detail=detail)


class UpdateException(HTTPException):
    def __init__(self,key):
        super().__init__(status_code=400,detail=f"Update {key} is not allowed!")



class CompanyAlreadyExistsException(HTTPException):
    def __init__(self, company_name: str):
        super().__init__(status_code=400, detail=f"Company with the name '{company_name}' already exists")


class NoSuchMemberException(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="No such member in the company")


class AlreadyAdminException(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="Member is already admin")


class MemberNotAdminException(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="Member is not admin")