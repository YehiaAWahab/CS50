import cs50
import csv

from flask import Flask, jsonify, redirect, render_template, request
import csv

# Configure application
app = Flask(__name__)

# Reload templates when they are changed
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.after_request
def after_request(response):
    """Disable caching"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET"])
def get_index():
    return redirect("/form")


@app.route("/form", methods=["GET"])
def get_form():
    return render_template("form.html")


@app.route("/form", methods=["POST"])
def post_form():
    name = request.form.get("name")
    house = request.form.get("house")
    position = request.form.get("position")
    if (not name) or (not house) or (position == "None"):
        return render_template("error.html", message="You have to provide Name, House and Position.")
    row = [name, house, position]
    with open('survey.csv', mode='a') as survey_file:
        survey_writer = csv.writer(survey_file)
        survey_writer.writerow(row)
    return redirect("/sheet")


@app.route("/sheet", methods=["GET"])
def get_sheet():
    row_count = 0
    rows = []
    with open('survey.csv', 'r') as survey_file:
        survey_reader = csv.reader(survey_file)
        for row in survey_reader:
            rows.append(row)
    return render_template("sheet.html", rows=rows)
