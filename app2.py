import os
import subprocess
from flask import Flask, request, jsonify, render_template
import traceback

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
        try:
            # Get the current directory
            current_dir = os.getcwd()

            # Change the current working directory to the project directory
            project_directory = r"C:\Users\Chandrasekaran\eclipse-workspace\DreamHotelSuite"
            os.chdir(project_directory)

            # Print the current directory
            directory_message = f"Current directory: {os.getcwd()}<br/>"

            # Change the current directory back to the original directory
            os.chdir(current_directory)

            bot_response = f"{directory_message}Please select an option:<br/><button type='button' class='option-button' data-option='Functional Testing'>Functional Testing</button><button type='button' class='option-button' data-option='Regression Testing'>Regression Testing</button><button type='button' class='option-button' data-option='Security Testing'>Security Testing</button>"
        except Exception:
            traceback_message = traceback.format_exc()
            bot_response = f"Error occurred while changing the directory.<br/>Error:<br/>{traceback_message}"
    elif user_input == "Regression Testing":
        try:
            # Get the current directory
            current_dir = os.getcwd()

            # Change the current working directory to the project directory
            project_directory = r"C:\Users\Chandrasekaran\eclipse-workspace\DreamHotelSuite"
            os.chdir(project_directory)

            # Print the current directory
            directory_message = f"Current directory: {os.getcwd()}<br/>"

            # Run the mvn clean test command and capture the output
            completed_process = subprocess.run(['mvn', 'clean', 'test'], capture_output=True, text=True)

            # Get the output and error as strings
            output = completed_process.stdout
            error = completed_process.stderr

            # Change the current directory back to the original directory
            os.chdir(current_directory)

            # Include the output in the response
            bot_response = f"{directory_message}Regression testing started. Current directory: {current_dir}<br/>Output:<br/>{output}<br/>Error:<br/>{error}"
        except Exception:
            traceback_message = traceback.format_exc()
            bot_response = f"Error occurred while running the tests.<br/>Error:<br/>{traceback_message}"
    else:
        bot_response = "Invalid command. Please try again."

    return jsonify({'bot_response': bot_response})

if __name__ == '__main__':
    app.run()
