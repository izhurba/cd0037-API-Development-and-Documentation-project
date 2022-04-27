import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from werkzeug.exceptions import HTTPException

from itsdangerous import json

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

# Used to display questions at a maximum of 10 per page


def paginate_questions(request, selection):
    try:
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        questions = [question.format() for question in selection]
        current_questions = questions[start:end]
        return current_questions
    except HTTPException as e:
        print(e)
        abort(400)

# Method for creating the category dict used by multiple methods


def get_categoryList():
    categories = {}
    categoryList = Category.query.order_by(Category.id).all()

    for category in categoryList:
        categories[category.id] = category.type

    return categories

# App creation and configuration


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)

    CORS(app)
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    # Endpoint to handle GET requests

    @app.route('/categories')
    def get_category():
        try:
            categories = get_categoryList()
            return jsonify({
                'success': True,
                'categories': categories
            }), 200
        except HTTPException as e:
            print(e)
            abort(422)

    # Endpoint to handle GET requests for questions

    @app.route('/questions')
    def get_questions():
        questionsList = Question.query.order_by(Question.id).all()
        totalQuestions = len(questionsList)
        currentQuestions = paginate_questions(request, questionsList)

        if len(currentQuestions) == 0:
            abort(404)

        categories = get_categoryList()

        return jsonify({
            'success': True,
            'total_questions': totalQuestions,
            'categories': categories,
            'questions': currentQuestions
        }), 200

    # Endpoint to DELETE a question using a question ID

    @app.route('/questions/<int:id>', methods=['DELETE'])
    def delete_question(id):
        question = Question.query.get(id)
        try:
            question.delete()
            return jsonify({
                'success': True,
                'deleted': id,
                'message': "Question Deleted"
            }), 200
        except Exception as e:
            return jsonify({
                'success': False,
                'deleted': id,
                'message': 'Failed to Delete Question with ID' + str(id)
            }), 404

    # POST a new question or to get questions based on a search term.

    @app.route('/questions', methods=["POST"])
    def create_question():
        searchTerm = request.get_json().get('searchTerm')
        if searchTerm:
            try:
                results = Question.query.filter(
                    Question.question.ilike(f'%{searchTerm}%')).all()
                if len(results) == 0:
                    abort(404)
                pagedQ = paginate_questions(request, results)
                return jsonify({
                    'success': True,
                    'questions': pagedQ
                }), 200
            except HTTPException as e:
                abort(404)
        else:
            try:
                newQuestion = request.get_json().get('question'),
                newAnswer = request.get_json().get('answer'),
                newCategory = request.get_json().get('category'),
                newDifficulty = request.get_json().get('difficulty')

                if ((newQuestion == '') or (newAnswer == '') or (newCategory == '') or (newDifficulty == '')):
                        abort(400) 

                new_question = Question(
                    question = newQuestion,
                    answer = newAnswer,
                    category = newCategory,
                    difficulty= newDifficulty
                )
                new_question.insert()
                selection = Question.query.order_by(Question.id).all()

                return jsonify({
                    'success': True,
                    'created': new_question.id,
                    'questions': paginate_questions(request, selection),
                    'total_questions': len(selection)
                }), 200
            except Exception as e:
                abort(400)

    # GET endpoint to get questions based on category.

    @app.route('/categories/<int:id>/questions')
    def get_questions_by_category(id):
        category = Category.query.filter_by(id=id).one_or_none()
        if category:
            questions = Question.query.filter_by(category=id).all()
            pagedQ = paginate_questions(request, questions)

            return jsonify({
                'success': True,
                'questions': pagedQ,
                'total_questions': len(questions),
                'current_category': category.type
            }), 200
        else:
            abort(404)

    # POST endpoint to get questions to play the quiz.

    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        quizCategory = request.get_json().get('quiz_category')
        prevQuestion = request.get_json().get('previous_questions')
        possQList = []

        try:
            if (quizCategory == 0):
                questions = Question.query.all()
            else:
                questions = Question.query.filter_by(
                    category=quizCategory['id']).all()

            for qs in questions:
                if qs.id not in prevQuestion:
                    possQList.append(qs)

            if len(possQList) == 0:
                return jsonify({
                    'success': True,
                }), 200

            nextQuestion = possQList[random.randint(0, len(possQList)-1)]
            
            return jsonify({
                'success': True,
                'question': nextQuestion.format()
            }), 200
        except Exception as e:
            abort(400)

    # Error handlers for all expected errors

    @app.errorhandler(400)
    def bad_request_error(error):
        return jsonify({
            "success": False,
            'error': 400,
            "message": "Bad Request"
        }), 400

    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({
            "success": False,
            'error': 404,
            "message": "Not Found"
        }), 404

    @app.errorhandler(405)
    def method_not_allowed_error(error):
        return jsonify({
            "success": False,
            'error': 405,
            "message": "Method Not Allowed"
        }), 405

    @app.errorhandler(422)
    def unprocessable_entity_error(error):
        return jsonify({
            "success": False,
            'error': 422,
            "message": "Unprocessable Entity"
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            'error': 500,
            "message": "Internal Server Error"
        }), 500

    return app
