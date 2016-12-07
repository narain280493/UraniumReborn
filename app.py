from flask import Flask, render_template, request, session, redirect, url_for
from database.database import db_session, init_db
from models.faculty import faculty
from models.project import project
from models.student import student
from models.overrides import overrides
from models.studentapplication import studentapplication
from models.fileurl import fileurl
from models.loginpage import loginpage
from ma_schema.facultyschema import facultyschema
from ma_schema.projectschema import projectschema
from ma_schema.studentschema import studentschema
from ma_schema.loginpageschema import loginpageschema
from ma_schema.overrideschema import overrideschema
from ma_schema.studentapplicationschema import studentapplicationschema
from ma_schema.fileurlschema import fileurlschema
from werkzeug import check_password_hash
from werkzeug import generate_password_hash
from datetime import timedelta
import os
import uuid
import json
import boto3
from botocore.client import Config
from flask_cors import CORS, cross_origin

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask("UraniumReborn", template_folder=tmpl_dir)
cors = CORS(app, resources={r"/sign-s3/*": {"origins": "*"}})
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
        stu.id = session['uid']
        stuapp = appSchema.load(applicationJson, session=db_session).data

        db_session.merge(stu)
        stuapp.s_id = stu.id

        db_session.commit()
        db_session.add(stuapp)
        db_session.commit()
        return json.dumps({'status': 'OK'})


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
            return json.dumps({'status': 'existing user'})

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
            db_session.add(fac)
            db_session.commit()
            lgn = lSchema.load(loginPageJson, session=db_session).data
            lgn.f_id = fac.id
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
            userJson['isResearchExperience'] = False
            userJson['isAppliedBefore'] = False
            userJson['isWorkedBefore'] = False
            userJson['isGoldShirt'] = False
            userJson['isMSBSStudent'] = False
            userJson['isBackgroundCheckDone'] = ""
            userJson['LastBackgroundCheckMonth'] = ""
            userJson['LastBackgroundCheckYear'] = ""
            userJson['isHarassmentTrainingDone'] = ""
            userJson['LastHarassmentTrainingMonth'] = ""
            userJson['LastHarassmentTrainingYear'] = ""
            userJson['isAvailability'] = ""
            loginPageJson['f_id'] = None
            loginPageJson['s_id'] = userJson['id']
            stud = sSchema.load(userJson, session=db_session).data
            db_session.add(stud)
            db_session.commit()
            lgn = lSchema.load(loginPageJson, session=db_session).data
            lgn.s_id = stud.id
            db_session.add(lgn)
            db_session.commit()
        session['name'] = userJson['FirstName'] + " " + userJson['LastName']
        session['email'] = userJson['Email']
        session['utype'] = loginPageJson['UserType']
        session['uid'] = userJson['id']
        return json.dumps({'status': 'OK'})
    elif request.method == 'GET':
        if 'email' in session:
            return json.dumps({'status': 'OK'})
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
            return json.dumps({'status': 'OK'})
        else:
            return json.dumps({'status': 'Login Failed'})
    else:
        if 'email' in session:
            return json.dumps({'status': 'OK'})

        return render_template('login.html')


@app.route('/listmatches', methods=['GET'])
def listmatches():
    return render_template('listofmatches.html')


@app.route('/sign-s3/', methods=['GET', 'POST'])
def sign_s3():
    urlSchema = fileurlschema()

    S3_BUCKET = os.environ.get('S3_BUCKET')

    file_name = request.args.get('file-name')
    file_name2 = request.args.get('file-name2')

    # Initialise the S3 client
    s3 = boto3.client('s3', 'us-west-2', config=Config(signature_version='s3v4'))

    name = session['name']

    # appending users name before file in order to prevent it from being overwritten by another file with same name.
    file_name = name + '_' + file_name
    file_name2 = name + '_' + file_name2

    # Generate and return the presigned URL
    presigned_post = s3.generate_presigned_url('get_object', Params={'Bucket': S3_BUCKET, 'Key': file_name},
                                               ExpiresIn=3600, HttpMethod='PUT')
    presigned_post2 = s3.generate_presigned_url('get_object', Params={'Bucket': S3_BUCKET, 'Key': file_name2},
                                                ExpiresIn=3600, HttpMethod='PUT')

    result = {}
    email = session['email']
    fr = fileurl.query.filter_by(email_id=email).first()
    result['resume_url'] = "https://" + S3_BUCKET + ".s3.amazonaws.com/" + file_name
    result['coverletter_url'] = "https://" + S3_BUCKET + ".s3.amazonaws.com/" + file_name2
    result['email_id'] = email

    # if user has already inserted a resume once - just use existing id
    if fr:
        result[u'id'] = fr.id
    else:
        result[u'id'] = str(uuid.uuid1())

    furl = urlSchema.load(result, session=db_session).data

    db_session.merge(furl)
    db_session.commit()

    return json.dumps({
        'url1': presigned_post,
        'url2': presigned_post2
    })


