from flask_restful import Resource
from application.models import *
from flask import make_response, jsonify, request
from flask_security import auth_required, roles_required



#<<<<<<<<<<<<<<SUBJECT/CHAPTERS>>>>>>>>>>>>>>>

class SubjectApi(Resource):
    @auth_required('token')
    @roles_required('admin')
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
    
    @auth_required('token')
    @roles_required('admin')
    def put(self, subject_id):
        subject_data = request.get_json()
        if not subject_data or 'name' not in subject_data:
            return {'message': 'Subject name is required'}, 400
        
        subject = Subject.query.get(subject_id)
        if not subject:
            return {'message': 'Subject not found'}, 404
        
        subject.name = subject_data['name']
        subject.description = subject_data.get('description', subject.description)
        db.session.commit()

        result = {
            'message': 'Subject updated successfully',
            'subject': {
                'id': subject.id,
                'name': subject.name,
                'description': subject.description
            }
        }
        return make_response(jsonify(result), 200)
    
    @auth_required('token')
    @roles_required('admin')
    def delete(self, subject_id):
        subject = Subject.query.get(subject_id)
        if not subject:
            return {'message': 'Subject not found'}, 404
        db.session.delete(subject)
        db.session.commit()

        return make_response(jsonify({'message': 'Subject deleted!'}, 200))
    
class SubjectListApi(Resource):
    @auth_required('token')
    @roles_required('admin')
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
    
    @auth_required('token')
    @roles_required('admin')
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
    



    
class ChapterApi(Resource):
    @auth_required('token')
    @roles_required('admin')
    def get(self, chapter_id):
        chapter = Chapter.query.get(chapter_id)
        if not chapter:
            return {'message': 'Chapter not found'}, 404
        
        result = {
            'message': 'Chapter retrieved!',
            'chapter':{
                'id': chapter.id,
                'name': chapter.name,
                'description': chapter.description
            }
        }

        return make_response(jsonify(result), 200)
    
    @auth_required('token')
    @roles_required('admin')
    def put(self, chapter_id):
        chapter_data = request.get_json()
        if not chapter_data or 'name' not in chapter_data:
            return {'message': 'Subject name is required'}, 400
        
        chapter = Chapter.query.get(chapter_id)
        if not chapter:
            return {'message': 'Chapter not found'}, 404
        
        chapter.name = chapter_data['name']
        chapter.description = chapter_data.get('description', chapter.description)
        db.session.commit()

        result = {
            'message': 'Chapter updated successfully',
            'chapter': {
                'id': chapter.id,
                'name': chapter.name,
                'description': chapter.description
            }
        }
        return make_response(jsonify(result), 200)
    
    @auth_required('token')
    @roles_required('admin')
    def delete(self, chapter_id):
        chapter = Chapter.query.get(chapter_id)
        if not chapter:
            return {'message': 'Chapter not found'}, 404
        db.session.delete(chapter)
        db.session.commit()

        return make_response(jsonify({'message': 'Chapter deleted!'}, 200))
    
class ChapterListApi(Resource):
    @auth_required('token')
    @roles_required('admin')
    def get(self, subject_id):
        chapters = Chapter.query.filter_by(subject_id=subject_id).all()
        if not chapters:
            return {'message': 'Chapters not found'}, 404
        
        result = [{
                'id': chapter.id,
                'name': chapter.name,
                'description': chapter.description
            } for chapter in chapters]
        return make_response(jsonify({'message': 'Chapters retrieved!', 'chapters': result}), 200)
    
    @auth_required('token')
    @roles_required('admin')
    def post(self, subject_id):
        chapter_data = request.get_json()
        if not chapter_data or 'name' not in chapter_data:
            return {'message': 'Chapter name is required'}, 400
        
        new_chapter = Chapter(
            name = chapter_data['name'],
            description = chapter_data.get('description', ''),
            subject_id = subject_id
        )

        existing_chapter = Chapter.query.filter_by(name=new_chapter.name).first()
        if existing_chapter:
            return {'message': 'Chapter name already exists'},400
        
        db.session.add(new_chapter)
        db.session.commit()

        result = {
            'message': 'Chapter added successfully',
            'chapter': {
                'id': new_chapter.id,
                'name': new_chapter.name,
                'description': new_chapter.description
            }
        }

        return make_response(jsonify(result), 201)




#<<<<<<<<<<<<<<QUIZ/QUESTIONS>>>>>>>>>>>>>>>


