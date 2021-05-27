from flask import Flask, request, render_template
from word_tree_api.wordtree import get_paths, read_files, WordTree

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/<name>", methods=['GET', 'POST'])
def greeting(name):
    username = request.args.get('username')
    return "Hello %s!! Your username is %s" % (name, username)



if __name__ == "__main__":
    app.run(debug=True)