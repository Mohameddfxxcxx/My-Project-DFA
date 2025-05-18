import unittest
from dfa_visualizer.dfa import DFA101

class TestDFA101(unittest.TestCase):
    """Test cases for the DFA101 class."""
    
    def setUp(self):
        """Initialize DFA for each test."""
        self.dfa = DFA101()
    
    def test_accepts_strings_with_101(self):
        """Test strings that contain '101' should be accepted."""
        test_cases = [
            "101",
            "0101",
            "1010",
            "1101",
            "101101",
            "111010",
            "000101000"
        ]
        
        for string in test_cases:
            with self.subTest(string=string):
                result = self.dfa.process_input(string)
                self.assertTrue(result['accepts'], 
                               f"Expected '{string}' to be accepted")
    
    def test_rejects_strings_without_101(self):
        """Test strings that don't contain '101' should be rejected."""
        test_cases = [
            "",
            "0",
            "1",
            "00",
            "11",
            "010",
            "100",
            "000",
            "111",
            "010010",
            "110011"
        ]
        
        for string in test_cases:
            with self.subTest(string=string):
                result = self.dfa.process_input(string)
                self.assertFalse(result['accepts'], 
                                f"Expected '{string}' to be rejected")
    
    def test_invalid_characters(self):
        """Test strings with invalid characters should be rejected."""
        test_cases = [
            "a",
            "101a",
            "1a1",
            "10a",
            "abc",
            "102",
            "10.1"
        ]
        
        for string in test_cases:
            with self.subTest(string=string):
                result = self.dfa.process_input(string)
                self.assertFalse(result['accepts'])
                self.assertIn("Invalid character", result['message'])
    
    def test_state_transitions(self):
        """Test correct state transitions for specific inputs."""
        # Test case 1: "101" - should reach q3
        result = self.dfa.process_input("101")
        self.assertEqual(result['path'][-1]['state'], 'q3')
        
        # Test case 2: "10" - should end in q2
        result = self.dfa.process_input("10")
        self.assertEqual(result['path'][-1]['state'], 'q2')
        
        # Test case 3: "100" - should reset to q0
        result = self.dfa.process_input("100")
        self.assertEqual(result['path'][-1]['state'], 'q0')
        
        # Test case 4: "1010" - should stay in q3
        result = self.dfa.process_input("1010")
        self.assertEqual(result['path'][-1]['state'], 'q3')

if __name__ == '__main__':
    unittest.main()