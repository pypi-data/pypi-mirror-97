class NodeNotFoundException(Exception):
    def __init__(self, path):
        self.path = path


class AuthenticationException(Exception):
    pass


class FormatterException(Exception):
    pass


class InvalidQueryException(Exception):
    pass


class CircularInheritanceException(Exception):
    pass
