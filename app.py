from flask import Flask
from flask_cors import CORS
from config.connection import get_db_connection
from models.roleModel import Role
from models.userModel import User
from models.ticketModel import Ticket
from routes.authRoutes import auth_routes
from routes.userRoutes import user_routes
from routes.ticketRoutes import ticket_routes
import os

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    db = get_db_connection(app)
    
    app.register_blueprint(auth_routes, url_prefix='/api')
    app.register_blueprint(user_routes, url_prefix='/api')
    app.register_blueprint(ticket_routes, url_prefix='/api')
    
    with app.app_context():
        Role.create_table_if_not_exists()
        User.create_table_if_not_exists()
        Ticket.create_table_if_not_exists()
        
        default_roles = ['admin', 'tecnico', 'usuario']
        for role_name in default_roles:
            if not Role.query.filter_by(name=role_name).first():
                role = Role(name=role_name, description=f'Rol de {role_name}')
                db.session.add(role)
        
        db.session.commit()
        print("Tablas y datos iniciales creados")
    
    return app

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    app.run(debug=debug, host='0.0.0.0', port=port)