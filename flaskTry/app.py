from flask import Flask, render_template
import random
from datetime import datetime, timedelta
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

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
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
