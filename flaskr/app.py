from flask_bootstrap import Bootstrap4
from flask import Flask, render_template

app = Flask(__name__)
bootstrap = Bootstrap4(app)


@app.route('/')
def homePage():
    return render_template('index.html', title="Home")

@app.route("/newInputs")
def newInputsPage():
    return render_template("newInputs.html", title="New Inputs")

@app.route("/records")
def recordsPage():
    return render_template("records.html", title="Records")

@app.route("/settings")
def settingsPage():
    return render_template("settings.html", title="Settings")


if __name__ == '__main__':
    app.run(debug=True)
