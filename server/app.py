from flask import Flask, render_template, request
from forms import SignupForm
from database.database import db_session, init_db
import os
import json
from models.faculty import faculty
from models.project import project

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask("UraniumReborn", template_folder=tmpl_dir)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

app.secret_key = "dev-key"


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/signup', methods = ['GET', 'POST'])
def signup():    
    form = SignupForm()
    if request.method == 'POST':
        if form.validate() == False:
            return render_template('signup.html', form=form)
        else:
            return "Dummy Signup"
    elif request.method == 'GET':
        return render_template('signup.html', form=form)


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/student')
def student():
    return render_template('student.html')


@app.route('/faculty')
def faculty_page():
    return render_template('faculty.html')


@app.route('/listofprojects', methods=['GET', 'POST'])
def listofprojects():

    if request.method == 'POST':
        f_first_name = request.form.get('facultyFirstName', None)
        f_last_name = request.form.get('facultyLastName',None)

        name = f_first_name +' ' + f_last_name

        f_ph = request.form.get('facultyPhone', None)
        f_email = request.form.get('facultyEmail', None)
        f_dept = request.form.get('facultyDepartment', None) #---
        sf = None
        g = None

        sf_first_name = request.form.get('secondFacultyFirstName',None)
        sf_last_name = request.form.get('secondFacultyLastName',None)

        sf_name= sf_first_name + ' ' + sf_last_name

        sf_ph = request.form.get('secondFacultyPhone',None)
        sf_email = request.form.get('secondFacultyEmail',None)
        sf_dept = request.form.get('secondDepartment',None)

        g_first_name = request.form.get('gradStudentFirstName',None)
        g_last_name = request.form.get('gradStudentLastName',None)

        g_name = g_first_name+ ' ' + g_last_name
        g_ph = request.form.get('gradStudentPhone',None)
        g_email = request.form.get('gradStudentEmail',None)

        is_focus = request.form.get('isDevelopingCommunities', False)
        print is_focus

        if is_focus == "yes":
            is_focus_value= True
        else:
            is_focus_value= False

        print is_focus_value
        p_title = request.form.get('apprenticeshipTitle',None)
        p_website = request.form.get('apprenticeshipWeblink',None)
        p_req = request.form.get('specialRequirements1',None) + '::' + request.form.get('specialRequirements2', None) + '::' + request.form.get(
            'specialRequirements3', None) + '::' + request.form.get('specialRequirements4', None) + '::' + request.form.get(
            'specialRequirements5', None)
        p_desc = request.form.get('apprenticeshipDescription',None)
        p_dept_n = str(request.form.getlist('fieldOfStudy[]'))
        print p_dept_n
        p_amt_sup = request.form.get('amountOfSupervision', None)
        p_sup_prov = request.form.get('supervisor', None)
        p_nat_w = request.form.get('primaryNature', None)
        p_amt_pr = request.form.get('priorWork', None)
        p_n_spec_stud = request.form.get('desiredStudent', None)
        p_sp_typ = request.form.get('speedType', None)
        p_acc_cnt = request.form.get('accountingContactName', None)
        p_has_sup_dla = request.form.get('isSupervisedBefore', 'yes') == 'yes' if True else False

        p = project(p_title, is_focus_value, p_website, p_req, p_desc, p_dept_n, p_amt_sup, p_sup_prov, p_nat_w, p_amt_pr,
                    p_n_spec_stud, p_sp_typ, p_acc_cnt, p_has_sup_dla)

        f = faculty(name, f_ph, f_email, f_dept, False, p.get_id())

        if sf_name:
            sf = faculty(sf_name, sf_ph, sf_email, sf_dept, False, p.get_id())
        if g_name:
            g = faculty(g_name, g_ph, g_email, None, True, p.get_id())


        db_session.add(p)
        db_session.commit()
        db_session.add(f)
        if g:
            db_session.add(g)
        if sf:
            db_session.add(sf)
        db_session.commit()

    facs = faculty.query.all()
    rows = []

    for f in facs:
        for p in f.projects:
            row = {"Faculty Name": f.faculty_name, "id": p.id, "Project Name": p.title, "Project Description": p.description}
            rows.append(row)

    return render_template('listofprojects.html', pRows=rows)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
