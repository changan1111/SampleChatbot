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
    bot_response = "Welcome! Please enter a command or select an option:<br/><button type='button' class='option-button' onclick='sendOption(\"Run Test Suite\")'>Run Test Suite</button>"
    return render_template('index.html', bot_response=bot_response)

@app.route('/process', methods=['POST'])
def process():
    global is_test_suite_running

    user_input = request.form['user_input']
    testng_file = ""

    if user_input == "Run Test Suite":
        if is_test_suite_running:
            bot_response = "A test suite is already running. Please wait for it to complete."
        else:
            options = ["Sanity", "Regression", "Security", "K2GTest"]
            button_html = ""
            for option in options:
                button_html += f'<button type="button" class="option-button" onclick="sendOption(\'{option}\')">{option}</button>'
            bot_response = f"Please select an option:<br/>{button_html}"
    elif user_input == "Sanity":
        if is_test_suite_running:
            bot_response = "A test suite is already running. Please wait for it to complete."
        else:
            is_test_suite_running = True
            testng_file = "testng_sanity.xml"
            bot_response = "Performing Sanity testing..."
    elif user_input == "Regression":
        if is_test_suite_running:
            bot_response = "A test suite is already running. Please wait for it to complete."
        else:
            is_test_suite_running = True
            testng_file = "testng.xml"
            bot_response = "Performing Regression testing..."
    elif user_input == "Security":
        if is_test_suite_running:
            bot_response = "A test suite is already running. Please wait for it to complete."
        else:
            is_test_suite_running = True
            testng_file = "testng_securitytest.xml"
            bot_response = "Performing Security testing..."
    elif user_input == "K2GTest":
        if is_test_suite_running:
            bot_response = "A test suite is already running. Please wait for it to complete."
        else:
            is_test_suite_running = True
            testng_file = "testng_ktog.xml"
            bot_response = "Performing K2GTest..."
    else:
        bot_response = "Invalid command. Please try again."

    if testng_file:
        try:
            # Run the Maven command and pass the test suite file name as an argument
            process = subprocess.Popen(['mvn', 'clean', 'test', '-DsuiteXmlFile=' + testng_file], cwd=current_directory, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

            # Read the output from the process
            output, _ = process.communicate()

            # Format the output log with specific styles
            formatted_output = format_output_log(output.strip())

            # Check if the test execution was successful or not
            if process.returncode == 0:
                bot_response = f"<span class='passed'>Testing completed. Result: Passed</span><br/>{formatted_output}"
            else:
                bot_response = f"<span class='failed'>Testing completed. Result: Failed</span><br/>{formatted_output}"
        except FileNotFoundError:
            bot_response = "Maven or testng.xml file not found. Make sure you have the required files."
        finally:
            is_test_suite_running = False

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
        if not line.strip():  # Skip empty lines
            continue
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
    formatted_log += f"<span class='skipped'>Skipped: {skipped}</span><br/>"

    # Generate the summary information
    summary = f"<br/><br/><span class='summary'>Testing completed. Result: "
    if failures == 0 and errors == 0:
        summary += "<span class='result-passed'>Passed</span></span><br/>"
    else:
        summary += "<span class='result-failed'>Failed</span></span><br/>"

    summary += f"Tests run: {test_runs}<br/>"
    summary += f"<span class='result-green'>Passed: <span class='result-green'>{passed}</span></span><br/>"
    summary += f"<span class='result-failed'>Failures: <span class='result-failed'>{failures}</span></span><br/>"
    summary += f"Errors: {errors}</span><br/>"
    summary += f"Skipped: {skipped}</span><br/>"

    return formatted_log + summary


if __name__ == '__main__':
    app.run()
