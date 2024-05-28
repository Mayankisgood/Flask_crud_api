import unittest
import json
from app import app, db, Todo

class TodoTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_database.db'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_todos(self):
        response = self.app.get('/todos')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'todos': []})

    def test_create_todo(self):
        response = self.app.post('/todos', data=json.dumps({'content': 'Test todo', 'completed': False}),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('Todo created successfully', response.json['message'])
        self.assertIn('todo_id', response.json)
        return response.json['todo_id']

    def test_update_todo(self):
        todo_id = self.test_create_todo()

        response = self.app.put(f'/todos/{todo_id}', data=json.dumps({'content': 'Updated content', 'completed': True}),
                                content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Todo updated successfully', response.json['message'])

        # Verify the update
        get_response = self.app.get('/todos')
        self.assertEqual(get_response.status_code, 200)
        todos = get_response.json['todos']
        self.assertEqual(len(todos), 1)
        self.assertEqual(todos[0]['id'], todo_id)
        self.assertEqual(todos[0]['content'], 'Updated content')
        self.assertTrue(todos[0]['completed'])

    def test_delete_todo(self):
        # First, create a todo
        todo_id = self.test_create_todo()

        # Then, delete the created todo
        response = self.app.delete(f'/todos/{todo_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Todo deleted successfully', response.json['message'])

        # Verify the deletion
        get_response = self.app.get('/todos')
        self.assertEqual(get_response.status_code, 200)
        todos = get_response.json['todos']
        self.assertEqual(len(todos), 0)

if __name__ == '__main__':
    unittest.main()

