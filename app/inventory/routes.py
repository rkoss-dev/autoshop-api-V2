from flask import jsonify, request

from app.extensions import db
from app.models import Inventory

from . import inventory_bp
from .schemas import inventories_schema, inventory_schema


@inventory_bp.route("/", methods=["POST"])
def create_part():
    try:
        new_part = inventory_schema.load(request.json)
        db.session.add(new_part)
        db.session.commit()
        return inventory_schema.jsonify(new_part), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 400


@inventory_bp.route("/", methods=["GET"])
def get_parts():
    parts = Inventory.query.all()
    return inventories_schema.jsonify(parts), 200


@inventory_bp.route("/", methods=["PUT"])
def update_part(id):
    part = Inventory.query.get_or_404(id)
    try:
        inventory_schema.load(request.json, instance=part, partial=True)
        db.session.commit()
        return inventory_schema.jsonify(part), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400


@inventory_bp.route("/", methods=["DELETE"])
def delete_part(id):
    part = Inventory.query.get_or_404(id)
    db.session.delete(part)
    db.session.commit()
    return jsonify({"message": f"Part '{part.name}' successfully deleted."}), 200