class QuizApi(Resource):
    @auth_required('token')
    @roles_required('admin')
    def get(self, quiz_id):
        quiz = Quiz.query.get(quiz_id)
        if not quiz:
            return {'message': 'Quiz not found'}, 404
        
        result = {
            'message': 'Quiz retrieved!',
            'quiz':{
                'id': quiz.id,
                'date': quiz.date,
                'duration': quiz.duration
            }
        }

        return make_response(jsonify(result), 200)
    
    @auth_required('token')
    @roles_required('admin')
    def put(self, quiz_id):
        quiz_data = request.get_json()
        if not quiz_data or 'date' not in quiz_data or 'duration' not in quiz_data:
            return {'message': 'Quiz name is required'}, 400
        
        quiz = Quiz.query.get(quiz_id)
        if not quiz:
            return {'message': 'Quiz not found'}, 404
        
        quiz.date = quiz_data['date']
        quiz.duration = quiz_data.get('duration', quiz.duration)
        db.session.commit()

        result = {
            'message': 'Quiz updated successfully',
            'quiz': {
                'id': quiz.id,
                'date': quiz.date,
                'duration': quiz.duration
            }
        }
        return make_response(jsonify(result), 200)
    
    @auth_required('token')
    @roles_required('admin')
    def delete(self, quiz_id):
        quiz = Quiz.query.get(quiz_id)
        if not quiz:
            return {'message': 'Quiz not found'}, 404
        db.session.delete(quiz)
        db.session.commit()

        return make_response(jsonify({'message': 'Quiz deleted!'}, 200))
    
class QuizListApi(Resource):
    @auth_required('token')
    @roles_required('admin')
    def get(self):
        quizes = Quiz.query.all()
        if not quizes:
            return {'message': 'Quizes not found'}, 404
        
        result = [{
                'id': quiz.id,
                'date': quiz.date,
                'duration': quiz.duration
            } for quiz in quizes]
        return make_response(jsonify({'message': 'Quizes retrieved!', 'quizes': result}), 200)
    
    
class QuizCreateApi(Resource):
    @auth_required('token')
    @roles_required('admin')  
    def post(self, chapter_id):
        quiz_data = request.get_json()
        if not quiz_data or 'date' not in quiz_data or 'duration' not in quiz_data:
            return {'message': 'Quiz date & duration is required'}, 400
        
        new_quiz = Quiz(
            date = quiz_data['date'],
            duration = quiz_data.get('duration', ''),
            chapter_id=chapter_id
        )

        existing_quiz = Quiz.query.filter_by(date=new_quiz.chapter_id).first()
        if existing_quiz:
            return {'message': 'Quiz already exists'},400
        
        db.session.add(new_quiz)
        db.session.commit()

        result = {
            'message': 'Quiz added successfully',
            'quiz': {
                'id': new_quiz.id,
                'name': new_quiz.date,
                'description': new_quiz.duration
            }
        }

        return make_response(jsonify(result), 201)


    
class QuestionsApi(Resource):
    @auth_required('token')
    @roles_required('admin')
    def get(self, questions_id):
        questions = Questions.query.get(questions_id)
        if not questions:
            return {'message': 'Questions not found'}, 404
        
        result = {
            'message': 'Questions retrieved!',
            'questions':{
                'id': questions.id,
                'name': questions.name,
                'question_statement': questions.question_statement,
                'option' : questions.option
            }
        }

        return make_response(jsonify(result), 200)
    
    @auth_required('token')
    @roles_required('admin')
    def put(self, questions_id):
        question_data = request.get_json()
        if not question_data or 'name' not in question_data or 'question_statement' not in question_data or 'option' not in question_data:
            return {'message': 'Question name is required'}, 400
        
        questions = Questions.query.get(questions_id)
        if not questions:
            return {'message': 'question not found'}, 404
        
        questions.name = question_data['name']
        questions.question_statement = question_data.get('question_statement', questions.question_statement)
        questions.option = question_data['option']
        db.session.commit()

        result = {
            'message': 'Ques updated successfully',
            'question': {
                'id': questions.id,
                'name': questions.name,
                'question_statement': questions.question_statement,
                'option' : questions.option
            }
        }
        return make_response(jsonify(result), 200)
    
    @auth_required('token')
    @roles_required('admin')
    def delete(self, questions_id):
        questions = Questions.query.get(questions_id)
        if not questions:
            return {'message': 'Question not found'}, 404
        db.session.delete(questions)
        db.session.commit()

        return make_response(jsonify({'message': 'Question deleted!'}, 200))
    
class QuestionsListApi(Resource):
    @auth_required('token')
    @roles_required('admin')
    def get(self, quiz_id):
        questions = Questions.query.filter_by(quiz_id=quiz_id).all()
        if not questions:
            return {'message': 'Questions not found'}, 404
        
        result = [{
                'id': question.id,
                'name': question.name,
                'question_statement': question.question_statement,
                'option' : question.option

            } for question in questions]
        return make_response(jsonify({'message': 'Questions retrieved!', 'questions': result}), 200)
    
    @auth_required('token')
    @roles_required('admin')
    def post(self, quiz_id):
        question_data = request.get_json()
        if not question_data or 'name' not in question_data or 'question_statement' not in question_data or 'option' not in question_data:
            return {'message': 'question details is required'}, 400
        
        new_question = Questions(
            name = question_data['name'],
            question_statement = question_data.get('question_statement', ''),
            option = question_data.get('option'),
            quiz_id = quiz_id
        )

        existing_question = Questions.query.filter_by(name=new_question.name).first()
        if existing_question:
            return {'message': 'Question name already exists'},400
        
        db.session.add(new_question)
        db.session.commit()

        result = {
            'message': 'Question added successfully',
            'question': {
                'id': new_question.id,
                'name': new_question.name,
                'question_statement': new_question.question_statement,
                'option': new_question.option
            }
        }

        return make_response(jsonify(result), 201)