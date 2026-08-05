from flask import jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import db
from app.models import Customer, ServiceTicket
from app.service_ticket.schemas import service_tickets_schema
from app.utils.util import encode_token, token_required

from . import customer_bp
from .schemas import customer_schema, customers_schema, login_schema


@customer_bp.route("/", methods=["POST"])
def create_customer():
    try:
        data = request.json
        if "password" in data:
            data["password"] = generate_password_hash(data["password"])

        new_customer = customer_schema.load(data)
        db.session.add(new_customer)
        db.session.commit()
        return customer_schema.jsonify(new_customer), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 400


@customer_bp.route("/", methods=["GET"])
def get_customers():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 5, type=int)

    paginated_customers = Customer.query.paginate(
        page=page, per_page=per_page, error_out=False
    )
    return customers_schema.jsonify(paginated_customers.items), 200


@customer_bp.route("/login", methods=["POST"])
def login():
    try:
        user_data = login_schema.load(request.json)
    except Exception as e:
        return jsonify({"message": "Invalid format", "errors": str(e)}), 400

    customer = Customer.query.filter_by(email=user_data.email).first()

    if customer and check_password_hash(customer.password, user_data.password):
        token = encode_token(customer.id)
        return jsonify({"message": "Login successful", "token": token}), 200
    else:
        return jsonify({"message": "Invalid email or password"}), 401


@customer_bp.route("/my-tickets", methods=["GET"])
@token_required
def my_tickets(customer_id):
    tickets = ServiceTicket.query.filter_by(customer_id=customer_id).all()
    return service_tickets_schema.jsonify(tickets), 200


@customer_bp.route("/<int:id>", methods=["PUT"])
@token_required
def update_customer(customer_id, id):
    if customer_id != id:
        return jsonify({"message": "Unauthorized to update this account."}), 403

    customer = Customer.query.get_or_404(id)
    try:
        data = request.json
        if "password" in data:
            data["password"] = generate_password_hash(data["password"])

        customer_schema.load(data, instance=customer, partial=True)
        db.session.commit()
        return customer_schema.jsonify(customer), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400


@customer_bp.route("/<int:id>", methods=["DELETE"])
@token_required
def delete_customer(customer_id, id):
    if customer_id != id:
        return jsonify({"message": "Unauthorized to delete this account."}), 403

    customer = Customer.query.get_or_404(id)
    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": f"Customer {id} successfully deleted."}), 200
