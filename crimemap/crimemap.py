import datetime
import json

import dateparser
from flask import Flask
from flask import render_template
from flask import request

from dbhelper import DBHelper

app = Flask(__name__)
DB = DBHelper()

categories = ['mugging', 'break-in']


def format_date(user_data):
    date = dateparser.parse(user_data)
    try:
        return datetime.datetime.strftime(date, "%Y-%m-%d")
    except TypeError:
        return None


@app.route("/")
def home(error_message=None):
    crimes = DB.get_all_crimes()
    crimes = json.dumps(crimes)
    return render_template("home.html", crimes=crimes, categories=categories, error_message=error_message)


@app.route("/submitcrime", methods=["POST"])
def submit_crime():
    try:
        error_message = None
        category = request.form.get("category")
        if category not in categories:
            return home("Invalid category.")
        date = format_date(request.form.get("date"))
        if not date:
            return home("Invalid date. Please use yyyy-mm-dd format")
        latitude = float(request.form.get("latitude"))
        longitude = float(request.form.get("longitude"))
        description = request.form.get("description")
        DB.add_crime(category, date, latitude, longitude, description)
        return home(error_message=error_message)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    app.run(port=5000, debug=True)
