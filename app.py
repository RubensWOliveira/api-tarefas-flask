from flask import Flask
from database import db
from routes.task_routes import task_bp
from flask_jwt_extended import JWTManager
from routes.auth_routes import auth_bp
from flask_bcrypt import Bcrypt
from flasgger import Swagger



app = Flask(__name__)

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec",
            "route": "/apispec.json",
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "swagger_ui": True,
    "specs_route": "/apidocs/"
}

swagger = Swagger(app, config=swagger_config)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "segredo-super-forte"

db.init_app(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)

app.register_blueprint(task_bp)
app.register_blueprint(auth_bp)


@app.route("/")
def home():
    return "API de tarefas funcionando!"


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)