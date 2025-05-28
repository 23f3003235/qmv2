from flask import Flask, jsonify, request, make_response
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin

app = Flask(__name__)
api = Api(app)

db = SQLAlchemy()
db.init_app(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECURITY_PASSWORD_SALT'] = 'my_precious_two'
app.config['SECRET_KEY'] = 'my_precious'

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    
database = []

if __name__ == '__main__':
    app.run(debug=True)
