from config.connection import db
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

class Ticket(db.Model):
    __tablename__ = 'tickets'
    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    prioridad = db.Column(db.String(20), nullable=False, default='media')
    estado = db.Column(db.String(20), nullable=False, default='abierto')
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_modificacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    fecha_completado = db.Column(db.DateTime, nullable=True)
    usuario_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)
    tecnico_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=True)
    admin_asignador_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=True)
    
    usuario = relationship('User', foreign_keys=[usuario_id], backref=db.backref('tickets_creados', lazy='dynamic'))
    tecnico = relationship('User', foreign_keys=[tecnico_id], backref=db.backref('tickets_asignados', lazy='dynamic'))
    admin_asignador = relationship('User', foreign_keys=[admin_asignador_id])
    
    def to_dict(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'descripcion': self.descripcion,
            'prioridad': self.prioridad,
            'estado': self.estado,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'fecha_modificacion': self.fecha_modificacion.isoformat() if self.fecha_modificacion else None,
            'fecha_completado': self.fecha_completado.isoformat() if self.fecha_completado else None,
            'usuario': self.usuario.to_dict() if self.usuario else None,
            'tecnico': self.tecnico.to_dict() if self.tecnico else None,
            'admin_asignador': self.admin_asignador.to_dict() if self.admin_asignador else None
        }
    
    @classmethod
    def create_table_if_not_exists(cls):
        try:
            inspector = db.inspect(db.engine)
            if not inspector.has_table(cls.__tablename__):
                cls.__table__.create(db.engine)
                print(f"Tabla {cls.__tablename__} creada")
            else:
                print(f"Tabla {cls.__tablename__} ya existe")
        except SQLAlchemyError as e:
            print(f"Error al crear tabla: {str(e)}")