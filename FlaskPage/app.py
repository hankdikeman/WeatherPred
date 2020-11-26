# import Flask and SQLAlchemy
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

# declare app
app = Flask(__name__)

# the homepage that directs to browse, search, or about pages
@app.route('/')
def index():
    return render_template('index.html')

# browse page allows users to view a map for given days
@app.route('/browse')
def browse():
    return 0

# search page allows searching by location, gives tabulated data
@app.route('/search')
def search():
    return 0

# about page details more about webpage and us
@app.route('/about')
def about():
    return 0
