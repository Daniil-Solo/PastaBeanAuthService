class ServiceException(Exception):
    def __init__(self, message: str):
        self.message = message


class SuchUserExistsException(ServiceException):
    pass


class SuchUserDoesntExistException(ServiceException):
    pass


class PasswordIncorrectException(ServiceException):
    pass


class PasswordValidationException(ServiceException):
    pass


class NeedAuthException(ServiceException):
    pass
