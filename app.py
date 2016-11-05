from flask import Flask, render_template, request, session, redirect, url_for
from database.database import db_session, init_db
from models.faculty import faculty
from models.project import project
from models.student import student
from models.studentapplication import studentapplication
from models.fileurl import fileurl
from models.loginpage import loginpage
from ma_schema.facultyschema import facultyschema
from ma_schema.projectschema import projectschema
from ma_schema.studentschema import studentschema
from ma_schema.loginpageschema import loginpageschema
from ma_schema.studentapplicationschema import studentapplicationschema
from ma_schema.fileurlschema import fileurlschema
from werkzeug import check_password_hash
from werkzeug import generate_password_hash
from datetime import timedelta
import os
import uuid
import json
import boto3

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask("UraniumReborn", template_folder=tmpl_dir)
app.secret_key = "dev-key"


@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=30)


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

    if request.method == 'POST':
        reqData = request.get_data()
        reqDataJson = json.loads(reqData)

        sSchema = studentschema()
        appSchema = studentapplicationschema()

        studentJson = None
        applicationJson = None

        if 'student' in reqDataJson.keys():
            studentJson = constructStudent(reqDataJson['student'])
        if 'application' in reqDataJson.keys():
            applicationJson = constructApplication(reqDataJson['application'])

        stu = sSchema.load(studentJson, session=db_session).data
        stuapp = appSchema.load(applicationJson, session=db_session).data

        db_session.add(stu)
        stuapp.s_id = stu.id

        db_session.commit()
        db_session.add(stuapp)
        db_session.commit()
        return render_template('home.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        reqData = json.loads(request.get_data())

        fSchema = facultyschema()
        lSchema = loginpageschema()
        sSchema = studentschema()

        loginPageJson = reqData['signupInfo']
        userJson = reqData['newUser']

        existingUser = loginpage.query.filter_by(Email=userJson['Email'].lower()).first()

        if existingUser:
            return redirect(url_for('signup'))

        userJson['id'] = str(uuid.uuid1())
        userJson['Phone'] = ""
        userJson['Department'] = ""
        loginPageJson['Email'] = userJson['Email']
        loginPageJson['Password'] = generate_password_hash(loginPageJson['Password'], method='pbkdf2:sha256',
                                                           salt_length=8)
        loginPageJson['id'] = str(uuid.uuid1())

        if loginPageJson['UserType'] == 'Faculty':
            userJson['is_grad'] = False
            userJson['isSupervisedBefore'] = False
            loginPageJson['f_id'] = userJson['id']
            loginPageJson['s_id'] = None
            fac = fSchema.load(userJson, session=db_session).data
            lgn = lSchema.load(loginPageJson, session=db_session).data
            db_session.add(fac)
            db_session.commit()
            db_session.add(lgn)
            db_session.commit()
        else:
            userJson['Student_id'] = ""
            userJson['LocalAddressLine1'] = ""
            userJson['LocalAddressLine2'] = ""
            userJson['LocalAddressCity'] = ""
            userJson['LocalAddressState'] = ""
            userJson['LocalAddressZip'] = ""
            userJson['SummerAddressLine_1'] = ""
            userJson['SummerAddressLine_2'] = ""
            userJson['SummerAddressCity'] = ""
            userJson['SummerAddressState'] = ""
            userJson['SummerAddressZip'] = ""
            userJson['PrimaryMajor'] = ""
            userJson['SecondaryMajor'] = ""
            userJson['GPA'] = ""
            userJson['StudentId'] = ""
            userJson['SchoolLevel'] = ""
            userJson['GraduationMonth'] = ""
            userJson['GraduationYear'] = ""
            userJson['isResearchExperience'] = ""
            userJson['isAppliedBefore'] = ""
            userJson['isBackgroundCheckDone'] = ""
            userJson['LastBackgroundCheckMonth'] = ""
            userJson['LastBackgroundCheckYear'] = ""
            userJson['isHarassmentTrainingDone'] = ""
            userJson['LastHarassmentTrainingMonth'] = ""
            userJson['LastHarassmentTrainingYear'] = ""
            userJson['resumeURL'] = ""
            loginPageJson['f_id'] = None
            loginPageJson['s_id'] = userJson['id']
            stud = sSchema.load(userJson, session=db_session)
            lgn = lSchema.load(loginPageJson, session=db_session)
            db_session.add(stud)
            db_session.commit()
            db_session.add(lgn)
            db_session.commit()
        session['name'] = userJson['FirstName'] + " " + userJson['LastName']
        session['email'] = userJson['Email']
        session['utype'] = loginPageJson['UserType']
        session['uid'] = userJson['id']
        return redirect(url_for('index'))
    elif request.method == 'GET':
        if 'email' in session:
            return redirect(url_for('index'))
        return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        credinfo = json.loads(request.get_data())
        email = credinfo['useremail']
        pwd = credinfo['password']
        lgn = loginpage.query.filter_by(Email=email.lower()).first()

        if lgn and check_password_hash(lgn.Password, pwd):
            session['email'] = email
            session['utype'] = lgn.UserType
            if lgn.UserType == 'Faculty':
                session['name'] = lgn.fac.FirstName + " " + lgn.fac.LastName
                session['uid'] = lgn.f_id
            elif lgn.UserType == 'Student':
                session['name'] = lgn.stud.FirstName + " " + lgn.stud.LastName
                session['uid'] = lgn.s_id
            return redirect(url_for('index'))
        else:
            return redirect(url_for('login'))
    else:
        if 'email' in session:
            return redirect(url_for('index'))

        return render_template('login.html')


@app.route('/sign-s3/')
def sign_s3():
    urlSchema = fileurlschema()

    # Load necessary information into the application
    S3_BUCKET = os.environ.get('S3_BUCKET')

    # Load required data from the request
    file_name = request.args.get('file-name')
    file_name2 = request.args.get('file-name2')

    # Initialise the S3 client
    s3 = boto3.client('s3')
    # Generate and return the presigned URL
    presigned_post = s3.generate_presigned_post(
        Bucket=S3_BUCKET,
        Key=file_name
    )

    presigned_post2 = s3.generate_presigned_post(
        Bucket=S3_BUCKET,
        Key=file_name2
    )

    url1 = "https://" + S3_BUCKET + ".s3.amazonaws.com/" + file_name
    url2 = "https://" + S3_BUCKET + ".s3.amazonaws.com/" + file_name2

    result = {}
    resume_url = url1
    coverletter_url = url2
    email = session['email']
    result['resume_url'] = resume_url
    result['coverletter_url'] = coverletter_url
    result['email_id'] = email
    result[u'id'] = str(uuid.uuid1())
    furl = urlSchema.load(result, session=db_session).data

    db_session.add(furl)
    db_session.commit()

    # Return the data to the client
    return json.dumps({
        'data1': presigned_post,
        'url1': 'https://%s.s3.amazonaws.com/%s' % (S3_BUCKET, file_name),
        'data2': presigned_post2,
        'url2': 'https://%s.s3.amazonaws.com/%s' % (S3_BUCKET, file_name2)
    })


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
    inpJson['specialRequirements'] = str(inpJson['specialRequirements'])
    inpJson['fieldOfStudy'] = str(inpJson['fieldOfStudy'])
    inpJson['isDevelopingCommunities'] = inpJson['isDevelopingCommunities'] == "Yes" if True else False
    inpJson['isDevelopingCommunities'] = False  ## what's this?
    return inpJson


def constructFaculty(inpJson, isgrad):
    if inpJson['FirstName'] != '':
        inpJson[u'id'] = str(uuid.uuid1())
        inpJson[u'is_grad'] = isgrad
        if 'isSupervisedBefore' in inpJson.keys():
            inpJson['isSupervisedBefore'] = inpJson['isSupervisedBefore'] == "Yes" if True else False
        else:
            inpJson['isSupervisedBefore'] = False
        return inpJson
    else:
        return None


def constructStudent(inpJson):
    if inpJson['FirstName'] != '':
        inpJson[u'id'] = str(uuid.uuid1())

        if 'isResearchExperience' in inpJson.keys():
            inpJson['isResearchExperience'] = inpJson['isResearchExperience'] == "Yes" if True else False
        else:
            inpJson['isResearchExperience'] = False

        inpJson['Race'] = str(inpJson['Race'])

        if 'isAppliedBefore' in inpJson.keys():
            inpJson['isAppliedBefore'] = inpJson['isAppliedBefore'] == "Yes" if True else False
        else:
            inpJson['isAppliedBefore'] = False

        if 'isBackgroundCheckDone' in inpJson.keys():
            inpJson['isBackgroundCheckDone'] = inpJson['isBackgroundCheckDone'] == "Yes" if True else False
        else:
            inpJson['isBackgroundCheckDone'] = False

        if 'isHarassmentTrainingDone' in inpJson.keys():
            inpJson['isHarassmentTrainingDone'] = inpJson['isHarassmentTrainingDone'] == "Yes" if True else False
        else:
            inpJson['isHarassmentTrainingDone'] = False

        return inpJson
    else:
        return None


def constructApplication(inpJson):
    inpJson[u'id'] = str(uuid.uuid1())
    return inpJson


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
        if secFacultyJson:
            secfac = fSchema.load(secFacultyJson, session=db_session).data
        else:
            secfac = None
        if gradStudentJson:
            gradStud = fSchema.load(gradStudentJson, session=db_session).data
        else:
            gradStud = None

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
            row = {"Faculty Name": f.FirstName + " " + f.LastName, "id": p.id, "Project Name": p.Title,
                   "Project Description": p.Description}
            rows.append(row)

    return render_template('listofprojects.html', pRows=rows)


if __name__ == '__main__':
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
