from flask import Flask
from flask import render_template
from flask import request

app = Flask("UraniumReborn")


@app.route("/", methods=['POST', 'GET'])
def mainpage():
    if request.method == 'POST':
        return request.form['Name']
    else:
        return render_template("mainpage.html")

app.run()

