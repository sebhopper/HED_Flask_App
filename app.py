import os
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/index')
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, port=os.getenv("PORT", default=5000))
