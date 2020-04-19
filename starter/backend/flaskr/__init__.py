import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

# Paginated Questions


def pagination(request, selection):
    page = request.args.get("page", 1)
    start = (int(page) - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    questions = [questions.format() for questions in selection]
    current_questions = questions[start:end]
    return current_questions

def create_app(test_config=None):
    # creating an instance of the app and configuring it
    app = Flask(__name__, instance_relative_config=False)
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    setup_db(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    # DONE: Use the after_request decorator to set Access-Control-Allow
    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control_Allow-Headers',
                             'Content-Type, Authorization')
        response.headers.add('Access-Control_Allow-Methods',
                             'GET, POST, PATCH, DELETE, OPTIONS')
        return response
   

    @app.route('/api/categories')
    def get_categories():
        try:
            every_category = Category.query.order_by(Category.id).all()
            total_categories = len(every_category)
            if total_categories == 0:
                abort(404)
            category = {}
            for c in every_category:
                category[c.id] = c.type
            response = {
                "success": True,
                "categories": category,
                "total_categories": total_categories
            }
            return jsonify(response)
        except():
            abort(404)

    # COMPLETED:
    # Create an endpoint to handle GET requests for questions,
    # including pagination (every 10 questions).
    # This endpoint should return a list of questions,
    # number of total questions, current category, categories.

    # TEST: At this point, when you start the application
    # you should see questions and categories generated,
    # ten questions per page and pagination at the bottom of the screen for three pages.
    # Clicking on the page numbers should update the questions.
    # '''

    @app.route('/api/questions', methods=['GET'])
    def get_questions():
        page = 0
        if request.args.get("page"):
            page = int(request.args.get("page"))
        else:
            page = 1

        try:
            selection = Question.query.order_by(Question.id).all()
            current_questions = pagination(request, selection)
            total_questions = len(selection)

            if len(current_questions) == 0:
                abort(404)

            # Aggregate categories
            all_categories = Category.query.order_by(Category.id).all()
            # Turn them into tuples for frontend
            category = {}
            for c in all_categories:
                category[c.id] = c.type
            # Get formatted categories
            formatted_cats = [categories.format()
                              for categories in all_categories]

            def next_page(page):
                if len(current_questions) < QUESTIONS_PER_PAGE:
                    return
                else:
                    return "http://127.0.0.1:5000/api/questions?page=" + str(int(page)+1)+""

            def previous_page(page):
                if page == 1:
                    return
                else:
                    return "http://127.0.0.1:5000/api/questions?page=" + str(int(page)-1)+""
            # There's never a current category set here
            current_category = formatted_cats[0]
            response = {
                "success": True,
                "questions": current_questions,
                "total_questions": total_questions,
                "categories": category,
                "current_category": current_category,
                "next_page": next_page(page),
                "previous": previous_page(page)
            }
            return jsonify(response)
        # if exception, there are no questions
        except():
            abort(404)

    # '''
    # COMPLETED:
    # Create an endpoint to DELETE question using a question ID.

    # TEST: When you click the trash icon next to a question, the question will be removed.
    # This removal will persist in the database and when you refresh the page.
    # '''
    @app.route('/api/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        category = request.args.get('category', 1, type=int)
        try:
            question = Question.query.filter(
                Question.id == question_id).one_or_none()
            if question is None:
                abort(422)
            # Delete this question
            question.delete()
            response = {
                "success": True,
                "message": "Deleted"
            }
            return jsonify(response)
        except():
            abort(400)
    # '''
    # COMPLETED:
    # Create an endpoint to POST a new question,
    # which will require the question and answer text,
    # category, and difficulty score.

    # TEST: When you submit a question on the "Add" tab,
    # the form will clear and the question will appear at the end of the last page
    # of the questions list in the "List" tab.
    # '''
    @app.route('/api/questions', methods=['POST', 'PUT'])
    def create_question():
        body = request.get_json()

        new_question = body.get('question', None)
        new_difficulty = body.get('difficulty', None)
        new_category = body.get('category', None)
        new_answer = body.get('answer', None)

        if new_question is None:
            abort(422)

        try:
            question = Question(
                question=new_question,
                answer=new_answer,
                difficulty=new_difficulty,
                category=new_category
            )
            question.insert()
            response = {
                "success": True,
                "created": question.id,
                "message": "Question created"
            }

            return jsonify(response)
        except():
            abort(422)
    # '''
    # @TODO:
    # Create a POST endpoint to get questions based on a search term.
    # It should return any questions for whom the search term
    # is a substring of the question.

    # TEST: Search by any phrase. The questions list will update to include
    # only question that include that string within their question.
    # Try using the word "title" to start.
    # '''

    @app.route('/api/questions/search', methods=['POST'])
    def search_questions():
        body = request.get_json()
        print(body.get("search_term"))
        search_query = Question.query.filter(
            Question.question.ilike('%' + body.get("search_term") + '%'))
        print(search_query)
        results = list(map(Question.format, search_query))

        search_term = body.get("search_term", None)
        if search_term is None:
            abort(422)

        response = {
            "questions": results,
            "total_questions": len(results),
            "success": True
        }

        return jsonify(response)

    # DONE: Create a GET endpoint to get questions based on category.
    #
    # TEST: In the "List" tab / main screen, clicking on one of the
    # categories in the left column will cause only questions of that
    # category to be shown.
    @app.route('/api/categories/<int:category_id>/questions', methods=['GET'])
    def category_questions(category_id):
        try:
            selection = Question.query.filter(
                Question.category == category_id).all()
            current_questions = pagination(request, selection)
            total_questions = len(selection)
            if len(current_questions) == 0:
                abort(404)
            current_category = Category.query.filter(
                Category.id == category_id).one_or_none().format()
            response = {
                "success": True,
                "questions": current_questions,
                "total_questions": total_questions,
                "current_category": current_category
            }
            return jsonify(response)

        except():
            abort(404)

    # DONE: Create a POST endpoint to get questions to play the quiz.
    # This endpoint should take category and previous question parameters
    # and return a random questions within the given category,
    # if provided, and that is not one of the previous questions.
    #
    # TEST: In the "Play" tab, after a user selects "All" or a category,
    # one question at a time is displayed, the user is allowed to answer
    # and shown whether they were correct or not.
    @app.route('/api/quizzes', methods=['GET', 'POST'])
    def play_quizzes():
        body = request.get_json()
        print(body)
        category = body.get("quiz_category").get('id')
        previous_questions = body.get("previous_questions", [])
        print("Previous Questions: ", previous_questions)
        try:
            # gather all questions and their ids
            if category == 0:
                questions = Question.query.filter(
                    Question.question != '').order_by(Question.id).all()
            else:
                questions = Question.query.filter(
                    Question.category == category and Question.question != '').order_by(Question.id).all()

            if len(questions) == 0:
                abort(404)
            categoryname = Category.query.filter(Category.id == category).all()
            categoryname = [categoryname.format() for categoryname in categoryname]
            def showCategory():
                if category == 0:
                    return "All Categories"
                else:
                    return categoryname[0].get('type')
            questions = [questions.format() for questions in questions]
            total_questions = len(questions)
            # Need to gather all questions in a selection and for each one,
            # skip the previous ones by previous_question ids
            i = 0
            if len(previous_questions):
                for question in questions:
                    question_id = question["id"]
                    for previous_id in previous_questions:
                        if question_id == previous_id:
                            del questions[i]
                    i = i + 1

            # Note the number of questions left
            number_of_asked_questions = len(previous_questions)

            # Randomize the question that comes up everytime you play if
            # number of asked questions is equal to total questions minus
            # asked questions means no random choice
            random_max = (total_questions - number_of_asked_questions) - 1

            # else randomize the question. keep it within the range of index.
            if random_max > 0:
                random_choice = random.randint(0, random_max)
            else:
                random_choice = 0

            # Need to check if there are any questions left
            # return False if no questions left to ask.
            if number_of_asked_questions:
                if number_of_asked_questions == total_questions:
                    current_question = False
                else:
                    current_question = questions[random_choice]
            else:
                current_question = questions[random_choice]

            response = {
                "success": True,
                "previousQuestions": previous_questions,
                "question": current_question,
                "questions": questions,
                "total_questions": total_questions,
                "current_category": showCategory()
            }
            print("Response: ", response)
            return jsonify(response)

        except():
            abort(503)

    # DONE: Create error handlers for all expected errors
    # including 404 and 422.
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not found"
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Method NOT allowed"
        }), 405

    @app.errorhandler(422)
    def unprocessable_entity(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable Entity"
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal Server Error"
        }), 500

    return app