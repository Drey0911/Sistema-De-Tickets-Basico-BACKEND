from flask import request, jsonify
import jwt
import datetime
import os
from config.connection import db
from models.userModel import User
from models.roleModel import Role

class AuthController:
    
    @staticmethod
    def login():
        data = request.get_json()
        correo = data.get('correo')
        password = data.get('password')
        
        user = User.query.filter_by(correo=correo).first()
        if not user or not user.check_password(password):
            return jsonify({'error': 'Credenciales inválidas'}), 401
        
        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, os.getenv('JWT_SECRET_KEY'), algorithm=os.getenv('JWT_ALGORITHM'))
        
        return jsonify({
            'token': token,
            'user': user.to_dict()
        })
    
    @staticmethod
    def register():
        data = request.get_json()
        
        if User.query.filter_by(correo=data.get('correo')).first():
            return jsonify({'error': 'El correo ya está registrado'}), 400
        
        if User.query.filter_by(dni=data.get('dni')).first():
            return jsonify({'error': 'El DNI ya está registrado'}), 400
        
        user_role = Role.query.filter_by(name='usuario').first()
        if not user_role:
            return jsonify({'error': 'Rol de usuario no encontrado'}), 500
        
        user = User(
            dni=data.get('dni'),
            nombres=data.get('nombres'),
            apellidos=data.get('apellidos'),
            telefono=data.get('telefono'),
            departamento=data.get('departamento'),
            correo=data.get('correo'),
            role_id=user_role.id
        )
        user.set_password(data.get('password'))
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({'message': 'Usuario registrado exitosamente', 'user': user.to_dict()}), 201