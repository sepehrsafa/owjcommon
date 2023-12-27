from .exception_codes import exception_codes


class OWJException(Exception):
    def __init__(self, code: str, http_status_code: int = 400):
        self.code = code
        self.message = exception_codes.get(code, "Unknown error")
        self.http_status_code = http_status_code

    def __str__(self):
        return f"OWJException: {self.code}"


class OWJPermissionException(OWJException):
    def __init__(self):
        super().__init__("E1022", 403)
