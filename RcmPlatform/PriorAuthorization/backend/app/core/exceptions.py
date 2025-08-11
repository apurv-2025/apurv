# Custom exceptions for Prior Authorization System

class PriorAuthorizationException(Exception):
    """Base exception for Prior Authorization system"""
    pass


class EDIException(PriorAuthorizationException):
    """Exception for EDI processing errors"""
    pass


class DatabaseException(PriorAuthorizationException):
    """Exception for database errors"""
    pass


class ValidationException(PriorAuthorizationException):
    """Exception for validation errors"""
    pass


class AuthorizationException(PriorAuthorizationException):
    """Exception for authorization errors"""
    pass


class PatientNotFoundException(PriorAuthorizationException):
    """Exception when patient is not found"""
    pass


class RequestNotFoundException(PriorAuthorizationException):
    """Exception when authorization request is not found"""
    pass


class CodeNotFoundException(PriorAuthorizationException):
    """Exception when healthcare code is not found"""
    pass 