# import Flask and SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for
import os
from os.path import join, dirname, realpath
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# declare app
app = Flask(__name__)
# define database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

class WeatherPred(db.Model):
    id = db.Column(db.Area, primary_key=True)
    temp = db.Column(db.Integer, nullable=False)
    date= db.Column(db.DataTime, nullable=False, default='N/A')
    pressure = db.Column(db.Double, nullable=True)
    windSpeed = db.Column(db.Integer, nullable=True)
    WindDirection = db.Column(db.String(20), nullable=True)

# Upload folder
UPLOAD_FOLDER = 'static/files'
app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER

# Root URL
@app.route('/')
def index():
     # Set The upload HTML template '\templates\csvUpload.html'
    return render_template('csvUpload.html')


# Get the uploaded files
@app.route("/", methods=['POST'])
def uploadFiles():
      # get the uploaded file
      uploaded_file = request.files['file']
      if uploaded_file.filename != '':
           file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
          # set the file path
           uploaded_file.save(file_path)
          # save the file
      return redirect(url_for('index'))

# the homepage that directs to browse, search, or about pages
@app.route('/')
def index():
    return render_template('index.html')

# browse page allows users to view a map for given days
@app.route('/browse')
def browse():
    return render_template('browse.html')

# search page allows searching by location, gives tabulated data
@app.route('/search')
def search():
    return render_template('search.html')

# location result given from location search
@app.route('/search/<string:loc>/<string:day>')
def loc_result(loc):
    ##
    # get map from db for search parameters
    ##
    return render_template('search.html', location_map = search_loc)

# about page details more about webpage and us
@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == "__main__":
    app.run(debug=True)
