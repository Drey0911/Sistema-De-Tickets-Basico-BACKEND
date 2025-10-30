from flask import Blueprint
from controllers.authController import AuthController

auth_routes = Blueprint('auth_routes', __name__)

@auth_routes.route('/auth/login', methods=['POST'])
def login():
    return AuthController.login()

@auth_routes.route('/auth/register', methods=['POST'])
def register():
    return AuthController.register()