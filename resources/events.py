from flask import Response, request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from database.models import Event, User
from mongoengine.errors import (
    FieldDoesNotExist,
    NotUniqueError,
    DoesNotExist,
    ValidationError,
    InvalidQueryError
)
from resources.errors import (
    SchemaValidationError,
    EventAlreadyExistsError,
    InternalServerError,
    UpdatingEventError,
    DeletingEventError,
    EventNotExistsError,
    UnauthorizedError
)
from datetime import datetime

class EventListApi(Resource):
    @jwt_required
    def get(self):
        try:
            user_id = get_jwt_identity()
            events = Event.objects(owner=user_id).to_json()
            return Response(events, mimetype="application/json", status=200)
        except Exception:
            raise InternalServerError

    @jwt_required
    def post(self):
        try:
            user_id = get_jwt_identity()
            body = request.get_json()
            user = User.objects.get(id=user_id)
            event = Event()
            event.title = body.get("title")
            event.description = body.get("description", "")
            event.start = datetime.strptime(body.get("start"), '%Y-%m-%dT%H:%M:%S.%fZ')
            event.end = datetime.strptime(body.get("end"), '%Y-%m-%dT%H:%M:%S.%fZ')
            event.owner = user
            event.save()
            user.update(push__events=event)
            user.save()
            return Response(event.to_json(), mimetype="application/json", status=200)
        except (FieldDoesNotExist, ValidationError):
            raise SchemaValidationError
        except NotUniqueError:
            raise EventAlreadyExistsError
        except Exception:
            raise InternalServerError


class EventApi(Resource):
    @jwt_required
    def get(self, id):
        try:
            user_id = get_jwt_identity()
            event = Event.objects.get(id=id, owner=user_id)
            return Response(event.to_json(), mimetype="application/json", status=200)
        except DoesNotExist:
            raise EventNotExistsError
        except Exception:
            raise InternalServerError

    @jwt_required
    def put(self, id):
        try:
            user_id = get_jwt_identity()
            event = Event.objects.get(id=id, owner=user_id)
            body = request.get_json()
            event.title = body.get("title")
            event.description = body.get("description", "")
            event.start = datetime.strptime(body.get("start"), '%Y-%m-%dT%H:%M:%S.%fZ')
            event.end = datetime.strptime(body.get("end"), '%Y-%m-%dT%H:%M:%S.%fZ')
            event.save()
            return Response(event.to_json(), mimetype="application/json", status=200)
        except InvalidQueryError:
            raise SchemaValidationError
        except DoesNotExist:
            raise UpdatingEventError
        except Exception:
            raise InternalServerError

    @jwt_required
    def delete(self, id):
        try:
            user_id = get_jwt_identity()
            event = Event.objects.get(id=id, owner=user_id)
            event.delete()
            return Response(status=200)
        except DoesNotExist:
            raise DeletingEventError
        except Exception:
            raise InternalServerError
