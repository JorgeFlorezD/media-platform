from fastapi import status

class NotFoundException(Exception):
    def __init__(self, message: str, code: int = status.HTTP_404_NOT_FOUND):
        super().__init__(message)
        self.code = code
        self.message = message
        
class NotControlledException(Exception):
    def __init__(self, message: str, code: int = status.HTTP_500_INTERNAL_SERVER_ERROR):
        super().__init__(message)
        self.code = code
        self.message = message
        
class ExternalServiceException(Exception):
    def __init__(self, message: str, code = status.HTTP_424_FAILED_DEPENDENCY):
        super().__init__(message)
        self.code = code
        self.message = message