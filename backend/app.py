from flask import Flask, jsonify, request, make_response
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin

app = Flask(__name__)
api = Api(app)


# db.init_app(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite3.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECURITY_PASSWORD_SALT'] = 'my_precious_two'
app.config['SECRET_KEY'] = 'my_precious'
db = SQLAlchemy(app)
# db.init_app(app)

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    Email = db.Column(db.String(255), unique=True, nullable=False)
    Password = db.Column(db.String(255), nullable = False)
    Username = db.Column(db.String(255), nullable = False)
    Qualification = db.Column(db.String(255), nullable = False)
    DOB = db.Column(db.String(255), nullable = False)

    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    fs_token_uniquifier = db.Column(db.String(255), unique=True, nullable=True)

    roles = db.relationship('Roles', secondary='user_roles')

class Roles(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(255))

class UserRoles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

database = []

class UserDetails(Resource):
    def get(self):
        return make_response(jsonify(database),200)
    def post(self):
        user_details = request.get_json()
        print(user_details)
        if not user_details:
            return jsonify({'error': 'NOuser details provided'})
        else:
            database.append(user_details)
            return jsonify({'message': 'User added successfully', 'user': user_details})

api.add_resource(UserDetails, '/api/users')

# @app.route('/api/get_users' , methods = ['GET'])
# def get_users():
#     return jsonify(database)

# @app.route('/api/add_user', methods=['POST'])
# def add_user():
#     user_details = request.get_json()
#     if not user_details:
#         return jsonify({'error': 'No user details provided'}), 400
#     else:
#         database.append(user_details)
#         return jsonify({'message': 'User added successfully', 'user': user_details}), 201

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
