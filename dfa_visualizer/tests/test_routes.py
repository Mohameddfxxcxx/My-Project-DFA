import unittest
from dfa_visualizer.app import create_app

class TestFlaskRoutes(unittest.TestCase):
    """Test cases for Flask routes."""
    
    def setUp(self):
        """Create test client for each test."""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
    def test_index_route(self):
        """Test the index route returns 200 OK."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'DFA 101 Substring Visualizer', response.data)
    
    def test_check_route_valid_input(self):
        """Test the check route with valid input."""
        test_cases = [
            ("101", True),
            ("0101", True),
            ("000", False),
            ("1101", True),
            ("111", False)
        ]
        
        for input_str, expected in test_cases:
            with self.subTest(input_str=input_str):
                response = self.client.post('/api/check', 
                                          json={'input_string': input_str})
                self.assertEqual(response.status_code, 200)
                data = response.get_json()
                self.assertEqual(data['accepts'], expected)
    
    def test_check_route_invalid_input(self):
        """Test the check route with invalid input."""
        response = self.client.post('/api/check', json={'input_string': '10a'})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertFalse(data['accepts'])
        self.assertIn("Invalid character", data['message'])
    
    def test_check_route_missing_input(self):
        """Test the check route with missing input."""
        response = self.client.post('/api/check', json={})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertFalse(data['accepts'])

if __name__ == '__main__':
    unittest.main()