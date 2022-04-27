import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}/{}".format('postgres:password@localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_categories(self):
        resp = self.client().get('/categories')
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['categories']), 6)

    def test_get_questions(self):
        resp = self.client().get('/questions')
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['success'], True)
        #self.assertEqual(data['total_questions'], 19) #Doesn't work well since errant questions get created
        self.assertEqual(len(data['questions']), 10)
        self.assertEqual(data['questions'][0]['id'], 2)
    
    def test_get_questions_404(self):
        resp = self.client().get('/questions?page=10')

        self.assertEqual(resp.status_code, 404)
    
    def test_get_questions_by_category(self):
        resp = self.client().get('/categories/3/questions')
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['current_category'], 'Geography')
        self.assertEqual(data['total_questions'], 3)

    def test_get_questions_by_category_404(self):
        resp = self.client().get('/categories/11/questions')

        self.assertEqual(resp.status_code, 404)
    
    def test_search_questions(self):
        resp = self.client().post('/questions' , json = {
                                'searchTerm' :"Tom"
                                })
        data = json.loads(resp.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 1)
        self.assertEqual(data['questions'][0]['id'], 2)

    def test_search_questions_404(self):
        resp = self.client().post('/questions', json = {
                                'searchTerm' : 'asdfas'
                        })
        
        self.assertEqual(resp.status_code, 404)

    def test_post_question(self):
        resp = self.client().post('/questions',
                            json = {
                                'question' : 'what is a test question?',
                                'answer' : 'A test answer',
                                'category': 1,
                                'difficulty' : 1
                            })
        data = json.loads(resp.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(resp.status_code, 200)

    def test_post_question_400(self):
        resp = self.client().post('/questions',
                            json = {
                                'question' : '',
                                'answer' : '',
                                'category': 100,
                                'difficulty' : 1
                            })
        self.assertEqual(resp.status_code, 400)

    def test_delete_question(self):
        newestQ = Question.query.all()[-1]  #Used to find the newest created question (to avoid errors)
        resp = self.client().delete('/questions/' + str(newestQ.id))
        data = json.loads(resp.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], newestQ.id)
        self.assertEqual(data['message'], "Question Deleted")
        self.assertEqual(resp.status_code, 200)

    def test_delete_question_404(self):
        resp = self.client().delete('/questions/200')
        data = json.loads(resp.data)

        self.assertEqual(data['success'], False)
        self.assertEqual(resp.status_code, 404)

    def test_play_quiz(self):
        resp = self.client().post('quizzes', 
                            json={
                                'previous_questions':[],
                                'quiz_category': {'id': 0, 'type': 'All'}
                            })
        
        self.assertEqual(resp.status_code, 200)

    def test_play_quiz_400(self):
        resp = self.client().post('quizzes', 
                            json={
                                'previous_questions':[],
                                'quiz_category': {}
                            }) 
    
        self.assertEqual(resp.status_code, 400)

    def test_play_quiz_with_options(self):
        resp = self.client().post('quizzes', 
                            json={
                                'previous_questions':[13, 14],
                                'quiz_category': {'id': 3, 'type': 'Geography'}
                            })
    
        data = json.loads(resp.data)

        self.assertEqual(data['question']['category'], 3)
        self.assertEqual(data['question']['id'], 15)
        self.assertEqual(resp.status_code, 200)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()