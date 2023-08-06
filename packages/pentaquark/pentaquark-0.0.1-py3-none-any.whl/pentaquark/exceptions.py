"""Pentaquark exceptions
"""


class PentaQuarkWarning(Warning):
    pass


class PentaQuarkException(Exception):
    pass


class PentaQuarkValidationError(PentaQuarkException, ValueError):
    """Raised on value validation error"""
    pass


class PentaQuarkConfigurationError(PentaQuarkException):
    """Raised on wrong configuration (settings or models)"""
    pass


class PentaQuarkInvalidLabelError(PentaQuarkException):
    """Invalid label name"""
    pass


class PentaQuarkObjectDoesNotExistError(PentaQuarkException):
    pass


class PentaQuarkCardinalityError(PentaQuarkException):
    pass


class PentaquarkInvalidOperationError(PentaQuarkException):
    pass


class PentaQuarkInvalidMatchOperationException(PentaquarkInvalidOperationError):
    pass

# class AtomicUniquenessViolationError(AtomicError):
#     """Raise when uniqueness constraint is not met"""
#     pass
#
#
# class AtomicPermissionError(AtomicError):
#     """Raised when a user tries to perform an action he does not have permission for"""
#     pass
#
#
# class AtomicPropertyValidationError(AtomicError):
#     """Raised when a property does not have the expected type/format"""
#     pass
#
#
# class AtomicConfigurationError(AtomicError):
#     """Raised on wrong configuration"""
#     pass
#
#
# class AtomicObjectDoesNotExist(AtomicError):
#     """Raised when trying to get an object and filters do not return any object"""
#     pass
#
#
# class AtomicMultipleObjectsReturned(AtomicError):
#     """Raised when several objects are found when only one was expected"""
#     pass
#
#
# class AtomicCreationError(AtomicError):
#     """Raised when obj.create or obj.save fails"""
#     pass
#
#
# class AtomicInvalidAttributeError(AtomicCreationError):
#     """Raised when provided attributes do not match ontology requirements"""
#     pass
#
#
# class AtomicMissingAttributeError(AtomicError):
#     """Raised when one tries to create an instance without providing all required attributes"""
#     pass
#
#
# class AtomicInvalidLabelError(AtomicConfigurationError):
#     """Raised when node label doesn't match the expected one"""
#     pass
