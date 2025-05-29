from application.database import db
from application.user_datastore import user_datastore

from flask import current_app as app
from flask import request, make_response, jsonify
from flask_restful import Resource
from flask_security import utils, auth_token_required

@app.route('/api/auth/register', methods = ['POST'])
def register():
    body_content = request.get_json()

    if 'email' not in body_content or 'password' not in body_content:
        return make_response(jsonify({
            'message': 'email & password are required'
        }),400)
    
    email = body_content.get('email')
    password = body_content.get('password')

    user = user_datastore.find_user(email=email)
    if user:
        return make_response(jsonify({
            'message': 'User already exists'
        }), 400)
    
    user_role = user_datastore.find_role('user')
    user = user_datastore.create_user(email=email, password=password, roles=[user_role])
    db.session.commit()

    return make_response(jsonify({
        'message': 'User created!',
        'user': {
            'email': user.email,
            'roles': [role.name for role in user.roles]
        }
    }), 201)

class Login(Resource):
    def post(self):
        login_credentials = request.get_json()

        if 'email' not in login_credentials or 'password' not in login_credentials:
            return make_response(jsonify({
                'message': 'email & password are required'
            }), 400)
        
        email = login_credentials.get('email')
        password = login_credentials.get('password')

        user = user_datastore.find_user(email=email)
        if not user:
            return make_response(jsonify({
                'message': 'User does not exists!'
            }), 404)
        
        if not utils.verify_password(password, user.password):
            return make_response(jsonify({
                'message': 'Invalid password'
            }), 401)
        
        utils.login_user(user)

        auth_token = user.get_auth_token()

        return make_response(jsonify({
            'message': 'Login successful',
            'user': {
                'email': user.email,
                'roles': [role.name for role in user.roles]
            },
            'auth_token': auth_token
        }), 200)

class Logout(Resource):
    @auth_token_required
    def post(self):
        utils.logout_user()
        return make_response(jsonify({
            'message': 'Logout successful'
        }), 200)