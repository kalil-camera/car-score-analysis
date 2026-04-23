"""Domain and Application level exceptions"""


class ApplicationException(Exception):
    """Base exception para toda aplicação"""
    
    def __init__(self, message: str, code: str = None, details: dict = None):
        self.message = message
        self.code = code or self.__class__.__name__
        self.details = details or {}
        super().__init__(self.message)


# Domain Exceptions
class EntityNotFoundError(ApplicationException):
    """Entity não encontrada no domínio"""
    pass


class InvalidValueObjectError(ApplicationException):
    """Value object inválido"""
    pass


class BusinessRuleViolationError(ApplicationException):
    """Violação de regra de negócio"""
    pass


class DuplicateEntityError(ApplicationException):
    """Entity duplicada"""
    pass


# Application Exceptions
class UseCaseExecutionError(ApplicationException):
    """Erro durante execução de use case"""
    pass


class ValidationError(ApplicationException):
    """Erro de validação"""
    pass


class ResourceNotFoundError(ApplicationException):
    """Recurso não encontrado"""
    pass
