from flask import Flask
from flask import render_template
from flask import request
from database.database import db_session
from database.database import init_db
from models.project_name import project_name
import os

app = Flask("UraniumReborn")


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.route("/", methods=['POST', 'GET'])
def mainpage():
    if request.method == 'POST':
        pn = project_name(request.form['Name'])
        db_session.add(pn)
        db_session.commit()
        result = project_name.query.all()
        return str(result).replace("<", "").replace(">", "")
    else:
        return render_template("mainpage.html")



init_db()
port = int(os.environ.get("PORT", 5000))
app.run(host='0.0.0.0', port=port)


