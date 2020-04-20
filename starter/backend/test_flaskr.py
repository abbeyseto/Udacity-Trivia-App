import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from models import setup_db, Question, Category
from flaskr import create_app

class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        # db_config = self.app.config["DATABASE_SETUP"]
        self.app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://{}:{}@{}/{}"\
            .format("AshNelson",
                    "ologinahtti1",
                    "localhost:5432",
                    "trivia_test")
        setup_db(self.app)

        self.new_question = {
            "category"  : 6,
            "question"  : "Who is the greatest developer? Hint: the author "
                          "of this question",
            "answer"    : "Joao Albuquerque",
            "difficulty": 1
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    # Done: Write at least one test for each test for successful operation
    # and for expected errors. GET Categories
    def test_retrieve_categories(self):
        res = self.client().get('/api/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'], True)

    # GET Questions - Paginated
    def test_retrieve_questions_paginated(self):
        res = self.client().get('/api/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])

    # GET Questions - Paginated - Out of bounds
    def test_retrieve_questions_out_of_pagination(self):
        res = self.client().get('/api/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    # GET Questions by Category
    def test_retrieve_questions_by_category_paginated(self):
        res = self.client().get('/api/categories/6/questions')
        data = json.loads(res.data)

        total_questions = len(Question.query.filter(Question.category == 6)
                              .all())

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertEqual(data['total_questions'], total_questions)

    # GET Questions by Category - out of bounds
    def test_retrieve_questions_by_category_out_of_pagination(self):
        res = self.client().get('/api/categories/6/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    # POST Create a Questions
    def test_create_questions(self):
        res = self.client().post('/api/questions', json=self.new_question)
        data = json.loads(res.data)

        question = Question.query.order_by(Question.id).all()
        total_questions = len(question)
        print("Total questions: ", total_questions)
        added_question = question[total_questions-1]

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['created'], added_question.id)
        self.assertEqual(data['message'], "Question created")

        # Clean up
        added_question.delete()

    # POST Failed to Create a Questions
    def test_create_questions_not_enough_information(self):
        res = self.client().post('/api/questions', json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    # POST Failed to Create a Questions wrong Endpoint
    def test_create_questions_wrong_endpoint(self):
        res = self.client().post('/api/questions/12', json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    # DELETE a Question - no id specified
    def test_delete_question_by_id_no_id_specified(self):
        res = self.client().delete('/api/questions/')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    # DELETE a Question - invalid id specified
    def test_delete_question_by_id_no_question_found(self):
        res = self.client().delete('/api/questions/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    # DELETE a Question - successfully
    def test_delete_question_by_id(self):
        # add a question and use that id to delete
        added_question = Question(
            question="This is a question?",
            category=3,
            difficulty=3,
            answer="This is an answer"
        )
        added_question.insert()

        res = self.client().delete('/api/questions/{}'.
                                   format(added_question.id))
        data = json.loads(res.data)

        total_questions = len(Question.query.all())

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], "Deleted")

    # POST Search Questions - with results
    def test_search_questions_with_results(self):
        res = self.client().post('/api/questions/search',
                                 json={"search_term": "title"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertGreater(data['total_questions'], 0)

    # POST Search Questions - no results
    def test_search_questions_without_results(self):
        res = self.client().post('/api/questions/search',
                                 json={"search_term": "zebra"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertFalse(data['questions'])
        self.assertEqual(data['total_questions'], 0)

    # POST Search Questions - blank searchTerm
    def test_search_questions_blank_search_term(self):
        res = self.client().post('/api/questions/search',
                                 json={"search_term": ""})
        data = json.loads(res.data)

        total_questions = len(Question.query.all())

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertEqual(data['total_questions'], total_questions)

    # POST Search Questions - no searchTerm
    def test_search_questions_no_search_term(self):
        res = self.client().post('/api/questions/search', json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 500)
        self.assertEqual(data['success'], False)

    # POST Play Quiz - One category
    def test_play_quizz_one_category_empty_previous_questions(self):
        res = self.client().post('/api/quizzes',
                                 json={"quiz_category": {"id" : 6,
                                                         "type" : "Sports"},
                                       "previous_questions" : []})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['question'])
        self.assertTrue(data['total_questions'])

    # POST Play Quiz - Category out of bounds
    def test_play_quizz_one_category_fake_category_id(self):
        res = self.client().post('/api/quizzes',
                                 json={"quiz_category": {"id": 99,
                                                         "type": "Fake"},
                                       "previous_questions" : []})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    # POST Play Quiz - with previous questions
    def test_play_quizz_one_category_with_previous_questions(self):
        res = self.client().post('/api/quizzes',
                                 json={"quiz_category": {"id": 6,
                                                         "type": "Sports"},
                                       "previous_questions": [62]})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['question'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['previousQuestions'])

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()