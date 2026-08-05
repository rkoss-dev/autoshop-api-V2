from flask import Blueprint

customer_bp = Blueprint("customer_bp", __name__)
from . import routes  # Import routes last so the blueprint is created first
