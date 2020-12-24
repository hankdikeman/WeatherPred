# import Flask and SQLAlchemy
import matplotlib as mpl
from matplotlib.figure import Figure
mpl.use('Agg')
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
long_vals= np.arange(xcords[0], xcords[1], (xcords[1]-xcords[0])/HORZ_DIMS)

# function to generate three 1D lists of weather data: lat, long, and temps
def display_format(data_line):
    # three empty 1D lists
    long = np.empty(shape = (HORZ_DIMS*VERT_DIMS))
    lat = np.empty(shape = (HORZ_DIMS*VERT_DIMS))
    temps = np.empty(shape = (HORZ_DIMS*VERT_DIMS))
    # assign values to list (lat, long, and temp)
    count = 0
    for lats in lat_vals:
        for lons in long_vals:
            long[count] = lons
            lat[count] = lats
            temps[count] = (data_line[count])
            count += 1
    # return collected values
    return long,lat,temps

# function to generate folium map with heatmap layer, takes in 1D lists of: long, lat, temps
def gen_folium_map(longitude, latitude, data_line):
    # make meshes of longitude and latitude values (100,175)
    longmesh,latmesh = np.meshgrid(long_vals, lat_vals)
    # make initial folium map
    folium_map = folium.Map(location = start_coords, zoom_start = 4, height = '75%')
    # generate temperature mesh to match latitude and longitude meshes
    temp_mesh = np.reshape(data_line, newshape = (VERT_DIMS, HORZ_DIMS))
    # temp_mesh = griddata((longitude, latitude), data_line, (longmesh, latmesh), method = 'linear')
    # generate matplotlib contour plot from lat, long, and temp meshes
    fig = Figure()
    ax = fig.add_subplot(111)
    temp_contour = ax.contourf(longmesh, latmesh, temp_mesh, alpha = 0.7, linestyles = 'None', vmin = 0, vmax = 100)
    # generate geojson data from contour plot
    temp_geojson = geojsoncontour.contourf_to_geojson(
                        contourf = temp_contour,
                        min_angle_deg = 3.0,
                        ndigits = 5,
                        stroke_width = 1,
                        fill_opacity = 0.5
                        )
    # generate folium chloropleth and add to previously created map
    folium.GeoJson(
        temp_geojson,
        style_function=lambda x: {
            'color':        x['properties']['stroke'],
            'weight':       x['properties']['stroke-width'],
            'fillColor':    x['properties']['fill'],
            'opacity':      0.6
        }).add_to(folium_map)
    # return map
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

    # pull line from csv and reformat to 1D (17500)
    data_line= np.genfromtxt('USTrainData1_1_2002TO9_17_2004.csv', delimiter=',')[100,:-4]
    data_line = np.reshape(data_line, newshape = (17500))

    # couple with latitude and longitude data, save to arrays
    long_data,lat_data,temp_data = display_format(data_line)

    # generate folium map from three arrays: longitude, latitude, and temps
    folium_map = gen_folium_map(longitude = long_data, latitude = lat_data, data_line = temp_data)

    # save folium map to templates folder (included in browse.html)
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
