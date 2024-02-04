from flask_bootstrap import Bootstrap4
from flask import Flask, render_template, request
from openai import OpenAI
import os

OPENAI_API_KEY='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'
openai_client = OpenAI(api_key=OPENAI_API_KEY)

# construct a prompt
user_prompt = f"You are a health assessment assistant. Given the the heartbeat data: 70 bmp and the records, provide insights and advise for the user in the format: x beats per minute falls within (normal/not normal date), average heart rate for people in age range given, advice:"

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


######### for the healthy meal + ingredients + average cost

recipe_prompt = f"Give me a healthy meal idea reccomendation along with the ingredients and average cost in USD."

print("Prompting recipe with openai:\n", recipe_prompt, type(recipe_prompt))

# call openai to get a response
openai_response_recipe = openai_client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": recipe_prompt}]
)

# get the response text
response_text_recipe = openai_response_recipe.choices[0].message.content


print("OpenAI response for recipes:)\n", response_text_recipe)

app = Flask(__name__)
bootstrap = Bootstrap4(app)

@app.route('/')
def homePage():
    return render_template('index.html', title="Home", response_text = response_text, response_text_recipe=response_text_recipe)


@app.route("/newInputs", methods=['GET'])
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
