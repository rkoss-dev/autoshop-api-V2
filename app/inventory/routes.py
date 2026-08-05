from flask import jsonify, request

from app.extensions import db
from app.models import Inventory
from app.utils.util import token_required

from . import inventory_bp
from .schemas import inventories_schema, inventory_schema


@inventory_bp.route("/", methods=["POST"])
@token_required
def create_part(customer_id):
    try:
        new_part = inventory_schema.load(request.json)
        db.session.add(new_part)
        db.session.commit()
        return inventory_schema.jsonify(new_part), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 400


@inventory_bp.route("/", methods=["GET"])
def get_parts():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    paginated_parts = Inventory.query.paginate(
        page=page, per_page=per_page, error_out=False
    )
    return inventories_schema.jsonify(paginated_parts.items), 200


@inventory_bp.route("/<int:id>", methods=["PUT"])
@token_required
def update_part(customer_id, id):
    part = Inventory.query.get_or_404(id)
    try:
        inventory_schema.load(request.json, instance=part, partial=True)
        db.session.commit()
        return inventory_schema.jsonify(part), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400


@inventory_bp.route("/<int:id>", methods=["DELETE"])
@token_required
def delete_part(customer_id, id):
    part = Inventory.query.get_or_404(id)
    db.session.delete(part)
    db.session.commit()
    return jsonify({"message": f"Part '{part.name}' successfully deleted."}), 200
