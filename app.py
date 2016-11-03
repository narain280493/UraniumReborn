from flask import Flask, render_template, request, session, redirect, url_for
from forms import SignupForm
from database.database import db_session, init_db
from models.faculty import faculty
from models.project import project
from models.loginpage import loginpage
from ma_schema.facultyschema import facultyschema
from ma_schema.projectschema import projectschema
from werkzeug import check_password_hash
from datetime import timedelta
import os
import uuid
import json

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask("UraniumReborn", template_folder=tmpl_dir)
app.secret_key = "dev-key"


@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=5)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        if 'email' in session:
            return render_template('home.html')
        else:
            return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if request.method == 'POST':

        if not form.validate():
            return render_template('signup.html', form=form)
        else:
            name = form.first_name.data + ' ' + form.last_name.data
            existingUser = loginpage.query.filter_by(username=form.email.data.lower()).first()

            # check whether user already exists
            if existingUser:
                return redirect(url_for('signup'))
            else:
                newuser = loginpage(form.email.data, name, form.password.data)
                db_session.add(newuser)
                db_session.commit()
                session['email'] = form.email.data
                session['name'] = name
                return redirect(url_for('index'))

    elif request.method == 'GET':

        if 'email' in session:
            return redirect(url_for('index'))
        return render_template('signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('useremail')
        passwd = request.form.get('password')
        user = loginpage.query.filter_by(username=email.lower()).first()

        if user and check_password_hash(user.passwdhash, passwd):
            session['email'] = email
            session['name'] = user.name
            return redirect(url_for('index'))
        else:
            return redirect(url_for('login'))
    else:
        if 'email' in session:
            return redirect(url_for('index'))

        return render_template('login.html')


@app.route('/logout')
def signout():
    if 'email' not in session:
        return render_template('login.html')

    session.pop('email', None)
    session.pop('name', None)
    return render_template('login.html')


@app.route('/student')
def student():
    if 'email' not in session:
        return redirect(url_for('index'))
    return render_template('student.html')


@app.route('/faculty')
def faculty_page():
    if 'email' not in session:
        return redirect(url_for('index'))

    return render_template('faculty.html')


def constructProject(inpJson):
    inpJson[u'id'] = str(uuid.uuid1())

    if 'specialRequirements' in inpJson.keys():
        inpJson['specialRequirements'] = str(inpJson['specialRequirements'])
    else:
        inpJson['specialRequirements'] = ""

    if 'isDevelopingCommunities' in inpJson.keys():
        inpJson['isDevelopingCommunities'] = inpJson['isDevelopingCommunities'] == no if False else True
    else:
        inpJson['isDevelopingCommunities'] = False

    return inpJson


def constructFaculty(inpJson, isgrad):
    if inpJson['FirstName'] == '':
        inpJson[u'id'] = str(uuid.uuid1())
        inpJson[u'is_grad'] = isgrad
        if 'isSupervisedBefore' in inpJson.keys():
            inpJson['isSupervisedBefore'] = inpJson['isSupervisedBefore'] == "no" if False else True
        else:
            inpJson['isSupervisedBefore'] = False
        return inpJson
    else:
        return None


@app.route('/listofprojects', methods=['GET', 'POST'])
def listofprojects():
    if 'email' not in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        reqData = request.get_data()
        reqDataJson = json.loads(reqData)

        fSchema = facultyschema()
        pSchema = projectschema()

        facultyJson = None
        secFacultyJson = None
        gradStudentJson = None
        projJson = None

        if 'faculty' in reqDataJson.keys():
            facultyJson = constructFaculty(reqDataJson['faculty'], False)
        if 'secondFaculty' in reqDataJson.keys():
            secFacultyJson = constructFaculty(reqDataJson['secondFaculty'], False)
        if 'gradStudent' in reqDataJson.keys():
            gradStudentJson = constructFaculty(reqDataJson['gradStudent'], True)
        if 'apprenticeship' in reqDataJson.keys():
            projJson = constructProject(reqDataJson['apprenticeship'])

        fac = fSchema.load(facultyJson, session=db_session).data
        secfac = fSchema.load(secFacultyJson, session=db_session).data
        gradStud = fSchema.load(gradStudentJson, session=db_session).data
        proj = pSchema.load(projJson, session=db_session).data

        db_session.add(fac)
        proj.f_id = fac.id

        if secfac:
            db_session.add(secfac)
            proj.sf_id = secfac.id
        if gradStud:
            db_session.add(gradStud)
            proj.g_id = gradStud.id

        db_session.commit()
        db_session.add(proj)
        db_session.commit()

    facs = faculty.query.all()
    rows = []

    for f in facs:
        for p in f.projects:
            row = {"Faculty Name": f.FirstName + f.LastName, "id": p.id, "Project Name": p.Title,
                   "Project Description": p.Description}
            rows.append(row)

    return render_template('listofprojects.html', pRows=rows)


if __name__ == '__main__':
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
