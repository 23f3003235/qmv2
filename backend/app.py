from flask import Flask, jsonify, request, make_response
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin

from application.models import *
from application.user_datastore import user_datastore
from application.database import db
from application.crud_apis import *
from application import worker

from sqlalchemy import event
from sqlalchemy.engine import Engine
import sqlite3

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///raj.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['CELERY_BROKER_URL'] = "redis://localhost:6379/0"
app.config['CELERY_RESULT_BACKEND'] = "redis://localhost:6379/0"

app.config['SECURITY_PASSWORD_SALT'] = 'my_mad2app'
app.config['SECRET_KEY'] = 'my_mad2'



@event.listens_for(Engine, "connect")
def enable_sqlite_foreign_keys(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, sqlite3.Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

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


# from celery_app import generate_csv
class ExportCSV(Resource):
    def get(self):
        from celery_app import generate_csv
        data = [{'name':'mahesh'},{'name':'suresh'}]
        generate_csv.delay(data, filename=f'static/raj.csv')
        return "CSV export initialised, you'll receive mail"
    
api.add_resource(ExportCSV, '/api/export_csv')

app.app_context().push()

from auth_apis import *

api.add_resource(Login, '/api/auth/login')
api.add_resource(Logout, '/api/auth/logout')

api.add_resource(SubjectListApi, '/api/subject')
api.add_resource(SubjectApi,'/api/subject/<int:subject_id>')

api.add_resource(ChapterListApi, '/api/chapter/<int:subject_id>')
api.add_resource(ChapterApi,'/api/chapter/<int:chapter_id>')

api.add_resource(QuizCreateApi, '/api/quiz/<int:chapter_id>')
api.add_resource(QuizListApi, '/api/quiz')
api.add_resource(QuizApi,'/api/quiz/<int:quiz_id>')

api.add_resource(QuestionsListApi, '/api/questions/<int:quiz_id>')
api.add_resource(QuestionsApi,'/api/questions/<int:questions_id>')

if __name__ == '__main__':
    app.run(debug=True)