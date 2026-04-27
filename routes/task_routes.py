from flask import Blueprint, request, jsonify
from database import db
from models.task import Task

task_bp = Blueprint("task_bp", __name__)


@task_bp.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json()

    new_task = Task(
        title=data["title"],
        description=data.get("description", "")
    )

    db.session.add(new_task)
    db.session.commit()

    return jsonify({
        "message": "Tarefa criada com sucesso",
        "id": new_task.id
    }), 201


@task_bp.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = Task.query.all()

    task_list = []

    for task in tasks:
        task_list.append({
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "completed": task.completed
        })

    return jsonify(task_list)


@task_bp.route("/tasks/<int:id>", methods=["GET"])
def get_task(id):
    task = Task.query.get(id)

    if not task:
        return jsonify({"message": "Tarefa não encontrada"}), 404

    return jsonify({
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "completed": task.completed
    })


@task_bp.route("/tasks/<int:id>", methods=["PUT"])
def update_task(id):
    task = Task.query.get(id)

    if not task:
        return jsonify({"message": "Tarefa não encontrada"}), 404

    data = request.get_json()

    task.title = data.get("title", task.title)
    task.description = data.get("description", task.description)
    task.completed = data.get("completed", task.completed)

    db.session.commit()

    return jsonify({"message": "Tarefa atualizada com sucesso"})


@task_bp.route("/tasks/<int:id>", methods=["DELETE"])
def delete_task(id):
    task = Task.query.get(id)

    if not task:
        return jsonify({"message": "Tarefa não encontrada"}), 404

    db.session.delete(task)
    db.session.commit()

    return jsonify({"message": "Tarefa deletada com sucesso"})