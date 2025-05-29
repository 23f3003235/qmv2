from flask import Flask, jsonify, request, make_response
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin

from application.models import *
from application.user_datastore import user_datastore
from application.database import db
from application.crud_apis import *


app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///raj.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECURITY_PASSWORD_SALT'] = 'my_mad2app'
app.config['SECRET_KEY'] = 'my_mad2'

db.init_app(app)
security = Security(app, user_datastore)

with app.app_context():
    db.create_all()

    admin_role = user_datastore.find_or_create_role(name='admin', description='Administrator role')
    user_role = user_datastore.find_or_create_role(name='user', description='User role')

    if not user_datastore.find_user(email="admin@gmail.com"):
        user_datastore.create_user(
            email = "admin@gmail.com",
            password = "admin123",
            roles = [user_role, admin_role],
        )
    db.session.commit()
app.app_context().push()

from auth_apis import *

api.add_resource(Login, '/api/auth/login')
api.add_resource(Logout, '/api/auth/logout')

api.add_resource(SubjectListApi, '/api/subject')
api.add_resource(SubjectApi,'/api/subject/<int:subject_id>')

if __name__ == '__main__':
    app.run(debug=True)