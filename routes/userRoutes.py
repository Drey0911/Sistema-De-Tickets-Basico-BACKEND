from flask import Blueprint
from controllers.userController import UserController
from middleware.authMiddleware import token_required

user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/users', methods=['GET'])
@token_required
def get_all_users():
    return UserController.get_all_users()

@user_routes.route('/users/<int:user_id>', methods=['GET'])
@token_required
def get_user(user_id):
    return UserController.get_user(user_id)

@user_routes.route('/users', methods=['POST'])
@token_required
def create_user():
    return UserController.create_user()

@user_routes.route('/users/<int:user_id>', methods=['PUT'])
@token_required
def update_user(user_id):
    return UserController.update_user(user_id)

@user_routes.route('/users/<int:user_id>', methods=['DELETE'])
@token_required
def delete_user(user_id):
    return UserController.delete_user(user_id)

@user_routes.route('/users/technicians', methods=['GET'])
@token_required
def get_technicians():
    return UserController.get_technicians()