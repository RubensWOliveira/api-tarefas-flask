from flask import Flask
from database import db
from routes.task_routes import task_bp

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

app.register_blueprint(task_bp)


@app.route("/")
def home():
    return "API de tarefas funcionando!"


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)