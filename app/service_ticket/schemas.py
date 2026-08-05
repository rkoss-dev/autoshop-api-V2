from marshmallow import fields

from app.extensions import ma
from app.models import ServiceTicket


class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):
    mechanics = fields.Nested("MechanicSchema", many=True, exclude=("tickets",))

    parts = fields.Nested("InventorySchema", many=True, exclude=("tickets",))

    class Meta:
        model = ServiceTicket
        load_instance = True
        include_fk = True

        fields = (
            "id",
            "VIN",
            "service_date",
            "service_description",
            "customer_id",
            "mechanics",
            "parts",
        )


service_ticket_schema = ServiceTicketSchema()
service_tickets_schema = ServiceTicketSchema(many=True)
