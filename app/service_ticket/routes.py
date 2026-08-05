from flask import jsonify, request

from app.extensions import db, limiter
from app.models import Inventory, Mechanic, ServiceTicket

from . import service_ticket_bp
from .schemas import service_ticket_schema, service_tickets_schema


@service_ticket_bp.route("/", methods=["POST"])
@limiter.limit("3 per minute")
def create_service_ticket():
    try:
        new_ticket = service_ticket_schema.load(request.json)
        db.session.add(new_ticket)
        db.session.commit()
        return service_ticket_schema.jsonify(new_ticket), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 400


@service_ticket_bp.route("/", methods=["GET"])
def get_service_tickets():
    tickets = ServiceTicket.query.all()
    return service_tickets_schema.jsonify(tickets), 200


@service_ticket_bp.route(
    "/<int:ticket_id>/assign-mechanic/<int:mechanic_id>", methods=["PUT"]
)
def assign_mechanic(ticket_id, mechanic_id):
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
def remove_mechanic(ticket_id, mechanic_id):
    ticket = ServiceTicket.query.get_or_404(ticket_id)
    mechanic = Mechanic.query.get_or_404(mechanic_id)

    if mechanic in ticket.mechanics:
        ticket.mechanics.remove(mechanic)
        db.session.commit()
        return jsonify({"message": "Mechanic removed."}), 200

    return jsonify({"message": "Mechanic not assigned."}), 400


@service_ticket_bp.route("//edit", methods=["PUT"])
def edit_ticket_mechanics(ticket_id):
    ticket = ServiceTicket.query.get_or_404(ticket_id)

    data = request.json
    add_ids = data.get("add_ids", [])
    remove_ids = data.get("remove_ids", [])

    for mech_id in add_ids:
        mechanic = Mechanic.query.get(mech_id)
        if mechanic and mechanic not in ticket.mechanics:
            ticket.mechanics.append(mechanic)

    for mech_id in remove_ids:
        mechanic = Mechanic.query.get(mech_id)
        if mechanic and mechanic in ticket.mechanics:
            ticket.mechanics.remove(mechanic)

    db.session.commit()

    return service_ticket_schema.jsonify(ticket), 200


@service_ticket_bp.route("//add-part/", methods=["PUT"])
def add_part(ticket_id, part_id):
    ticket = ServiceTicket.query.get_or_404(ticket_id)
    part = Inventory.query.get_or_404(part_id)

    if part not in ticket.parts:
        ticket.parts.append(part)
        db.session.commit()
        return jsonify(
            {"message": f"Part '{part.name}' added to Ticket #{ticket_id}."}
        ), 200

    return jsonify({"message": "This part is already attached to this ticket."}), 400
