from flask import Flask, render_template

app = Flask(__name__)


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
    app.run(debug=True)
