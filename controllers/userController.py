from flask import request, jsonify
from config.connection import db
from models.userModel import User
from models.roleModel import Role

class UserController:
    
    @staticmethod
    def get_all_users():
        users = User.query.all()
        return jsonify([user.to_dict() for user in users])
    
    @staticmethod
    def get_user(user_id):
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        return jsonify(user.to_dict())
    
    @staticmethod
    def create_user():
        data = request.get_json()
        
        if User.query.filter_by(correo=data.get('correo')).first():
            return jsonify({'error': 'El correo ya está registrado'}), 400
        
        user = User(
            dni=data.get('dni'),
            nombres=data.get('nombres'),
            apellidos=data.get('apellidos'),
            telefono=data.get('telefono'),
            departamento=data.get('departamento'),
            correo=data.get('correo'),
            role_id=data.get('role_id')
        )
        user.set_password(data.get('password'))
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({'message': 'Usuario creado exitosamente', 'user': user.to_dict()}), 201
    
    @staticmethod
    def update_user(user_id):
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        data = request.get_json()
        if 'nombres' in data:
            user.nombres = data['nombres']
        if 'apellidos' in data:
            user.apellidos = data['apellidos']
        if 'telefono' in data:
            user.telefono = data['telefono']
        if 'departamento' in data:
            user.departamento = data['departamento']
        if 'role_id' in data:
            user.role_id = data['role_id']
        
        db.session.commit()
        return jsonify({'message': 'Usuario actualizado', 'user': user.to_dict()})
    
    @staticmethod
    def delete_user(user_id):
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'Usuario eliminado'})
    
    @staticmethod
    def get_technicians():
        technicians_role = Role.query.filter_by(name='tecnico').first()
        if not technicians_role:
            return jsonify([])
        
        technicians = User.query.filter_by(role_id=technicians_role.id).all()
        return jsonify([tech.to_dict() for tech in technicians])