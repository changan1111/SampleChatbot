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
                print("Branches:", branches)  # Print the branch list
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
    
    return render_template('index.html', branches=[], branch_selected=False)

if __name__ == '__main__':
    app.run()
