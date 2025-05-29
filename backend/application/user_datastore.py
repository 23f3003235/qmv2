from flask_security import SQLAlchemyUserDatastore
from application.database import db
from application.models import Users, Roles

user_datastore = SQLAlchemyUserDatastore(db, Users, Roles)