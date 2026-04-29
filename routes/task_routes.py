from flask import Blueprint, request, jsonify
from database import db
from models.task import Task
from flask_jwt_extended import jwt_required, get_jwt_identity


task_bp = Blueprint("task_bp", __name__)


@task_bp.route("/tasks", methods=["POST"])
@jwt_required()
def create_task():
    """
    Criar nova tarefa
    ---
    tags:
      - Tarefas
    security:
      - Bearer: []
    parameters:
      - name: body
        in: body
        required: true
        schema:
          properties:
            title:
              type: string
            description:
              type: string
    responses:
      201:
        description: Tarefa criada com sucesso
      401:
        description: Token inválido ou ausente
    """
    data = request.get_json()
    user_id = get_jwt_identity()

    new_task = Task(
        title=data["title"],
        description=data.get("description", ""),
        user_id=user_id
    )

    db.session.add(new_task)
    db.session.commit()

    return jsonify({
        "message": "Tarefa criada com sucesso",
        "id": new_task.id
    }), 201


@task_bp.route("/tasks", methods=["GET"])
@jwt_required()
def get_tasks():
    """
    Listar tarefas do usuário logado
    ---
    tags:
      - Tarefas
    security:
      - Bearer: []
    responses:
      200:
        description: Lista de tarefas retornada com sucesso
      401:
        description: Token inválido ou ausente
    """
    user_id = get_jwt_identity()

    tasks = Task.query.filter_by(user_id=user_id).all()

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
@jwt_required()
def get_task(id):

    user_id = get_jwt_identity()

    task = Task.query.get(id)

    if not task:
        return jsonify({"message": "Tarefa não encontrada"}), 404

    if task.user_id != int(user_id):
        return jsonify({"message": "Acesso negado"}), 403

    return jsonify({
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "completed": task.completed
    })

@task_bp.route("/tasks/<int:id>", methods=["PUT"])
@jwt_required()
def update_task(id):
    user_id = get_jwt_identity()

    task = Task.query.filter_by(id=id, user_id=user_id).first()

    if not task:
        return jsonify({"message": "Tarefa não encontrada"}), 404

    data = request.get_json()

    task.title = data.get("title", task.title)
    task.description = data.get("description", task.description)
    task.completed = data.get("completed", task.completed)

    db.session.commit()

    return jsonify({"message": "Tarefa atualizada com sucesso"})


@task_bp.route("/tasks/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_task(id):
    user_id = get_jwt_identity()

    task = Task.query.filter_by(id=id, user_id=user_id).first()

    if not task:
        return jsonify({"message": "Tarefa não encontrada"}), 404

    db.session.delete(task)
    db.session.commit()

    return jsonify({"message": "Tarefa deletada com sucesso"})

@task_bp.route("/tasks/<int:id>/complete", methods=["PATCH"])
@jwt_required()
def complete_task(id):
    """
    Marcar tarefa como concluída
    ---
    tags:
      - Tarefas
    security:
      - Bearer: []
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Tarefa marcada como concluída
      404:
        description: Tarefa não encontrada
    """

    user_id = get_jwt_identity()

    task = Task.query.filter_by(id=id, user_id=user_id).first()

    if not task:
        return jsonify({"message": "Tarefa não encontrada"}), 404

    task.completed = True

    db.session.commit()

    return jsonify({"message": "Tarefa marcada como concluída"})