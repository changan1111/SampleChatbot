import os
import subprocess
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Get the absolute path of the directory containing the app.py file
current_directory = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    user_input = request.form['user_input']
    
    if user_input == "Run Test Suite":
        options = ["Functional Testing", "Regression Testing", "Security Testing"]
        button_html = ""
        for option in options:
            button_html += f'<button type="button" class="option-button" data-option="{option}" onclick="sendOption(\'{option}\')">{option}</button>'
        bot_response = f"Please select an option:<br/>{button_html}"
    else:
        bot_response = "Invalid command. Please try again."
    
    return jsonify({'bot_response': bot_response})

@app.route('/send_option', methods=['POST'])
def send_option():
    selected_option = request.form['selected_option']
    
    if selected_option == "Regression Testing":
        try:
            # Run the Maven command and capture the output
            result = subprocess.run(['mvn', 'clean', 'test'], cwd=current_directory, shell=True, capture_output=True, text=True)
            output = result.stdout.strip()  # Get the output from the completed process
            
            # Check if the test execution was successful or not
            if result.returncode == 0:
                bot_response = f"Regression testing completed. Result: Passed<br/>{output}"
            else:
                bot_response = f"Regression testing completed. Result: Failed<br/>{output}"
        except FileNotFoundError:
            bot_response = "Maven or testng.xml file not found. Make sure you have the required files."
    else:
        bot_response = "Invalid command. Please try again."
    
    return jsonify({'bot_response': bot_response})

if __name__ == '__main__':
    app.run()
