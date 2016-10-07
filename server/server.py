from flask import Flask
from flask import render_template
from flask import request
from database.database import db_session
from database.database import init_db
from models.faculty import faculty
from models.project import project
import os

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask("UraniumReborn",template_folder=tmpl_dir)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.route("/", methods=['POST', 'GET'])
def mainpage():
    if request.method == 'POST':
        f_name = request.form['facultyName']
        f_ph = request.form['']
        f_email = request.form['']
        f_dept = request.form['']
        f = faculty(f_name,f_ph,f_email,f_dept,False)
        sf = None
        g = None

        sf_name = request.form['']
        sf_ph = request.form['']
        sf_email = request.form['']
        sf_dept = request.form['']

        if sf_name:
        	sf = faculty(sf_name,sf_ph,sf_email,sf_dept,False)

        g_name = request.form['']
        g_ph = request.form['']
        g_email = request.form['']
        g_dept = request.form['']

        if g_name:
        	g = faculty(g_name,g_ph,g_email,g_dept,True)

        is_focus = request.form['']
        p_title = request.form['']
		p_website = request.form['']
		p_req = request.form['']
		p_desc = request.form['']
		p_dept_n = request.form['']
		p_amt_sup = request.form['']
		p_sup_prov = request.form['']
		p_nat_w = request.form['']
		p_amt_pr = request.form['']
		p_n_spec_stud = request.form['']
		p_sp_typ = request.form['']
		p_acc_cnt = request.form['']
		p_has_sup_dla = request.form['']

		p = project(p_title, is_focus, p_website, p_req, p_desc, p_dept_n,p_amt_sup,p_sup_prov, p_nat_w, p_amt_pr,p_n_spec_stud, p_sp_typ, p_acc_cnt, p_has_sup_dla)

        db_session.add(p)

        if g:
        	db_session.add(g)
        if sf:
        	db_session.add(sf)
        
        db_session.add(f)

        db_session.commit()
        result = project.query.all()
        return str(result).replace("<", "").replace(">", "")
    else:
        return render_template("mainpage.html")



init_db()
port = int(os.environ.get("PORT", 5000))
app.run(host='0.0.0.0', port=port)


