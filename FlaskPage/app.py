# import Flask and SQLAlchemy
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import os

# declare app
app = Flask(__name__)

# define route to static images folder
PHOTO_FOLDER = 'testpics'
app.config['MAPS'] = PHOTO_FOLDER

# the homepage that directs to browse, search, or about pages
@app.route('/')
def index():
    return render_template('index.html')

# base browse page redirects to next day by default
@app.route('/browse')
def browse_home():
    # initial browse page redirects to "tomorrow" browse page
    today = (datetime.now()+timedelta(days = 1)).strftime("%m%d%Y")
    return redirect('/browse/'+today)

# browse page allows users to view a map for given days
@app.route('/browse/<string:day>')
def browse(day):
    actual_map_filename = os.path.join(app.config['MAPS'], 'lg_mts.jpg')
    print(actual_map_filename)
    predicted_map_filename = os.path.join(app.config['MAPS'], 'ye.png')
    print(predicted_map_filename)
    return render_template('browse.html', actual_map_img = actual_map_filename, predicted_map_img = predicted_map_filename)

# this is stand-in functionality when image generation code is added
# html image url references will be replaced from static to these

# browse images
@app.route('/browse/predicted/<string:day>/map')
def browse_pred_img(day):
    return 0
@app.route('/browse/actual/<string:day>/map')
def browse_actual_img(day):
    return 0
# search images
@app.route('/search/<string:loc>/<string:day>/predicted/map')
def search_pred_img(loc, day):
    return 0
@app.route('/browse/actual/<string:day>/actual/map')
def search_actual_img(loc, day):
    return 0

# search page allows searching by location, gives tabulated data
@app.route('/search', methods = ['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_day = request.form['search-date']
        search_loc = request.form['search-loc']
        return redirect('/search/'+str(search_loc)+'/'+str(search_day))
    else:
        return render_template('search.html')

# location result given from location search, loc will likely be state number
@app.route('/search/<string:loc>/<string:day>')
def loc_result(loc, day):
    actual_map_filename = os.path.join(app.config['MAPS'], 'ye.png')
    print(actual_map_filename)
    predicted_map_filename = os.path.join(app.config['MAPS'], 'ye.png')
    print(predicted_map_filename)
    return render_template('search-results.html', loc_code = loc, date = day, actual_map_img = actual_map_filename, predicted_map_img = predicted_map_filename)

# about page details more about webpage and us
@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == "__main__":
    app.run(debug=True)
