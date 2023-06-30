import subprocess
from flask import Flask, request, jsonify, render_template, session

app = Flask(__name__)

# Global variables to store user inputs
username = ""
repository = ""
destination = ""
branch = ""

@app.route('/', methods=['GET', 'POST'])
def index():
    if session.get('current_step') == 'branch':
        bot_response = "Please enter the branch name:"
    elif session.get('current_step') == 'destination':
        bot_response = "Please enter the destination path:"
    elif session.get('current_step') == 'repository':
        bot_response = "Please enter the repository name:"
    elif session.get('current_step') == 'username':
        bot_response = "Please enter your username:"
    else:
        bot_response = "Welcome! Please enter a command or select an option:<br/><button type='button' class='option-button' onclick='sendOption(\"Clone Repository\")'>Clone Repository</button>"

    return render_template('index.html', bot_response=bot_response)

@app.route('/process', methods=['POST'])
def process():
    global username, repository, destination, branch

    user_input = request.form['user_input']

    perform_clone = False  # Initialize perform_clone variable

    if user_input == "Clone Repository":
        session['current_step'] = 'username'
        bot_response = "Please enter your username:"
    elif session.get('current_step') == 'username':
        username = user_input
        session['current_step'] = 'repository'
        bot_response = "Please enter the repository name:"
    elif session.get('current_step') == 'repository':
        repository = user_input
        session['current_step'] = 'destination'
        bot_response = "Please enter the destination path:"
    elif session.get('current_step') == 'destination':
        destination = user_input
        session['current_step'] = 'branch'
        bot_response = "Please enter the branch name:"
    elif session.get('current_step') == 'branch':
        branch = user_input
        session['current_step'] = None
        perform_clone = True
        bot_response = "Cloning repository..."
    else:
        bot_response = "Invalid command. Please try again."

    if perform_clone:
        url = f"https://bitbucket.mycompany.com/{username}/{repository}.git"
        password = "<password>"  # Replace with the actual password

        try:
            # Store the credentials in the credentials manager
            process = subprocess.Popen(["git", "credential", "approve"], stdin=subprocess.PIPE)
            process.stdin.write(f"url={url}\nusername={username}\npassword={password}\n".encode())
            process.stdin.close()
            process.wait()

            # Clone the repository
            subprocess.run(["git", "clone", url, destination])

            # Checkout the specified branch
            subprocess.run(["git", "-C", destination, "checkout", branch])

            bot_response = "Repository cloned successfully."
        except subprocess.CalledProcessError as e:
            bot_response = f"Error cloning repository: {e}"

        # Reset the global variables for the next interaction
        username = ""
        repository = ""
        destination = ""
        branch = ""

    return jsonify({'bot_response': bot_response})

if __name__ == '__main__':
    app.secret_key = 'your_secret_key'
    app.run()



import subprocess

def clone_repository(url, username, password, destination):
    # Remove the existing Git configuration related to credentials
    subprocess.run(["git", "config", "--unset", "user.name"])
    subprocess.run(["git", "config", "--unset", "user.email"])
    subprocess.run(["git", "config", "--unset-all", "credential.helper"])

    # Set the new username and password for the repository
    subprocess.run(["git", "config", "--global", "user.name", username])
    subprocess.run(["git", "config", "--global", "user.password", password])

    # Clone the repository with the provided credentials
    subprocess.run(["git", "clone", url, destination])

# Example usage
url = "https://bitbucket.mycompany.com/SCM/ngbauto/mb_implementation.git"
username = "your_username"
password = input("Please enter your password: ")
destination = "path/to/destination"
clone_repository(url, username, password, destination)
