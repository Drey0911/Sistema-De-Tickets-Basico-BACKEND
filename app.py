from flask import Flask, jsonify
from flask_cors import CORS
from config.connection import get_db_connection
from models.roleModel import Role
from models.userModel import User
from models.ticketModel import Ticket
from routes.authRoutes import auth_routes
from routes.userRoutes import user_routes
from routes.ticketRoutes import ticket_routes
import os
import time

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    # Configurar la base de datos
    db = get_db_connection(app)
    
    # Registrar blueprints
    app.register_blueprint(auth_routes, url_prefix='/api')
    app.register_blueprint(user_routes, url_prefix='/api')
    app.register_blueprint(ticket_routes, url_prefix='/api')
    
    # Endpoint de health check
    @app.route('/health')
    def health_check():
        return jsonify({
            'status': 'healthy', 
            'message': 'La app funciona bien',
            'database': 'unknown'
        }), 200
    
    @app.route('/')
    def index():
        return jsonify({'message': 'Ticket System API'}), 200
    
    # Intentar inicializar la base de datos con manejo de errores
    def initialize_database():
        max_retries = 3
        for attempt in range(max_retries):
            try:
                with app.app_context():
                    print(f"Intentando conectar a la base de datos (intento {attempt + 1})...")
                    
                    # Crear tablas
                    Role.create_table_if_not_exists()
                    User.create_table_if_not_exists()
                    Ticket.create_table_if_not_exists()
                    
                    # Crear roles por defecto
                    default_roles = ['admin', 'tecnico', 'usuario']
                    for role_name in default_roles:
                        if not Role.query.filter_by(name=role_name).first():
                            role = Role(name=role_name, description=f'Rol de {role_name}')
                            db.session.add(role)
                    
                    db.session.commit()
                    print("Tablas y datos iniciales creados exitosamente")
                    return True
                    
            except Exception as e:
                print(f"Error en intento {attempt + 1}: {e}")
                if attempt < max_retries - 1:
                    print("Reintentando en 5 segundos...")
                    time.sleep(5)
                else:
                    print("No se pudo conectar a la base de datos después de varios intentos")
                    print("La aplicación continuará ejecutándose para health checks")
                    return False
    
    # Inicializar base de datos en segundo plano
    import threading
    db_init_thread = threading.Thread(target=initialize_database)
    db_init_thread.daemon = True
    db_init_thread.start()
    
    return app

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    debug = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    print(f"Iniciando aplicación en puerto {port}...")
    app.run(debug=debug, host='0.0.0.0', port=port)