from flask_bootstrap import Bootstrap
from flask import Flask, render_template, request
from openai import OpenAI
import os
import serial
import time
import threading

from datetime import datetime


openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# construct a prompt
user_prompt = f"You are a health assessment assistant. Given the the heartbeat data: 70 bmp and the records, provide insights and advise for the user in the format: x beats per minute falls within (normal/not normal date), average heart rate for people in age range given, advice:"

print("Prompting openai with:\n", user_prompt)

# buffer

# # call openai to get a response
# openai_response = openai_client.chat.completions.create(
#     model="gpt-4",
#     messages=[{"role": "user", "content": user_prompt}]
# )

# # get the response text
# response_text = openai_response.choices[0].message.content

# # print the response
# print("OpenAI response:\n", response_text)


# ######### for the healthy meal + ingredients + average cost

# recipe_prompt = f"Give me a healthy meal idea reccomendation along with the ingredients and average cost in USD."

# print("Prompting recipe with openai:\n", recipe_prompt, type(recipe_prompt))

# # call openai to get a response
# openai_response_recipe = openai_client.chat.completions.create(
#     model="gpt-4",
#     messages=[{"role": "user", "content": recipe_prompt}]
# )

# # get the response text
# response_text_recipe = openai_response_recipe.choices[0].message.content


# print("OpenAI response for recipes:)\n", response_text_recipe)

######### read data from sensor

# Establish a connection to the serial port.
# Your serial connection setup
ser = serial.Serial('/dev/cu.usbmodem11301', 9600, timeout=1)

data_buffer = []  # Initialize your data buffer

def read_from_serial():
    time.sleep(2)  # wait for the serial connection to initialize
    while True:
        if ser.in_waiting > 0:
            data = ser.readline().decode('utf-8').rstrip()
            data_json = {
                "value": data,
                "timestamp": datetime.now().timestamp()
            }
            data_buffer.append(data_json)
            print(data_json)  # Print the data received from Arduino

# Start the serial reading in a background thread
thread = threading.Thread(target=read_from_serial)
thread.daemon = True  # Daemonize thread
thread.start()

app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route('/')
def homePage():
    return render_template('index.html', title="Home", response_text = response_text)


@app.route("/newInputs", methods=['GET'])
def newInputsPage():
    print("data_buffer:")
    print(data_buffer)
    return render_template("newInputs.html", title="New Input", data_buffer=data_buffer)

@app.route("/records")
def recordsPage():
    return render_template("records.html", title="Records", response_text=response_text)

@app.route("/recommendations")
def recommendationsPage():
    return render_template("recommendations.html", title="Recommendations",  response_text_recipe=response_text_recipe)

if __name__ == '__main__':
    app.run(debug=True)
