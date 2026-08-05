from flask import jsonify, request
from sqlalchemy import func

from app.extensions import cache, db
from app.models import Mechanic, ServiceTicket
from app.utils.util import token_required

from . import mechanic_bp
from .schemas import mechanic_schema, mechanics_schema


@mechanic_bp.route("/", methods=["POST"])
@token_required
def create_mechanic(customer_id):
    try:
        new_mechanic = mechanic_schema.load(request.json)
        db.session.add(new_mechanic)
        db.session.commit()
        cache.delete("mechanics_list")
        return mechanic_schema.jsonify(new_mechanic), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 400


@mechanic_bp.route("/", methods=["GET"])
@cache.cached(timeout=60, key_prefix="mechanics_list")
def get_mechanics():
    mechanics = Mechanic.query.all()
    return mechanics_schema.jsonify(mechanics), 200


@mechanic_bp.route("/<int:id>", methods=["PUT"])
@token_required
def update_mechanic(customer_id, id):
    mechanic = Mechanic.query.get_or_404(id)
    try:
        mechanic_schema.load(request.json, instance=mechanic, partial=True)
        db.session.commit()
        cache.delete("mechanics_list")
        return mechanic_schema.jsonify(mechanic), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400


@mechanic_bp.route("/<int:id>", methods=["DELETE"])
@token_required
def delete_mechanic(customer_id, id):
    mechanic = Mechanic.query.get_or_404(id)
    db.session.delete(mechanic)
    db.session.commit()
    cache.delete("mechanics_list")
    return jsonify({"message": f"Mechanic {id} deleted."}), 200


@mechanic_bp.route("/top-mechanics", methods=["GET"])
def get_top_mechanics():
    mechanics = (
        db.session.query(Mechanic)
        .join(ServiceTicket, Mechanic.tickets)
        .group_by(Mechanic.id)
        .order_by(func.count(ServiceTicket.id).desc())
        .all()
    )

    return mechanics_schema.jsonify(mechanics), 200
