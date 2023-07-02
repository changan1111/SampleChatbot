import json
import git
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Global variables to store user inputs
username = ""
password = ""
repository = ""
destination = ""
branch = ""

def get_branch_list():
    repo = git.Repo(destination)
    branches = [b.name for b in repo.branches]
    return branches

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        global username, password, repository, destination, branch

        if request.form['user_input'] == "Clone Repository":
            username = request.form['username']
            password = request.form['password']
            repository = request.form['repository']
            destination = request.form['destination']
            
            url = f"https://{username}:{password}@bitbucket.mycompany.com/{repository}.git"
            
            try:
                git.Repo.clone_from(url, destination)
                branches = get_branch_list()
                return render_template('index.html', branches=branches, branch_selected=False)
            except git.exc.GitCommandError as e:
                return render_template('index.html', error=str(e))

        elif request.form.get('branch'):
            branch = request.form['branch']
            try:
                repo = git.Repo(destination)
                repo.git.checkout(branch)
                return render_template('index.html', branches=get_branch_list(), branch_selected=True)
            except git.exc.GitCommandError as e:
                return render_template('index.html', branches=get_branch_list(), branch_selected=False, error=str(e))

        elif request.form.get('city'):
            selected_city = request.form['city']
            if selected_city == "Main City":
                # Read the startup.json file
                with open('startup.json') as file:
                    json_data = file.read()
                
                # Parse the JSON data
                data = json.loads(json_data)
                
                # Update the main city value in the JSON data
                data['main_city'] = selected_city
                
                # Write the updated JSON data back to the file
                with open('startup.json', 'w') as file:
                    file.write(json.dumps(data, indent=2))
                    
    # Read the startup.json file
    with open('startup.json') as file:
        json_data = file.read()

    # Parse the JSON data
    data = json.loads(json_data)

    # Get the list of cities
    cities = [hotel['city'] for hotel in data['hotels']]

    # Insert "Main City" option at the beginning of the list
    cities.insert(0, "Main City")

    # Pass the cities to the HTML template
    return render_template('index.html', cities=cities)

if __name__ == '__main__':
    app.run()
