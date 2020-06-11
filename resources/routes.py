from .events import EventApi, EventListApi
from .auth import RegisterApi, LoginApi


def initialize_routes(api):
    api.add_resource(EventListApi, '/api/events')
    api.add_resource(EventApi, '/api/events/<id>')
    api.add_resource(RegisterApi, '/api/auth/register')
    api.add_resource(LoginApi, '/api/auth/login')