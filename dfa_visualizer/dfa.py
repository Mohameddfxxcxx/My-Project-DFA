"""
Deterministic Finite Automaton (DFA) implementation for recognizing strings
containing the substring '101' with detailed state transition tracking.
"""

class DFA101:
    """DFA that recognizes strings containing the substring '101'."""
    
    def __init__(self):
        """
        Initialize the DFA with states, alphabet, transitions, and accepting states.
        
        States:
        - q0: Initial state (no progress towards '101')
        - q1: Saw '1' (first character of '101')
        - q2: Saw '10' (first two characters of '101')
        - q3: Saw '101' (accepting state)
        """
        self.states = {'q0', 'q1', 'q2', 'q3'}
        self.alphabet = {'0', '1'}
        self.start_state = 'q0'
        self.accept_states = {'q3'}
        
        # Transition function with descriptive messages
        self.transitions = {
            'q0': {
                '0': ('q0', "Remained in q0 - no progress towards '101'"),
                '1': ('q1', "Moved to q1 - saw first '1' of '101'")
            },
            'q1': {
                '0': ('q2', "Moved to q2 - saw '10' (first two characters)"),
                '1': ('q1', "Stayed in q1 - already saw '1', waiting for '0'")
            },
            'q2': {
                '0': ('q0', "Reset to q0 - pattern broken (needed '1' after '10')"),
                '1': ('q3', "Moved to q3 - found complete '101' substring!")
            },
            'q3': {
                '0': ('q3', "Stayed in accepting state q3"),
                '1': ('q3', "Stayed in accepting state q3")
            }
        }
    
    def process_input(self, input_string):
        """
        Process the input string through the DFA and return detailed path information.
        
        Args:
            input_string (str): The binary string to process
            
        Returns:
            dict: {
                'accepts': bool,
                'path': list of state transitions,
                'message': str
            }
        """
        current_state = self.start_state
        path = [{
            'state': current_state,
            'input': '',
            'message': f"Started in initial state {current_state}"
        }]
        
        for i, char in enumerate(input_string):
            if char not in self.alphabet:
                return {
                    'accepts': False,
                    'path': path,
                    'message': f"Invalid character '{char}' in input - only '0' and '1' allowed"
                }
            
            next_state, message = self.transitions[current_state][char]
            path.append({
                'state': next_state,
                'input': char,
                'message': f"Step {i+1}: Read '{char}' - {message}"
            })
            current_state = next_state
        
        return {
            'accepts': current_state in self.accept_states,
            'path': path,
            'message': "Accepted! The string contains '101'." 
                      if current_state in self.accept_states 
                      else "Rejected: The string does not contain '101'."
        }