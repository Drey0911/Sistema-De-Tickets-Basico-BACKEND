from flask import request, jsonify
from config.connection import db
from models.ticketModel import Ticket
from models.userModel import User
from models.roleModel import Role
from datetime import datetime

class TicketController:
    
    @staticmethod
    def get_all_tickets():
        tickets = Ticket.query.all()
        return jsonify([ticket.to_dict() for ticket in tickets])
    
    @staticmethod
    def get_user_tickets(user_id):
        tickets = Ticket.query.filter_by(usuario_id=user_id).all()
        return jsonify([ticket.to_dict() for ticket in tickets])
    
    @staticmethod
    def get_technician_tickets(technician_id):
        tickets = Ticket.query.filter_by(tecnico_id=technician_id).order_by(
            db.case(
                (Ticket.estado != 'completado', 1),
                else_=2
            ),
            db.case(
                (Ticket.prioridad == 'alta', 1),
                (Ticket.prioridad == 'media', 2),
                (Ticket.prioridad == 'baja', 3),
                else_=4
            ),
            Ticket.fecha_creacion.desc()
        ).all()
        return jsonify([ticket.to_dict() for ticket in tickets])
    
    @staticmethod
    def create_ticket():
        data = request.get_json()
        
        ticket = Ticket(
            titulo=data.get('titulo'),
            descripcion=data.get('descripcion'),
            prioridad=data.get('prioridad', 'media'),
            usuario_id=data.get('usuario_id')
        )
        
        db.session.add(ticket)
        db.session.commit()
        
        return jsonify({'message': 'Ticket creado', 'ticket': ticket.to_dict()}), 201
    
    @staticmethod
    def update_ticket(ticket_id):
        ticket = Ticket.query.get(ticket_id)
        if not ticket:
            return jsonify({'error': 'Ticket no encontrado'}), 404
        
        data = request.get_json()
        if 'titulo' in data:
            ticket.titulo = data['titulo']
        if 'descripcion' in data:
            ticket.descripcion = data['descripcion']
        if 'prioridad' in data:
            ticket.prioridad = data['prioridad']
        if 'estado' in data:
            ticket.estado = data['estado']
            if data['estado'] == 'completado' and not ticket.fecha_completado:
                ticket.fecha_completado = datetime.utcnow()
        
        db.session.commit()
        return jsonify({'message': 'Ticket actualizado', 'ticket': ticket.to_dict()})
    
    @staticmethod
    def assign_ticket(ticket_id):
        ticket = Ticket.query.get(ticket_id)
        if not ticket:
            return jsonify({'error': 'Ticket no encontrado'}), 404
        
        data = request.get_json()
        ticket.tecnico_id = data.get('tecnico_id')
        ticket.admin_asignador_id = data.get('admin_asignador_id')
        
        db.session.commit()
        return jsonify({'message': 'Ticket asignado', 'ticket': ticket.to_dict()})
    
    @staticmethod
    def delete_ticket(ticket_id):
        ticket = Ticket.query.get(ticket_id)
        if not ticket:
            return jsonify({'error': 'Ticket no encontrado'}), 404
        
        db.session.delete(ticket)
        db.session.commit()
        return jsonify({'message': 'Ticket eliminado'})