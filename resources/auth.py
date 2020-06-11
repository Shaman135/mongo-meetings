from flask import request, Response
from flask_restful import Resource
from flask_jwt_extended import create_access_token
from database.models import User
from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist
from resources.errors import (
    SchemaValidationError,
    EmailAlreadyExistsError,
    UnauthorizedError,
    InternalServerError,
)
import datetime, json


class RegisterApi(Resource):
    def post(self):
        try:
            body = request.get_json()
            user = User(**body)
            user.hash_password()
            user.save()
            return Response(
                json.dumps({id: str(user.id)}), mimetype="application/json", status=200
            )
        except FieldDoesNotExist:
            raise SchemaValidationError
        except NotUniqueError:
            raise EmailAlreadyExistsError
        except Exception:
            raise InternalServerError


class LoginApi(Resource):
    def post(self):
        try:
            body = request.get_json()
            user = User.objects.get(email=body.get("email"))
            authorized = user.check_password(body.get("password"))
            if not authorized:
                return Response(
                    json.dumps({"error": "Invalid login data"}),
                    mimetype="application/json",
                    status=401,
                )

            expires = datetime.timedelta(days=7)
            access_token = create_access_token(
                identity=str(user.id), expires_delta=expires
            )
            return Response(
                json.dumps({"token": str(access_token)}),
                mimetype="application/json",
                status=200,
            )
        except (UnauthorizedError, DoesNotExist):
            raise UnauthorizedError
        except Exception:
            raise InternalServerError
