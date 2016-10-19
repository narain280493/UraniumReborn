from flask import Flask, render_template
from database.database import init_db
from database.database import db_session
import os

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask("UraniumReborn", template_folder=tmpl_dir)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/student')
def student():
    return render_template('student.html')


@app.route('/faculty')
def faculty():
    return render_template('faculty.html')


@app.route('/listofprojects')
def listofprojects():
    return render_template('listofprojects.html')


if __name__ == '__main__':
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
