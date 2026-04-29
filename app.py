from flask import Flask
from database import db
from routes.task_routes import task_bp
from flask_jwt_extended import JWTManager
from routes.auth_routes import auth_bp
from flask_bcrypt import Bcrypt
from flasgger import Swagger


app = Flask(__name__)

swagger = Swagger(app)

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


@app.route("/docs-test")
def docs_test():
    """
    Test endpoint
    ---
    responses:
      200:
        description: Endpoint de teste Swagger
    """
    return "Swagger ativo"


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)