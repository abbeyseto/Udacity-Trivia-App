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
    '''This api gets the list of categories of questions in the trivia app
    via a GET method and also shows the total count of the categories'''

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
                    print("YESSS")
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
    # @TODO:
    # Create an endpoint to DELETE question using a question ID.

    # TEST: When you click the trash icon next to a question, the question will be removed.
    # This removal will persist in the database and when you refresh the page.
    # '''

    # '''
    # @TODO:
    # Create an endpoint to POST a new question,
    # which will require the question and answer text,
    # category, and difficulty score.

    # TEST: When you submit a question on the "Add" tab,
    # the form will clear and the question will appear at the end of the last page
    # of the questions list in the "List" tab.
    # '''

    # '''
    # @TODO:
    # Create a POST endpoint to get questions based on a search term.
    # It should return any questions for whom the search term
    # is a substring of the question.

    # TEST: Search by any phrase. The questions list will update to include
    # only question that include that string within their question.
    # Try using the word "title" to start.
    # '''

    # '''
    # @TODO:
    # Create a GET endpoint to get questions based on category.

    # TEST: In the "List" tab / main screen, clicking on one of the
    # categories in the left column will cause only questions of that
    # category to be shown.
    # '''
    # '''
    # @TODO:
    # Create a POST endpoint to get questions to play the quiz.
    # This endpoint should take category and previous question parameters
    # and return a random questions within the given category,
    # if provided, and that is not one of the previous questions.

    # TEST: In the "Play" tab, after a user selects "All" or a category,
    # one question at a time is displayed, the user is allowed to answer
    # and shown whether they were correct or not.
    # '''

    # '''
    # @TODO:
    # Create error handlers for all expected errors
    # including 404 and 422.
    # '''

    return app