@app.route('/logout')
def signout():
    if 'email' not in session:
        return render_template('login.html')

    session.pop('email', None)
    session.pop('name', None)
    session.pop('utype', None)
    session.pop('uid', None)
    return redirect(url_for('login'))


@app.route('/student')
def studentpage():
    if 'email' not in session:
        return redirect(url_for('index'))
    pList = project.query.with_entities(project.id, project.Title)
    pListJ = []

    for pid, ptit in pList:
        pListJ.append({"pid": pid, "Title": ptit})

    return render_template('student.html', pList=pListJ)


@app.route('/faculty')
def faculty_page():
    if 'email' not in session:
        return redirect(url_for('index'))

    return render_template('faculty.html')


def escape(inpString):
    inpString = inpString.replace('\"', '\\"')
    inpString = inpString.replace('\n', '\\n')
    inpString = inpString.replace('\r', '\\r')
    inpString = inpString.replace('\a', '\\a')
    inpString = inpString.replace('\b', '\\b')
    inpString = inpString.replace('\f', '\\f')
    inpString = inpString.replace('\r', '\\r')
    inpString = inpString.replace('\t', '\\t')
    return inpString


def constructProject(inpJson):
    inpJson[u'id'] = str(uuid.uuid1())
    inpJson['Description'] = escape(inpJson['Description'])
    inpJson['specialRequirements'] = json.dumps(inpJson['specialRequirements'])
    inpJson['fieldOfStudy'] = json.dumps(inpJson['fieldOfStudy'])
    inpJson['isDevelopingCommunities'] = inpJson['isDevelopingCommunities'] == "Yes" if True else False
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


@app.route('/override', methods=['POST'])
def overrideMatch():
    try:
        oSchema = overrideschema()
        oDataS = request.get_data()
        oDataJ = json.loads(oDataS)
        oObj = oSchema.load(oDataJ, session=db_session).data
        oObj.s_id = str(oDataJ['s_id'])
        oObj.p_id = str(oDataJ['p_id'])
        db_session.merge(oObj)
        db_session.commit()
    except Exception:
        return json.dumps({'status': 'override failed'})
    return json.dumps({'status': 'OK'})


@app.route('/getMatches')
def filterApplications():
    sSchema = studentschema()
    pSchema = projectschema()
    oSchema = overrideschema()
    saSchema = studentapplicationschema()

    stud = student.query.all()
    proj = project.query.all()


    overridenStudList = []
    overridenProjList = []
    overridenprojPrefList = []


    ## get re-assigned projects and students here
    over = overrides.query.all()
    for o in over:
        oJson = oSchema.dump(obj=o).data
        overridenStudList.append(getStudent(oJson['stud']))
        overridenProjList.append(oJson['proj'])
        stuApp = studentapplication.query.filter_by(s_id=oJson['stud']).first()
        saJson = saSchema.dump(obj=stuApp).data
        overridenprojPrefList.append(saJson)

    studList = []

    #filtering students
    for s in stud:
        sJson = sSchema.dump(obj=s).data
        gpa = sJson['GPA']
        isWorkedBefore = sJson['isWorkedBefore']
        isAvailability = sJson['isAvailability']
        isMSBSStudent = sJson['isMSBSStudent']
        firstName = sJson['FirstName']
        lastName = sJson['LastName']
        name = firstName + lastName

        if gpa < u'3':
            continue
        elif isWorkedBefore == True:
            continue
        elif isAvailability == 'Not sure' or isAvailability == 'No':
            continue
        elif isMSBSStudent == 'Yes':
            continue
        else:
            sJson['Race'] = json.loads(sJson['Race'])
            studList.append(sJson)


    ## remove re-assigned student from studList

    for st in overridenStudList:
        for s in studList:
            if s['id'] == st['id']:
                studList.remove(s)


    #filtering projects
    projList = []
    for p in proj:
        pJson = pSchema.dump(obj=p).data

        id = pJson['id']
        projPref1 = studentapplication.query.filter_by(ProjectPreference1=id).first()
        projPref2 = studentapplication.query.filter_by(ProjectPreference2=id).first()
        projPref3 = studentapplication.query.filter_by(ProjectPreference3=id).first()
        projPref4 = studentapplication.query.filter_by(ProjectPreference4=id).first()
        projPref5 = studentapplication.query.filter_by(ProjectPreference5=id).first()

        if projPref1 or projPref2 or projPref3 or projPref4 or projPref5:
            pJson["fieldOfStudy"] = json.loads(pJson["fieldOfStudy"])
            pJson["specialRequirements"] = json.loads(pJson["specialRequirements"])
            projList.append(pJson)

    # remove re-assigned project from ProjList here
    for id in overridenProjList:
        for p in projList:
            if p['id'] == id:
                projList.remove(p)

    data = {}
    rankedStudList = rankStudents(studList)
    assignedStudents, assignedProjects, assignedStudentProjPreferenceList = matchStudents(rankedStudList, projList)

    # add re-assigned students, projects and projectpreferencelist here

    assignedStudents = assignedStudents + overridenStudList
    assignedProjects  = assignedProjects + overridenProjList
    assignedStudentProjPreferenceList = assignedStudentProjPreferenceList + overridenprojPrefList

    for id in overridenProjList:
        projList.append(getProject(id))

    data['student'] = assignedStudents
    data['assignedProject'] = assignedProjects
    data['projects'] = projList
    data['projectPreference'] = assignedStudentProjPreferenceList
    json_data = json.dumps(data)

    return json_data


