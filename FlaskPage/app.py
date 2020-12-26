# import packages
import matplotlib as mpl
mpl.use('Agg')
from matplotlib.figure import Figure
from flask import Flask, render_template, request, redirect, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import folium
import os
import numpy as np
import geojsoncontour
import json
from scipy.ndimage import gaussian_filter
import branca

# print current time for timing code throughput
def printTime(chunk):
    currTime = datetime.now().time()
    print(chunk + ": ", currTime)

# Geospatial coordinate declarations
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
# load pickled mask arrays
filter_data_mask = np.empty(shape = (VERT_DIMS,HORZ_DIMS))
with open('static/no_stations_mask.npy', 'rb') as filename:
        filter_data_mask = np.load(filename)
# load pickled statecode location dictionary
statecode_dict = np.empty(shape = (51,3))
with open('static/statecode_loc.npy', 'rb') as filename:
        statecode_dict = np.load(filename, allow_pickle = True)
statecode_dict = {code:(lat,long) for (code,lat,long) in statecode_dict[:,]}

# function to generate three 1D lists of weather data: lat, long, and temps
def display_format(data_line):
    printTime("top disp output")
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
    printTime("bot disp output")
    return long,lat,temps

# function to generate folium map with heatmap layer, takes in 1D lists of: long, lat, temps
def gen_folium_map(longitude, latitude, data_line, zoomstart = 4, startcords = start_coords, mapheight = '75%'):
    printTime("top gen folmap")
    # Setup colormap
    colors = ['#26195e', '#024c7a', '#185110', '#abdda4', '#F2F29E', '#eac5a1', '#cc7475']
    vmin = -20
    vmax = 120
    levels = [-20 + 20*x for x in range(8)]
    color_map = branca.colormap.LinearColormap(colors, vmin=vmin, vmax=vmax).to_step(len(colors))
    color_map.caption = 'Temperature (°F)'
    # make meshes of longitude and latitude values (100,175)
    longmesh,latmesh = np.meshgrid(long_vals, lat_vals)
    # make initial folium map
    folium_map = folium.Map(
                    location = startcords,
                    zoom_start = zoomstart,
                    height = '75%',
                    tiles = 'OpenStreetMap',
                    scrollWheelZoom=False
                    )
    # generate temperature mesh to match latitude and longitude meshes
    temp_mesh = np.reshape(data_line, newshape = (VERT_DIMS, HORZ_DIMS))
    # gaussian filter to smooth out data
    temp_mesh = gaussian_filter(temp_mesh * filter_data_mask, sigma=2)
    temp_mesh /= gaussian_filter(filter_data_mask, sigma=2)
    temp_mesh[np.logical_not(filter_data_mask)] = np.nan
    # generate matplotlib contour plot from lat, long, and temp meshes
    fig = Figure()
    ax = fig.add_subplot(111)
    temp_contour = ax.contourf(
                        longmesh,
                        latmesh,
                        temp_mesh,
                        levels = levels,
                        alpha = 0.7,
                        linestyles = 'None',
                        vmin = vmin, vmax = vmax,
                        colors = colors
                        )
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
    # Combine folium and color map
    folium_map.add_child(color_map)
    # return map
    printTime("bot gen folmap")
    return folium_map

def pull_db_instance(target_date, predictive):
    # query for correct date and data type (predicted/actual)
    instance = WeatherDay.query.filter(and_(
                                    WeatherDay.date == target_date,
                                    WeatherDay.predictive == predictive
                                    )).first_or_404()
    # unpack db entry and return
    temps,date = unpack_db_entry(instance)
    # return unpacked values
    return temps,date

def unpack_db_entry(instance):
    # get numpy array from json text file
    temps = np.array(json.loads(instance.temps))
    # get date from date column
    date = instance.date
    # return tuple of unpacked temperature and date
    return temps,date

# declare app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class WeatherDay(db.Model):
    id = db.Column(db.Integer, unique = True, primary_key=True)
    date = db.Column(db.DateTime, nullable = False)
    temps = db.Column(db.Text, unique=True, nullable=False)
    predictive = db.Column(db.Boolean, nullable = False)

    def __repr__(self):
        if self.predictive == True:
            return "<Pred Temps %r>" % self.date.strftime("%m/%d/%Y")
        else:
            return "<Actual Temps %r>" % self.date.strftime("%m/%d/%Y")

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
    printTime("start load")
    printTime("start open data")
    # pull line from csv and reformat to 1D (17500)
    data_line= np.genfromtxt('USTrainData1_1_2002TO9_17_2004.csv', delimiter=',')[390,:-4]
    data_line = np.reshape(data_line, newshape = (17500))
    printTime("end open data")

    # couple with latitude and longitude data, save to arrays
    long_data,lat_data,temp_data = display_format(data_line)

    # generate folium map from three arrays: longitude, latitude, and temps
    folium_map = gen_folium_map(
                        longitude = long_data,
                        latitude = lat_data,
                        data_line = temp_data
                        )
    printTime("start save map")
    # save folium map to templates folder (included in browse.html)
    folium_map.save('templates/forecastmap.html')
    printTime("end save map")
    printTime("end load")
    return render_template('forecast.html', date = day, backdate = backdate, frontdate = frontdate)

# forecast templates for iframes
@app.route('/forecast/predicted/map/img', methods = ['GET'])
def forecast_map():
    return render_template('forecastmap.html')
# browse templates for iframes
@app.route('/browse/predicted/map/img', methods = ['GET'])
def browse_pred_map():
    return render_template('pred_browsemap.html')
@app.route('/browse/actual/map/img', methods = ['GET'])
def browse_actual_map():
    return render_template('actual_browsemap.html')

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

        # parse location code and assign start coordinates
        if(loc != "USA"):
            # pull required latitude and longitude from dict
            start_lat,start_long = statecode_dict[loc]
            zoom_start = 7
        else:
            start_lat,start_long = start_coords
            zoom_start = 4

        # parse date and store in datetime object (for querying)
        selected_day = datetime.strptime(day, "%Y-%m-%d")

        ##
        #  database query goes here
        ##

        # pull two days of data from csv
        data_line = np.genfromtxt('USTrainData1_1_2002TO9_17_2004.csv', delimiter=',')[460:462,:-4]
        pred_day = np.reshape(data_line[0,:], newshape = (17500))
        actual_day = np.reshape(data_line[1,:], newshape = (17500))

        # generate longitude, latitude and temperature lists
        long_data,lat_data,pred_data = display_format(pred_day)
        __,__,actual_data = display_format(actual_day)

        # generate folium html from
        pred_map = gen_folium_map(
                        longitude = long_data,
                        latitude = lat_data,
                        data_line = pred_data,
                        mapheight = '20%',
                        zoomstart = zoom_start,
                        startcords = (start_lat,start_long)
                        )
        pred_map.save('templates/pred_browsemap.html')

        actual_map = gen_folium_map(
                        longitude = long_data,
                        latitude = lat_data,
                        data_line = actual_data,
                        mapheight = '20%',
                        zoomstart = zoom_start,
                        startcords = (start_lat,start_long)
                        )
        actual_map.save('templates/actual_browsemap.html')

        return render_template('browse.html', loc_code = loc, date = day, backdate = backdate, frontdate = frontdate)

# about page details more about webpage and us
@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == "__main__":
    app.run(debug=True)
