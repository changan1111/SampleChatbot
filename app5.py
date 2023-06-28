import os
import subprocess
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Get the absolute path of the directory containing the app.py file
current_directory = os.path.dirname(os.path.abspath(__file__))

# Flag variable to track the status of test suite execution
is_test_suite_running = False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    global is_test_suite_running

    user_input = request.form['user_input']
    
    if user_input == "Run Test Suite":
        options = ["Functional Testing", "Regression Testing", "Security Testing"]
        button_html = ""
        for option in options:
            button_html += f'<button type="button" class="option-button" onclick="sendOption(\'{option}\')">{option}</button>'
        bot_response = f"Please select an option:<br/>{button_html}"
    elif user_input == "Regression Testing":
        if is_test_suite_running:
            bot_response = "A test suite is already running. Please wait for it to complete."
        else:
            try:
                is_test_suite_running = True
                # Run the Maven command and capture the output
                result = subprocess.run(['mvn', 'clean', 'test'], cwd=current_directory, shell=True, capture_output=True, text=True)
                output = result.stdout.strip()  # Get the output from the completed process
                
                # Format the output log with specific styles
                formatted_output = format_output_log(output)
                
                # Check if the test execution was successful or not
                if result.returncode == 0:
                    bot_response = f"<span class='passed'>Regression testing completed. Result: Passed</span><br/>{formatted_output}"
                else:
                    bot_response = f"<span class='failed'>Regression testing completed. Result: Failed</span><br/>{formatted_output}"
            except FileNotFoundError:
                bot_response = "Maven or testng.xml file not found. Make sure you have the required files."
            finally:
                is_test_suite_running = False
    else:
        bot_response = "Invalid command. Please try again."
    
    return jsonify({'bot_response': bot_response})

def format_output_log(output):
    # Format the output log with specific styles
    formatted_log = ""
    lines = output.split("\n")
    test_runs = 0
    failures = 0
    errors = 0
    skipped = 0

    for line in lines:
        if "Tests run" in line:
            test_runs = int(line.split(":")[1].split(",")[0].strip())
            formatted_log += f"<span class='tests-run'>Tests run: {test_runs}</span><br/>"
        elif "Failures" in line:
            failures = int(line.split(":")[1].strip())
            formatted_log += f"<span class='failures'>Failures: {failures}</span><br/>"
        elif "Errors" in line:
            errors = int(line.split(":")[1].strip())
        elif "Skipped" in line:
            skipped = int(line.split(":")[1].strip())

        formatted_log += f"{line}<br/>"

    passed = test_runs - failures - errors - skipped
    formatted_log += f"<span class='passed'>Passed: <span class='passed-number'>{passed}</span></span><br/>"
    formatted_log += f"<span class='failures'>Failures: {failures}</span><br/>"
    formatted_log += f"<span class='errors'>Errors: {errors}</span><br/>"

    # Generate the summary information
    summary = f"<br/><br/><span class='summary'>Regression testing completed. Result: "
    if failures == 0 and errors == 0:
        summary += "<span class='result-passed'>Passed</span></span><br/>"
    else:
        summary += "<span class='result-failed'>Failed</span></span><br/>"

    summary += f"Tests run: {test_runs}<br/>"
    summary += f"Passed: {passed}<br/>"
    summary += f"Failures: {failures}<br/>"
    summary += f"Errors: {errors}<br/>"

    return formatted_log + summary






if __name__ == '__main__':
    app.run()