def constructProjectPreferences(saJson):
    projPrefList = []
    if len(saJson['ProjectPreference1']) > 0:
        projPrefList.append(saJson['ProjectPreference1'])
    if len(saJson['ProjectPreference2']) > 0:
        projPrefList.append(saJson['ProjectPreference2'])
    if len(saJson['ProjectPreference3']) > 0:
        projPrefList.append(saJson['ProjectPreference3'])
    if len(saJson['ProjectPreference4']) > 0:
        projPrefList.append(saJson['ProjectPreference4'])
    if len(saJson['ProjectPreference5']) > 0:
        projPrefList.append(saJson['ProjectPreference5'])
    return projPrefList


def getProject(project_id):
    pSchema = projectschema()
    proj = project.query.filter_by(id=project_id).first()
    pJson = pSchema.dump(obj=proj).data
    return pJson

def getStudent(student_id):
    sSchema = studentschema()
    stud = student.query.filter_by(id=student_id).first()
    sJson = sSchema.dump(obj=stud).data
    return sJson

def matchStudents(studList, projList):
    data = {}
    projIdList = []
    for proj in projList:
        projIdList.append(proj['id'])

    saSchema = studentapplicationschema()

    matchDict = {}
    unassignedStudents = []
    assignedStudents = []
    assignedProjects = []
    assignedStudentProjPreferenceList = []

    for stud in studList:
        # if there are no projects available, quit here itself.
        assignedProject = 0
        if len(projIdList) == 0:
            break
        stuApp = studentapplication.query.filter_by(s_id=stud['id']).first()
        saJson = saSchema.dump(obj=stuApp).data
        projPrefList = constructProjectPreferences(saJson)
        for proj in projPrefList:
            if proj in projIdList:
                matchDict[stud['id']] = proj
                projIdList.remove(proj)
                assignedProject = 1
                assignedStudents.append(stud)
                assignedProjects.append(proj)
                assignedStudentProjPreferenceList.append(saJson)
                break

        if assignedProject != 1:
            # keeping track of unassigned students
            unassignedStudents.append(stud)

    return assignedStudents, assignedProjects, assignedStudentProjPreferenceList


def rankStudents(studList):
    levelDict = {"Freshman":200, "Sophomore": 400, "Junior": 600, "Senior":800, "5th Year Senior":1000}
    genderDict = {"Male":0, "Female":50}
    rankDict = {}

    for stud in studList:
        score = 0

        score = score + levelDict[stud['SchoolLevel']] + genderDict[stud['Gender']]

        ## add more minorities if needed
        if stud['isSpanishOrigin'] == 'Yes' or stud['Race'] == 'Black or African-American':
            score = score + 50

        if stud['isGoldShirt'] == True:
            score = score + 50

        if stud['isAppliedBefore'] == True:
            score = score + 100

        gpa =  float(stud['GPA'])
        score = score + 100 * gpa

        rankDict[stud['id']] = score

    sortedList = sorted(sorted(rankDict), key=rankDict.get, reverse=True)

    sSchema = studentschema()

    rankedStudentList = []
    for element in sortedList:
        s = student.query.filter_by(id=element).first()
        sJson = sSchema.dump(obj=s).data
        sJson['Race'] = json.loads(sJson['Race'])
        rankedStudentList.append(sJson)

    return rankedStudentList


