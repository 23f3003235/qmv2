from flask_restful import Resource
from application.models import *
from flask import make_response, jsonify, request

class SubjectApi(Resource):
    def get(self, subject_id):
        subject = Subject.query.get(subject_id)
        if not subject:
            return {'message': 'Subject not found'}, 404
        
        result = {
            'message': 'Subject retrieved!',
            'subject':{
                'id': subject.id,
                'name': subject.name,
                'description': subject.description
            }
        }

        return make_response(jsonify(result), 200)
    
class SubjectListApi(Resource):
    def get(self):
        subjects = Subject.query.all()
        if not subjects:
            return {'message': 'Subjects not found'}, 404
        
        result = [{
                'id': subject.id,
                'name': subject.name,
                'description': subject.description
            } for subject in subjects]
        return make_response(jsonify({'message': 'Subjects retrieved!', 'subjects': result}), 200)
    
    def post(self):
        subject_data = request.get_json()
        if not subject_data or 'name' not in subject_data:
            return {'message': 'Subject name is required'}, 400
        
        new_subject = Subject(
            name = subject_data['name'],
            description = subject_data.get('description', '')
        )

        existing_subject = Subject.query.filter_by(name=new_subject.name).first()
        if existing_subject:
            return {'message': 'Subject name already exists'},400
        
        db.session.add(new_subject)
        db.session.commit()

        result = {
            'message': 'Subject added successfully',
            'subject': {
                'id': new_subject.id,
                'name': new_subject.name,
                'description': new_subject.description
            }
        }

        return make_response(jsonify(result), 201)