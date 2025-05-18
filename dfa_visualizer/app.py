"""
Flask application for DFA 101 Substring Visualizer.
"""

from flask import Flask, render_template, request, jsonify
from dfa_visualizer.dfa import DFA101

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__, static_folder='static', template_folder='templates')
    
    # Enable better error handling in production
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
    app.config['JSON_SORT_KEYS'] = False
    
    @app.route('/')
    def index():
        """Render the main visualization interface."""
        return render_template('index.html')
    
    @app.route('/api/check', methods=['POST'])
    def check_string():
        """
        API endpoint to check if a string contains '101'.
        
        Expects JSON payload: {'input_string': 'binary_string'}
        Returns JSON response with DFA processing results.
        """
        try:
            data = request.get_json()
            if not data or 'input_string' not in data:
                return jsonify({
                    'error': 'Invalid request format',
                    'message': 'Please provide input_string in JSON payload'
                }), 400
                
            input_string = str(data.get('input_string', ''))
            dfa = DFA101()
            result = dfa.process_input(input_string)
            
            return jsonify(result)
            
        except Exception as e:
            return jsonify({
                'error': 'Server error',
                'message': str(e)
            }), 500
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)