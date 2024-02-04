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
    return listHeartRate, listTimeStamps

def averageHeartRate(listHeartRate):
    """gives average heart rate given a list of heart rates
    Args:
        listHeartRate (list): _description_
    Returns:
        num: average
    """
    return sum(listHeartRate)/len(listHeartRate)

testingRate = averageHeartRate([2,4,6,8,10])

openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# construct a prompt
user_prompt = f"You are a health assessment assistant. Given the the heartbeat data: {testingRate} bmp and the records, provide insights and advise for the user in the format: x beats per minute falls within (normal/not normal date), average heart rate for people in age range given, advice:"

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


@app.route('/')
def index():
    # Generate data
    df = generate_data()

    # Plot graph
    sns.lineplot(data=df, x='time', y='rate')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.xlabel('Time')
    plt.ylabel('Heart Rate')
    plt.title('Heart Rate Over Time')
    plt.savefig('static/graph.png')  # Save the graph as a static file
    plt.close()

    # Render the template with the graph
    return render_template('index.html', responseInputAnalysis=responseInputAnalysis)

if __name__ == '__main__':
    app.run(debug=True)
