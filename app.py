from flask import Flask
from flask_restful import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from database.db import initialize_db
from resources.routes import initialize_routes
from resources.errors import errors

app = Flask(__name__)

app.config["MONGODB_SETTINGS"] = {
    "host": "mongodb://localhost/meetings"
}
app.config["JWT_SECRET_KEY"] = "ultrahiperjwtsecretkeyformongodbproject2137xD"

api = Api(app, errors=errors)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

initialize_db(app)
initialize_routes(api)

if __name__ == "__main__":
    app.run(debug=True)
