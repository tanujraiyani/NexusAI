class NexusAIException(Exception):
    def __init__(self, message: str):
        self.message = message


class AlreadyExistsException(NexusAIException):
    pass


class UnauthorizedException(NexusAIException):
    pass


class ForbiddenException(NexusAIException):
    pass


class NotFoundException(NexusAIException):
    pass