from flask import jsonify, request

from app.extensions import db, limiter
from app.models import Inventory, Mechanic, ServiceTicket
from app.utils.util import token_required

from . import service_ticket_bp
from .schemas import service_ticket_schema, service_tickets_schema


@service_ticket_bp.route("/", methods=["POST"])
@token_required
@limiter.limit("3 per minute")
def create_service_ticket(customer_id):
    try:
        data = request.json
        data["customer_id"] = customer_id
        new_ticket = service_ticket_schema.load(data)
        db.session.add(new_ticket)
        db.session.commit()
        return service_ticket_schema.jsonify(new_ticket), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 400


@service_ticket_bp.route("/", methods=["GET"])
@token_required
def get_service_tickets(customer_id):
    tickets = ServiceTicket.query.all()
    return service_tickets_schema.jsonify(tickets), 200


@service_ticket_bp.route(
    "/<int:ticket_id>/assign-mechanic/<int:mechanic_id>", methods=["PUT"]
)
@token_required
def assign_mechanic(customer_id, ticket_id, mechanic_id):
    ticket = ServiceTicket.query.get_or_404(ticket_id)
    mechanic = Mechanic.query.get_or_404(mechanic_id)

    if mechanic not in ticket.mechanics:
        ticket.mechanics.append(mechanic)
        db.session.commit()
        return jsonify({"message": "Mechanic assigned."}), 200

    return jsonify({"message": "Mechanic already assigned."}), 400


@service_ticket_bp.route(
    "/<int:ticket_id>/remove-mechanic/<int:mechanic_id>", methods=["PUT"]
)
@token_required
def remove_mechanic(customer_id, ticket_id, mechanic_id):
    ticket = ServiceTicket.query.get_or_404(ticket_id)
    mechanic = Mechanic.query.get_or_404(mechanic_id)

    if mechanic in ticket.mechanics:
        ticket.mechanics.remove(mechanic)
        db.session.commit()
        return jsonify({"message": "Mechanic removed."}), 200

    return jsonify({"message": "Mechanic not assigned."}), 400


@service_ticket_bp.route("/<int:ticket_id>/edit", methods=["PUT"])
@token_required
def edit_ticket_mechanics(customer_id, ticket_id):
    ticket = ServiceTicket.query.get_or_404(ticket_id)
    data = request.json
    add_ids = data.get("add_ids", [])
    remove_ids = data.get("remove_ids", [])

    if add_ids:
        mechanics_to_add = Mechanic.query.filter(Mechanic.id.in_(add_ids)).all()
        for mechanic in mechanics_to_add:
            if mechanic not in ticket.mechanics:
                ticket.mechanics.append(mechanic)

    if remove_ids:
        mechanics_to_remove = Mechanic.query.filter(Mechanic.id.in_(remove_ids)).all()
        for mechanic in mechanics_to_remove:
            if mechanic in ticket.mechanics:
                ticket.mechanics.remove(mechanic)

    db.session.commit()
    return service_ticket_schema.jsonify(ticket), 200


@service_ticket_bp.route("/<int:ticket_id>/add-part/<int:part_id>", methods=["PUT"])
@token_required
def add_part(customer_id, ticket_id, part_id):
    ticket = ServiceTicket.query.get_or_404(ticket_id)
    part = Inventory.query.get_or_404(part_id)

    if part not in ticket.parts:
        ticket.parts.append(part)
        db.session.commit()
        return jsonify(
            {"message": f"Part '{part.name}' added to Ticket #{ticket_id}."}
        ), 200

    return jsonify({"message": "This part is already attached to this ticket."}), 400
