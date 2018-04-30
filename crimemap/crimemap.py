import datetime
import json
import string

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


def sanitize_string(user_input):
    whitelist = string.letters + string.digits + " !?.,;:-'()&"
    return filter(lambda x: x in whitelist, user_input)


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
            return home("Invalid category")
        date = format_date(request.form.get("date"))
        if not date:
            error_message = "Invalid date. Please use yyyy-mm-dd format"
            return home(error_message=error_message)

        try:
            latitude = float(request.form.get("latitude"))
            longitude = float(request.form.get("longitude"))
        except ValueError:
            error_message = "Latitude or Longitude have incorrect format"
            return home(error_message=error_message)

        description = sanitize_string(request.form.get("description"))
        DB.add_crime(category, date, latitude, longitude, description)
        return home(error_message=error_message)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    app.run(port=5000, debug=True)
