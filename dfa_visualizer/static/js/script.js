/**
 * Main application script for DFA 101 Visualizer
 */

document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const inputField = document.getElementById('binary-input');
    const checkButton = document.getElementById('check-btn');
    const errorMessage = document.getElementById('error-message');
    const exampleButtons = document.querySelectorAll('.example-btn');
    const states = document.querySelectorAll('.state');
    const resultMessage = document.getElementById('result-message');
    const pathDetails = document.getElementById('path-details');
    
    // Event Listeners
    checkButton.addEventListener('click', processInput);
    inputField.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') processInput();
    });
    
    // Example button handlers
    exampleButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            inputField.value = this.dataset.example;
            processInput();
        });
    });
    
    /**
     * Process the input string through the DFA
     */
    function processInput() {
        const input = inputField.value.trim();
        
        // Validate input
        if (!/^[01]*$/.test(input)) {
            showError('Please enter a valid binary string (only 0s and 1s allowed)');
            return;
        }
        
        if (input === '') {
            showError('Please enter a binary string to process');
            return;
        }
        
        // Clear previous state
        resetVisualization();
        hideError();
        
        // Show loading state
        checkButton.disabled = true;
        checkButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing';
        
        // Send request to server
        fetch('/api/check', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ input_string: input })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            displayResult(data);
            animateDFA(data.path);
        })
        .catch(error => {
            console.error('Error:', error);
            showError('An error occurred while processing your request');
        })
        .finally(() => {
            checkButton.disabled = false;
            checkButton.innerHTML = '<i class="fas fa-play"></i> Run DFA';
        });
    }
    
    /**
     * Display the final result and execution trace
     */
    function displayResult(data) {
        // Set result message
        resultMessage.textContent = data.message;
        resultMessage.className = `result-message ${data.accepts ? 'success' : 'error'}`;
        
        // Build step-by-step explanation
        pathDetails.innerHTML = '';
        data.path.forEach((step, index) => {
            const stepElement = createStepElement(step, index);
            pathDetails.appendChild(stepElement);
        });
    }
    
    /**
     * Create a DOM element for a single step in the execution trace
     */
    function createStepElement(step, index) {
        const stepDiv = document.createElement('div');
        stepDiv.className = 'step fade-in';
        
        const header = document.createElement('div');
        header.className = 'step-header';
        
        if (index === 0) {
            header.innerHTML = `<span class="step-state">Initial State: ${step.state}</span>`;
        } else {
            header.innerHTML = `
                <span class="step-state">State: ${step.state}</span>
                <span class="step-input">Input: '${step.input}'</span>
            `;
        }
        
        const message = document.createElement('div');
        message.className = 'step-message';
        message.textContent = step.message;
        
        stepDiv.appendChild(header);
        stepDiv.appendChild(message);
        
        return stepDiv;
    }
    
    /**
     * Animate the DFA state transitions
     */
    function animateDFA(path) {
        let delay = 0;
        const stepDuration = 1000;
        
        path.forEach((step, index) => {
            setTimeout(() => {
                // Highlight current state
                states.forEach(state => {
                    state.classList.remove('active', 'pulse');
                    if (state.id === step.state) {
                        state.classList.add('active', 'pulse');
                    }
                });
                
                // Highlight corresponding step in explanation
                const steps = document.querySelectorAll('.step');
                if (steps[index]) {
                    steps[index].scrollIntoView({ 
                        behavior: 'smooth', 
                        block: 'nearest' 
                    });
                    steps[index].classList.add('pulse');
                    setTimeout(() => {
                        steps[index].classList.remove('pulse');
                    }, 500);
                }
                
            }, delay);
            
            // Increase delay for next step
            delay += stepDuration;
        });
    }
    
    /**
     * Reset the visualization to initial state
     */
    function resetVisualization() {
        states.forEach(state => state.classList.remove('active'));
        resultMessage.textContent = '';
        resultMessage.className = 'result-message';
        pathDetails.innerHTML = '';
    }
    
    /**
     * Show error message
     */
    function showError(message) {
        errorMessage.textContent = message;
        errorMessage.style.display = 'block';
    }
    
    /**
     * Hide error message
     */
    function hideError() {
        errorMessage.style.display = 'none';
    }
});