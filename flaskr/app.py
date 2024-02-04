from flask_bootstrap import Bootstrap
from flask import Flask, render_template, request
from openai import OpenAI
import os
# from pyserial import serial
import time
import threading
from datetime import datetime
from flask import Flask, render_template
import random
from datetime import datetime, timedelta
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from flask_bootstrap import Bootstrap
from flask import Flask, render_template, request
from openai import OpenAI
import os
import serial
import time
import json




openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# construct a prompt
user_prompt = f"You are a health assessment assistant. Given the the heartbeat data: 70 bmp and the records, provide insights and advise for the user in the format: x beats per minute falls within (normal/not normal date), average heart rate for people in age range given, advice:"

print("Prompting openai with:\n", user_prompt)

# buffer

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

######### read data from sensor

# Establish a connection to the serial port.
# Your serial connection setup

ser = serial.Serial('/dev/cu.usbmodem11301', 9600, timeout=1)

data_buffer = []  # Initialize your data buffer

def read_from_serial():
    time.sleep(2)  # wait for the serial connection to initialize
    while True:
        try:
            if ser.in_waiting > 0:
                data = ser.readline().decode('utf-8').rstrip()
                data_json = {
                    "value": int(data),
                    "timestamp": datetime.now().timestamp()
                }
                data_buffer.append(data_json)
                # if there is data, write it to a .json file
                
                with open('./static/new_data.jsonl','w') as f:
                    for index, entry in enumerate(data_buffer):
                        json.dump(entry, f)
                        f.write('\n')
                        print(data_json)  # Print the data received from Arduino

                        if index > 20:
                            break
        except:
            pass
            


# Start the serial reading in a background thread
thread = threading.Thread(target=read_from_serial)
thread.daemon = True  # Daemonize thread
thread.start()



app = Flask(__name__)

def generate_data():
    # Generate sample data
    num_entries = 10
    start_time = datetime(2024, 2, 3, 8, 0, 0)  # Start time
    end_time = datetime(2024, 2, 3, 9, 0, 0)     # End time

    # Generate random timestamp and heart rate data
    data = []
    for _ in range(num_entries):
        # Generate random timestamp within the given time range
        timestamp = start_time + timedelta(minutes=random.randint(0, 60))
        
        # Generate random heart rate between 60 and 120 bpm
        heart_rate = random.randint(60, 120)
        
        # Append timestamp and heart rate to the data list
        data.append((timestamp, heart_rate))

    # Create a dictionary out of the data
    dictNums = {}
    for entry in data:
        # Convert the timestamp to the desired string format
        timestamp_str = entry[0].strftime("%Y-%m-%d %H:%M:%S")
        # Assign the formatted timestamp as the key and the heart rate as the value to the dictionary
        dictNums[timestamp_str] = entry[1]

    # Create a DataFrame from the dictionary
    df = pd.DataFrame(list(dictNums.items()), columns=['time', 'rate'])
    return df


def json_file_to_dict(file_path):
    """
    Convert a JSON file containing data in the format:
    {"value": value, "timestamp": timestamp}
    into a dictionary where timestamps are keys and values are values.

    Parameters:
    - file_path (str): The path to the JSON file.

    Returns:
    - dict: A dictionary where timestamps are keys and values are values.
    """
    # Initialize an empty dictionary
    data_dict = {}

    # Open the JSON file for reading
    with open('./static/new_data.jsonl', 'r') as file:
        # Iterate over each line in the file
        for line in file:
            # Parse the JSON object from the line
            data = json.loads(line)

            # Extract the value and timestamp from the parsed JSON object
            value = data['value']
            timestamp = data['timestamp']

            # Add the value to the dictionary with its timestamp as the key
            data_dict[timestamp] = value

    return data_dict

# file_path = 'static\data.jsonl'  # Update with your file path
result_dict = json_file_to_dict(data_buffer)
print(result_dict)


def dataParser(data):
    """parses data in the form: 
    {“value”: 70, “timestamp”: “2024-02-04T02:30:58.590377”}

    Args:
        data (dict): heartrate, timestamp

    Returns:
        _type_: _description_
    """
    listHeartRate = [num for num in data.keys()]
    listTimeStamps = [time for time in data.values()]
    return [listTimeStamps, listHeartRate]

def averageHeartRate(listHeartRate):
    """gives average heart rate given a list of heart rates
    Args:
        listHeartRate (list): _description_
    Returns:
        num: average
    """
    # listHeartRate=[int(num) for num in listHeartRate]
    if len(listHeartRate)>0:
        return sum(listHeartRate)/len(listHeartRate)
    else:
        pass

testingRate = averageHeartRate([2,2,2,2,2])


parsedData = dataParser(result_dict)
# print(parsedData)
listHeartRate= parsedData[0]
listTimeStamps =parsedData[1]
averageHeartRateNonStatic = averageHeartRate(listHeartRate) 
print("AVERAGE HEART RATE :)", averageHeartRateNonStatic)
openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
# construct a prompt
user_prompt = f"You are a health assessment assistant. Given the the heartbeat data: {averageHeartRateNonStatic} bmp and the records, provide insights and advise for the user in the format: x beats per minute falls within (normal/not normal date), average heart rate for people in age range given, advice:"

print("Promp:\n", user_prompt)

# call openai to get a response
openai_response = openai_client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": user_prompt}]
)

# get the response text
responseInputAnalysis = openai_response.choices[0].message.content

# print the response
print("OpenAI response:\n", responseInputAnalysis)


app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route('/')
def homePage():
    return render_template('index.html', title="Home", response_text = response_text)


@app.route("/newInputs", methods=['GET'])
def newInputsPage():
    # print("data_buffer:")
    # print(data_buffer)

    import matplotlib as mpl
    mpl.use('Agg')
    import matplotlib.pyplot as plt
    import seaborn as sns
    import pandas as pd

    df = pd.DataFrame(list(result_dict.items()), columns=['timestamp', 'value'])

    # Plot graph
    sns.lineplot(data=df, x=listTimeStamps, y=listHeartRate)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.xlabel('Time')
    plt.ylabel('Heart Rate')
    plt.title('Heart Rate Over Time')
    plt.savefig('static/graph.png')  # Save the graph as a static file
    plt.close()

    return render_template("newInputs.html", title="New Input", data_buffer=data_buffer,responseInputAnalysis=responseInputAnalysis)

@app.route("/records")
def recordsPage():
    return render_template("records.html", title="Records", response_text=response_text)

@app.route("/recommendations")
def recommendationsPage():
    return render_template("recommendations.html", title="Recommendations",  response_text_recipe=response_text_recipe)

if __name__ == '__main__':
    app.run(debug=True)
