from flask import jsonify, request

from app.extensions import cache, db
from app.models import Mechanic

from . import mechanic_bp
from .schemas import mechanic_schema, mechanics_schema


@mechanic_bp.route("/", methods=["POST"])
def create_mechanic():
    try:
        new_mechanic = mechanic_schema.load(request.json)
        db.session.add(new_mechanic)
        db.session.commit()
        return mechanic_schema.jsonify(new_mechanic), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 400


@mechanic_bp.route("/", methods=["GET"])
@cache.cached(timeout=60)
def get_mechanics():
    mechanics = Mechanic.query.all()
    return mechanics_schema.jsonify(mechanics), 200


@mechanic_bp.route("/<int:id>", methods=["PUT"])
def update_mechanic(id):
    mechanic = Mechanic.query.get_or_404(id)
    try:
        mechanic_schema.load(request.json, instance=mechanic, partial=True)
        db.session.commit()
        return mechanic_schema.jsonify(mechanic), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400


@mechanic_bp.route("/<int:id>", methods=["DELETE"])
def delete_mechanic(id):
    mechanic = Mechanic.query.get_or_404(id)
    db.session.delete(mechanic)
    db.session.commit()
    return jsonify({"message": f"Mechanic {id} deleted."}), 200


@mechanic_bp.route("/top-mechanics", methods=["GET"])
def get_top_mechanics():

    mechanics = Mechanic.query.all()

    mechanics.sort(key=lambda m: len(m.tickets), reverse=True)

    return mechanics_schema.jsonify(mechanics), 200
