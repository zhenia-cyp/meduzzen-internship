class CustomTokenExceptionBase(Exception):
    def init(self, detail: str):
        self.detail = detail

class CredentialsException(CustomTokenExceptionBase):
    def __init__(self, detail: str):
        self.detail = detail
        super().__init__(self.detail)


class TokenExpiredException(CustomTokenExceptionBase):
    def __init__(self, detail: str):
        self.detail = detail
        super().__init__(detail)

class TokenError(CustomTokenExceptionBase):
    def __init__(self, detail: str):
        self.detail = detail
        super().__init__(detail)


class NotFoundException(Exception):
    def __init__(self, key=None):
        if key is not None:
            self.message = f"Object {key} with such ID not found"
        else:
            self.message = "Object with such ID not found"
        super().__init__(self.message)


class UpdateException(Exception):
    def __init__(self, key):
        self.message = f"Update {key} is not allowed!"
        super().__init__(self.message)



class CompanyAlreadyExistsException(Exception):
    def __init__(self, company_name: str):
        self.message = f"Company with the name '{company_name}' already exists"
        super().__init__(self.message)


class NoSuchMemberException(Exception):
    def __init__(self, message="No such member in the company"):
        self.message = message
        super().__init__(self.message)

class AlreadyAdminException(Exception):
    def __init__(self, message="Member is already admin"):
        self.message = message
        super().__init__(self.message)


class MemberNotAdminException(Exception):
    def __init__(self, message="Member is not admin"):
        self.message = message
        super().__init__(self.message)


class PermissionDeniedException(Exception):
    def __init__(self, key=None):
        if key is not None:
            self.message = f"{key} is owner of a company"
        else:
            self.message = "Not enough permissions"
            super().__init__(self.message)


class RequestMemberInvitationException(Exception):
    def __init__(self, key):
        self.key = key
        if key == "request":
            self.message = "Request already sent"
        elif key == "member":
            self.message = "User is already a member"
        elif key == "invitation":
            self.message = "Invitation already sent"
        super().__init__(self.message)


