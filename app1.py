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
            button_html += f'<button type="button" class="option-button" data-option="{option}">{option}</button>'
        bot_response = f"Please select an option:<br/>{button_html}"
    elif user_input == "Regression Testing":
        try:
            # Specify the absolute path to the TestNG XML file
            #xml_file_path = os.path.join(current_directory, 'C:\Users\Chandrasekaran\eclipse-workspace\DreamHotelSuite')
            
            # Run the TestNG XML file
            subprocess.run(['cmd.exe', 'C:\\Users\\Chandrasekaran\\eclipse-workspace\\DreamHotelSuite', 'mvn clean test'])
            
            bot_response = "Regression testing started."
        except FileNotFoundError:
            bot_response = "TestNG or testng.xml file not found. Make sure you have the required files."
    else:
        bot_response = "Invalid command. Please try again."
    
    return jsonify({'bot_response': bot_response})

if __name__ == '__main__':
    app.run()
