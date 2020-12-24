# import Flask and SQLAlchemy
import matplotlib as mpl
from matplotlib.figure import Figure
# mpl.use('Agg')
from flask import Flask, render_template, request, redirect, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import folium
from folium import plugins
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import geojsoncontour
# reset matplotlib so it doesn't open popups


# Longitude
xcords = (-125, -60)
HORZ_DIMS = 175
# Latitude
ycords = (25, 50)
VERT_DIMS = 100
# start coords
start_coords = (39.8, -98.6)
# generate lists of sample points
lat_vals= np.arange(ycords[0], ycords[1], (ycords[1]-ycords[0])/VERT_DIMS)
lon_vals= np.arange(xcords[0], xcords[1], (xcords[1]-xcords[0])/HORZ_DIMS)

def display_format(data_line):
    # three empty 1D lists
    long = np.empty(shape = (HORZ_DIMS*VERT_DIMS))
    lat = np.empty(shape = (HORZ_DIMS*VERT_DIMS))
    temps = np.empty(shape = (HORZ_DIMS*VERT_DIMS))
    # assign values to list
    count = 0
    for lats in lat_vals:
        for lons in lon_vals:
            long[count] = lons
            lat[count] = lats
            temps[count] = (data_line[count])
            count += 1
    print(temps[1200:1230])
    return long,lat,temps

def gen_folium_map(longitude, latitude, data_line):
    print("2nd long shape " + str(np.shape(longitude)))
    print("2nd lat shape " + str(np.shape(latitude)))
    print("2nd temp shape " + str(np.shape(data_line)))
    print(longitude[1200:1230])
    print(latitude[1200:1230])
    print(data_line[1200:1230])
    print(np.sum(data_line))
    for dp in data_line:
        print(dp)
    # make meshes
    longmesh,latmesh = np.meshgrid(lat_vals, lon_vals)
    # make initial folium map
    folium_map = folium.Map(location=start_coords, zoom_start = 4, height = '75%')
    # make temperature mesh more dense
    print("error1")
    temp_mesh = griddata((longitude, latitude), data_line, (longmesh, latmesh), method = 'linear')
    print(np.shape(temp_mesh))
    print(np.shape(longmesh))
    print(np.shape(latmesh))
    # generate matplotlib contour plot
    print("error2")
    fig = Figure()
    ax = fig.add_subplot(111)
    temp_contour = ax.contourf(longmesh, latmesh, temp_mesh, alpha = 0.5, linestyles = 'None', vmin = 0, vmax = 100)
    # generate geojson list
    print("error3")
    temp_geojson = geojsoncontour.contourf_to_geojson(
                        contourf = temp_contour,
                        min_angle_deg = 3.0,
                        ndigits = 5,
                        stroke_width = 1,
                        fill_opacity = 0.5
                        )
    # make folium layer
    print('error4')
    folium.GeoJson(
        temp_geojson,
        style_function=lambda x: {
            'color':        x['properties']['stroke'],
            'weight':       x['properties']['stroke-width'],
            'fillColor':    x['properties']['fill'],
            'opacity':      0.6
        }).add_to(folium_map)
    return folium_map


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
    # pull one line from csv
    # three lists from csv line for lat, long, and temp
    long_data,lat_data,temp_data = display_format(data_line)

    print("1st long shape " + str(np.shape(long_data)))
    print("1st lat shape " + str(np.shape(lat_data)))
    print("1st temp shape " + str(np.shape(temp_data)))

    # generate folium map from function
    folium_map = gen_folium_map(longitude = long_data, latitude = lat_data, data_line = temp_data)

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
