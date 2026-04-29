from flask import Flask
from database import db
from routes.task_routes import task_bp
from flask_jwt_extended import JWTManager
from routes.auth_routes import auth_bp
from flask_bcrypt import Bcrypt
from flasgger import Swagger

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Flask Task Manager API",
        "description": "API REST com autenticação JWT",
        "version": "1.0.0"
    }
}

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

Swagger(app, template=swagger_template, config=swagger_config)

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
    return "API de tarefas funcionando com Swagger!"


with app.app_context():
    db.create_all()

@app.route("/debug/routes")
def debug_routes():
    return {
        "routes": [str(rule) for rule in app.url_map.iter_rules()]
    }

if __name__ == "__main__":
    app.run(debug=True)