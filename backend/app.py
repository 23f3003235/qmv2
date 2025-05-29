from flask import Flask, jsonify, request, make_response
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin

from application.models import *
from application.user_datastore import user_datastore
from application.database import db



app = Flask(__name__)
api=Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECURITY_PASSWORD_SALT'] = 'my_precious_two'
app.config['SECRET_KEY'] = 'my_precious'

db.init_app(app)

# user_datastore = SQLAlchemyUserDatastore(db, Users, Roles)
security = Security(app, user_datastore)

with app.app_context():
    db.create_all()

    admin_role = user_datastore.find_or_create_role(name='admin', description='Administrator role')
    user_role = user_datastore.find_or_create_role(name='user', description='User role')

    if not user_datastore.find_user(email="admin@gmail.com"):
        user_datastore.create_user(
            email = "admin@gmail.com",
            password    = "admin123",
            roles = [user_role, admin_role],
        )

    db.session.commit()



# role = Roles.filter_by(name='admin').first()


# user = Users(
#     email = 'admin@gmail.com',
#     password = 'admin123',
#     roles = [role],
# )
# db.session.add(user)
# db.session.commit()

# get_user = Users.query.filter_by(email = "admin@gmail.com").first()
# role = Roles.query.filter_by(name='admin').first()

# userrole = UserRoles(
#     user_id = get_user.id,
#     role_id = role.id
# )

# db.session.add(userrole)
# db.session.commit()





database = []

class UserDetails(Resource):
    def get(self):
        return make_response(jsonify(database),200)
    
    def post(self):
        user_details = request.get_json()
        print(user_details)
        if not user_details:
            return jsonify({'error': 'No user details provided'})
        else:
            database.append(user_details)
            return jsonify({'message': 'User added successfully', 'user': user_details})
        
    def delete(self, str1, str2):
        len1 = len(str1)
        len2 = len(str2)
        result = {
            'total_length': len1 + len2,
        }

        return make_response(jsonify(result), 203)
        
api.add_resource(UserDetails, '/api/users', '/api/users/<string:str1>/<string:str2>')


@app.route('/api/get_users' , methods = ['GET'])
def get_users():
    return jsonify(database)

@app.route('/api/add_user', methods=['POST'])
def add_user():
    user_details = request.get_json()
    if not user_details:
        return jsonify({'error': 'No user details provided'}), 400
    else:
        database.append(user_details)
        return jsonify({'message': 'User added successfully', 'user': user_details}), 201
    

@app.route('/api/hello_world', methods=['GET'])
def hello_world():
    return jsonify({'message': 'Hello, World!'})

@app.route('/api/<string:str1>/<string:str2>')
def get_length(str1, str2):
    length1 = len(str1)
    length2 = len(str2)
    result = {
        'total_lenght' : length1 + length2,
    }

    return jsonify(result) , 203

app.app_context().push()

from auth_apis import *
# from auth_apis import Login, Logout

api.add_resource(Login, '/api/auth/login')
api.add_resource(Logout, '/api/auth/logout')


if __name__ == '__main__':
    app.run(debug=True)
