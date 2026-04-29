from flask import Blueprint, request, jsonify
from database import db
from models.user import User
from flask_jwt_extended import create_access_token
from flask_bcrypt import Bcrypt


bcrypt = Bcrypt()

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():

    """
Cadastro de usuário
---
tags:
  - Autenticação
parameters:
  - name: body
    in: body
    required: true
    schema:
      properties:
        username:
          type: string
        password:
          type: string
responses:
  200:
    description: Usuário criado com sucesso
"""
    data = request.get_json()

    password_hash = bcrypt.generate_password_hash(data["password"]).decode("utf-8")

    user = User(
        username=data["username"],
        password=password_hash
    )

    db.session.add(user)
    db.session.commit()

    return jsonify(message="Usuário criado com sucesso")


@auth_bp.route("/login", methods=["POST"])
def login():
    """
Login do usuário
---
tags:
  - Autenticação
parameters:
  - name: body
    in: body
    required: true
    schema:
      properties:
        username:
          type: string
        password:
          type: string
responses:
  200:
    description: Token JWT gerado com sucesso
  401:
    description: Credenciais inválidas
"""
    data = request.get_json()

    user = User.query.filter_by(
        username=data["username"]
    ).first()

    if user and bcrypt.check_password_hash(user.password, data["password"]):
        token = create_access_token(
            identity=str(user.id)
        )

        return jsonify(access_token=token)

    return jsonify(message="Credenciais inválidas"), 401