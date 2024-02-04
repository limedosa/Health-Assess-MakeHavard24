from flask_bootstrap import Bootstrap4
from flask import Flask, render_template
from openai import OpenAI
import os

openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# construct a prompt
user_prompt = f"You are a health assess assistance. You have been given the the heartbeat data: 70 bmp. Base on this data and the record, provide the insights and advisor for the user."

print("Prompting openai with:\n", user_prompt)

# call openai to get a response
openai_response = openai_client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": user_prompt}]
)

# get the response text
response_text = openai_response.choices[0].message.content

# print the response
print("OpenAI response:\n", response_text)


app = Flask(__name__)
bootstrap = Bootstrap4(app)


@app.route('/')
def homePage():
    return render_template('index.html', title="Home", response_text = response_text)

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
