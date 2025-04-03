
from flask import Flask, jsonify

app = Flask(__name__)#creating the app instance

@app.route('/name')
def get_name():
    return "<h1> hawezi</h1>"
     
    return app 
