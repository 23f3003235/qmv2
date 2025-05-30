from application.database import db
from flask_security import UserMixin, RoleMixin

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean(), default=True)
    
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

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    chapter = db.relationship(
        'Chapter',
        backref='subject',
        cascade='all, delete-orphan',
        passive_deletes=True
    )
    

class Chapter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    subject_id = db.Column(
        db.Integer,
        db.ForeignKey('subject.id', ondelete='CASCADE'),
        nullable=False
    )
    quiz = db.relationship(
        'Quiz',
        backref='chapter',
        cascade='all, delete-orphan',
        passive_deletes=True
    )

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'), nullable=False)
    date = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.String(50), nullable=False)
    chapter_id = db.Column(
        db.Integer,
        db.ForeignKey('chapter.id', ondelete='CASCADE'),
        nullable=False
    )
    questions = db.relationship(
        'Questions',
        backref='quiz',
        cascade='all, delete-orphan',
        passive_deletes=True
    )
    
class Questions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    question_statement = db.Column(db.Text, nullable=False)
    option = db.Column(db.String(100), nullable=False)
    quiz_id = db.Column(
        db.Integer,
        db.ForeignKey('quiz.id', ondelete='CASCADE'),
        nullable=False
    )

# class Scores(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
#     users_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     time_stamp_of_attempt = db.Column(db.String(50), nullable=False)
#     total_scored = db.Column(db.Integer,nullable=False)