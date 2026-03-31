class RISError(Exception):
    pass


class RISApiError(RISError):

    def __init__(self, application: str, message: str) -> None:
        self.application = application
        self.api_message = message
        super().__init__(f"RIS API error [{application}]: {message}")


class RISRequestError(RISError):

    def __init__(self, message: str, status_code: int | None = None) -> None:
        self.status_code = status_code
        super().__init__(message)


class RISValidationError(RISError):
    pass