def constructStudent(inpJson):
    if inpJson['FirstName'] != '':
        inpJson[u'id'] = str(uuid.uuid1())

        if 'isResearchExperience' in inpJson.keys():
            inpJson['isResearchExperience'] = inpJson['isResearchExperience'] == "Yes" if True else False
        else:
            inpJson['isResearchExperience'] = False

        inpJson['Race'] = json.dumps(inpJson['Race'])

        if 'isAppliedBefore' in inpJson.keys():
            inpJson['isAppliedBefore'] = inpJson['isAppliedBefore'] == "Yes" if True else False
        else:
            inpJson['isAppliedBefore'] = False

        if 'isWorkedBefore' in inpJson.keys():
            inpJson['isWorkedBefore'] = inpJson['isWorkedBefore'] == "Yes" if True else False
        else:
            inpJson['isWorkedBefore'] = False

        if 'isGoldShirt' in inpJson.keys():
            inpJson['isGoldShirt'] = inpJson['isGoldShirt'] == "Yes" if True else False
        else:
            inpJson['isGoldShirt'] = False

        if 'isMSBSStudent' in inpJson.keys():
            inpJson['isMSBSStudent'] = inpJson['isGoldShirt'] == "Yes" if True else False
        else:
            inpJson['isMSBSStudent'] = False

        return inpJson
    else:
        return None


def constructApplication(inpJson):
    inpJson[u'id'] = str(uuid.uuid1())
    if 'preference1Requirements' not in inpJson:
        inpJson['preference1Requirements'] = ''
    else:
        inpJson['preference1Requirements'] = json.dumps(inpJson['preference1Requirements'])
    if 'preference2Requirements' not in inpJson:
        inpJson['preference2Requirements'] = ''
    else:
        inpJson['preference2Requirements'] = json.dumps(inpJson['preference2Requirements'])
    if 'preference3Requirements' not in inpJson:
        inpJson['preference3Requirements'] = ''
    else:
        inpJson['preference3Requirements'] = json.dumps(inpJson['preference3Requirements'])
    if 'preference4Requirements' not in inpJson:
        inpJson['preference4Requirements'] = ''
    else:
        inpJson['preference4Requirements'] = json.dumps(inpJson['preference4Requirements'])
    if 'preference5Requirements' not in inpJson:
        inpJson['preference5Requirements'] = ''
    else:
        inpJson['preference5Requirements'] = json.dumps(inpJson['preference5Requirements'])

    return inpJson


@app.route('/projects', methods=['GET', 'POST'])
def projects():
    if 'email' not in session:
        return redirect(url_for('index'))

    projs = project.query.all()
    pSchema = projectschema()
    projsL = []
    for p in projs:
        pJson = pSchema.dump(obj=p).data
        pJson["fieldOfStudy"] = json.loads(pJson["fieldOfStudy"])
        pJson["specialRequirements"] = json.loads(pJson["specialRequirements"])
        projsL.append(pJson)

    return json.dumps(projsL)


@app.route('/listofprojects', methods=['GET', 'POST'])
def listofprojects():
    if 'email' not in session:
        return redirect(url_for('index'))

    fSchema = facultyschema()
    pSchema = projectschema()

    if request.method == 'POST':
        reqData = request.get_data()
        reqDataJson = json.loads(reqData)

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
        fac.id = session['uid']
        db_session.merge(fac)
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
                   "Project Description": p.Description, "Faculty Department": f.Department,
                   "Student Majors": json.loads(p.fieldOfStudy)}
            rows.append(row)

    projs = project.query.all()
    projsL = []
    for p in projs:
        pJson = pSchema.dump(obj=p).data
        pJson["fieldOfStudy"] = json.loads(pJson["fieldOfStudy"])
        pJson["specialRequirements"] = json.loads(pJson["specialRequirements"])
        projsL.append(pJson)

    return render_template('listofprojects.html', pRows=rows, pFRows=projsL)


if __name__ == '__main__':
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
