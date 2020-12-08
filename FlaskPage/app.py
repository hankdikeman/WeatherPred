# import Flask and SQLAlchemy
from flask import Flask, render_template, request, redirect, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import os

# declare app
app = Flask(__name__)

# define route to static images folder
PHOTO_FOLDER = 'maps'
app.config['MAPS'] = PHOTO_FOLDER

# the homepage that directs to browse, search, or about pages
@app.route('/')
def index():
    return render_template('index.html')

# base browse page redirects to next day by default
@app.route('/browse')
def browse_home():
    # initial browse page redirects to "tomorrow" browse page
    today = (datetime.now()+timedelta(days = 1)).strftime("%Y-%m-%d")
    return redirect('/browse/'+today)

# browse page allows users to view a map for given days
@app.route('/browse/<string:day>')
def browse(day):
    ##
    #   query database to get data for day
    ##

    ##
    #   Generate images and store them here
    #   cartopy, geoplotlib, gmplot, Folium
    ##
    return render_template('browse.html', date = day)

# this is stand-in functionality when image generation code is added
# html image url references will be replaced from static to these

# browse images
@app.route('/browse/predicted/<string:day>/map', methods = ['GET'])
def browse_pred_img(day):
    filename = 'browse-pred-map.jpg'
    return send_from_directory(app.config['MAPS'], filename)
@app.route('/browse/actual/<string:day>/map', methods = ['GET'])
def browse_actual_img(day):
    filename = 'browse-actual-map.jpg'
    return send_from_directory(app.config['MAPS'], filename)
# search images
# add lookup table to properly format searched maps by state
@app.route('/search/<string:loc>/<string:day>/predicted/map', methods = ['GET'])
def search_pred_img(loc, day):
    filename = 'search-pred-map.jpg'
    return send_from_directory(app.config['MAPS'], filename)
@app.route('/browse/<string:loc>/<string:day>/actual/map', methods = ['GET'])
def search_actual_img(loc, day):
    filename = 'search-actual-map.jpg'
    return send_from_directory(app.config['MAPS'], filename)

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
    ##
    #   query database to get data for loc and day
    ##

    ##
    #   generate images using image library
    #   cartopy, geoplotlib, gmplot, Folium
    ##
    return render_template('search-results.html', loc_code = loc, date = day)

# about page details more about webpage and us
@app.route('/about')
def about():
    return render_template('about.html')

def pullWeatherData():
    # placeholder function to query NOAA and push days data to database
    # also removes data from one year ago
    return 0

if __name__ == "__main__":
    app.run(debug=True)
