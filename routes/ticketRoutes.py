from flask import Blueprint
from controllers.ticketController import TicketController
from middleware.authMiddleware import token_required

ticket_routes = Blueprint('ticket_routes', __name__)

@ticket_routes.route('/tickets', methods=['GET'])
@token_required
def get_all_tickets():
    return TicketController.get_all_tickets()

@ticket_routes.route('/tickets/user/<int:user_id>', methods=['GET'])
@token_required
def get_user_tickets(user_id):
    return TicketController.get_user_tickets(user_id)

@ticket_routes.route('/tickets/technician/<int:technician_id>', methods=['GET'])
@token_required
def get_technician_tickets(technician_id):
    return TicketController.get_technician_tickets(technician_id)

@ticket_routes.route('/tickets', methods=['POST'])
@token_required
def create_ticket():
    return TicketController.create_ticket()

@ticket_routes.route('/tickets/<int:ticket_id>', methods=['PUT'])
@token_required
def update_ticket(ticket_id):
    return TicketController.update_ticket(ticket_id)

@ticket_routes.route('/tickets/<int:ticket_id>/assign', methods=['PUT'])
@token_required
def assign_ticket(ticket_id):
    return TicketController.assign_ticket(ticket_id)

@ticket_routes.route('/tickets/<int:ticket_id>', methods=['DELETE'])
@token_required
def delete_ticket(ticket_id):
    return TicketController.delete_ticket(ticket_id)