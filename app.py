"""
Concept of building web forms from a yaml file with python using flask
Created 2021-11-01
"""

from flask import Flask, render_template, request
import yaml
import datetime

# Set input file
inputfile = "quiz.yml"

# Initiate flask
app = Flask(__name__)


@app.route("/")
def index():
    """read from inputfile and push that to the index page"""
    # open quiz file to build form page and set title
    with open(inputfile, "r") as quiz_file:
        quiz = yaml.load(quiz_file, Loader=yaml.FullLoader)
    title = "PyQuiz" if not "title" in quiz.keys() else quiz["title"]

    # show form page
    return render_template("index.html", title=title, quiz=quiz)


@app.route("/form", methods=["POST"])
def form():
    """get submitted form result"""
    # open quiz file and set response and title
    with open(inputfile, "r") as quiz_file:
        quiz = yaml.load(quiz_file, Loader=yaml.FullLoader)
    response = (
        "Thanks for your answer!" if not "response" in quiz.keys() else quiz["response"]
    )
    title = "PyQuiz" if not "title" in quiz.keys() else quiz["title"]

    # build a dict of responses
    result = {}
    for ids, values in quiz.items():
        if ids not in ["title", "response"] and isinstance(values, dict):
            # in radios we need to figure out what value that has been choosen
            if values.get("form") == "radio":
                choice = ""
                for option in values.get("options"):
                    if option in request.form.keys():
                        choice = option
                result[ids] = choice
            else:
                # in all other cases getting the value from the form i straight forward
                result[ids] = request.form.get(ids)

    # save response to result file
    with open(f'{title.replace(" ", "_")}.yml', "a") as outfile:
        yaml.dump(
            {datetime.datetime.now().isoformat(): result},
            outfile,
            default_flow_style=False,
        )

    # show response form page
    return render_template("form.html", response=response)
