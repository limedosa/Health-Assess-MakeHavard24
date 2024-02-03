from flask_bootstrap import Bootstrap4
from flask import Flask, render_template

app = Flask(__name__)
bootstrap = Bootstrap4(app)


@app.route('/')
def home():
    return render_template('base.html')

if __name__ == '__main__':
    app.run(debug=True)
