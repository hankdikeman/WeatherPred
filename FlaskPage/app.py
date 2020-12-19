# import Flask and SQLAlchemy
from flask import Flask, render_template, request, redirect, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import folium
import os

# declare app
app = Flask(__name__)

# define route to static images folder
PHOTO_FOLDER = 'maps'
app.config['MAPS'] = PHOTO_FOLDER

@app.route('/')
def base_redirect():
    return redirect('/forecast')

# the homepage that directs to browse, search, or about pages
@app.route('/navigate')
def index():
    return render_template('index.html')

# base browse page redirects to next day by default
@app.route('/forecast')
def forecast():
    # initial browse page redirects to "tomorrow" browse page
    today = (datetime.now()+timedelta(days = 1)).strftime("%Y-%m-%d")
    return redirect('/forecast/'+today)

# browse page allows users to view a map for given days
@app.route('/forecast/<string:day>')
def browse(day):
    backdate = (datetime.now()-timedelta(days = 2)).strftime("%Y-%m-%d")
    frontdate = (datetime.now()+timedelta(days = 10)).strftime("%Y-%m-%d")
    ##
    #   query database to get data for day
    ##

    start_coords = (46.9540700, 142.7360300)
    folium_map = folium.Map(location=start_coords, zoom_start=14, height = '75%')
    folium_map.save('templates/forecastmap.html')

    return render_template('forecast.html', date = day, backdate = backdate, frontdate = frontdate)

# this is stand-in functionality when image generation code is added
# html image url references will be replaced from static to these

# forecast images
@app.route('/forecast/predicted/<string:day>/map', methods = ['GET'])
def forecast_img(day):
    filename = 'forecast_disp_map.jpg'
    print("getting img for forecast")
    return send_from_directory(app.config['MAPS'], filename)
# search images
# add lookup table to properly format searched maps by state
@app.route('/browse/<string:loc>/<string:day>/predicted/map', methods = ['GET'])
def browse_pred_img(loc, day):
    print("pred " + loc + " "+ day)
    filename = 'browse-pred-map.jpg'
    return send_from_directory(app.config['MAPS'], filename)
@app.route('/browse/<string:loc>/<string:day>/actual/map', methods = ['GET'])
def browse_actual_img(loc, day):
    print("actual " + loc + " "+ day)
    filename = 'browse-actual-map.jpg'
    return send_from_directory(app.config['MAPS'], filename)

# search page allows searching by location, gives tabulated data
@app.route('/browse')
def search():
    today = datetime.now().strftime("%Y-%m-%d")
    return redirect('/browse/USA/'+str(today))

# location result given from location search, loc will likely be state number
@app.route('/browse/<string:loc>/<string:day>', methods = ['GET', 'POST'])
def loc_result(loc, day):
    if request.method == 'POST':
        search_day = request.form['search-date']
        search_loc = request.form['search-loc']
        print(str(200))
        return redirect('/browse/'+str(search_loc)+'/'+str(search_day))
    else:
        backdate = (datetime.now()-timedelta(days = 30)).strftime("%Y-%m-%d")
        frontdate = (datetime.now()+timedelta(days = 10)).strftime("%Y-%m-%d")
        ##
        #   query database to get data for loc and day
        ##

        ##
        #   generate images using image library
        #   cartopy, geoplotlib, gmplot, Folium
        ##
        return render_template('browse.html', loc_code = loc, date = day, backdate = backdate, frontdate = frontdate)

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
