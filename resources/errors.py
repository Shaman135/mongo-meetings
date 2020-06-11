class InternalServerError(Exception):
    pass


class SchemaValidationError(Exception):
    pass


class EventAlreadyExistsError(Exception):
    pass


class UpdatingEventError(Exception):
    pass


class DeletingEventError(Exception):
    pass


class EventNotExistsError(Exception):
    pass


class EmailAlreadyExistsError(Exception):
    pass


class UnauthorizedError(Exception):
    pass


errors = {
    "InternalServerError": {"message": "Something went wrong", "status": 500},
    "SchemaValidationError": {
        "message": "Request is missing required fields",
        "status": 400,
    },
    "EventAlreadyExistsError": {
        "message": "Event with given name already exists",
        "status": 400,
    },
    "UpdatingEventError": {
        "message": "Updating Event added by other is forbidden",
        "status": 403,
    },
    "DeletingEventError": {
        "message": "Deleting Event added by other is forbidden",
        "status": 403,
    },
    "EventNotExistsError": {
        "message": "Event with given id doesn't exists",
        "status": 400,
    },
    "EmailAlreadyExistsError": {
        "message": "User with given email address already exists",
        "status": 400,
    },
    "UnauthorizedError": {"message": "Invalid username or password", "status": 401},
}
