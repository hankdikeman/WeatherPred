# import packages
from flask import Flask, render_template, request, redirect, abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import numpy as np
import json
import os
import heatmap_utils


# print current time for timing code throughput
def printTime(chunk):
    currTime = datetime.now().time()
    print(chunk + ": ", currTime)


# load pickled statecode location dictionary
statecode_dict = np.empty(shape=(51, 3))
with open('static/statecode_loc.npy', 'rb') as filename:
    statecode_dict = np.load(filename, allow_pickle=True)
statecode_dict = {code: (lat, long)
                  for (code, lat, long) in statecode_dict[:, ]}


# pull database instance based on date and predictive flag
def pull_db_instance(target_date, predictive):
    # query for correct date and data type (predicted/actual)
    instance = WeatherDay.query.filter(
        (WeatherDay.date == target_date) and
        (WeatherDay.predictive == predictive)
    ).first()
    if(instance):
        # unpack db entry and return
        temps, date = unpack_db_entry(instance)
        # return unpacked values
        return temps
    else:
        return "null"


# parse json text and convert to temperatures, pull ate
def unpack_db_entry(instance):
    # get numpy array from json text file
    temps = np.array(json.loads(instance.temps))
    # get date from date column
    date = instance.date
    # return tuple of unpacked temperature and date
    return temps, date


# declare app
app = Flask(__name__)
# set database path
db_path = os.path.join(os.path.dirname(__file__), 'weatherdata.db')
db_uri = 'sqlite:///{}'.format(db_path)
# set app config for database
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# weather data class for database
class WeatherDay(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    temps = db.Column(db.Text, nullable=False)
    predictive = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        if self.predictive:
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
    today = datetime.now().strftime("%Y-%m-%d")
    return redirect('/forecast/' + today)


# browse page allows users to view a map for given days
@app.route('/forecast/<string:day>')
def browse(day):
    # get front and backdate for slider
    backdate = (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d")
    frontdate = (datetime.now() + timedelta(days=10)).strftime("%Y-%m-%d")

    # strip date string and convert to datetime object
    try:
        selected_day = datetime.strptime(day, "%Y-%m-%d")
    except ValueError:
        abort(400)

    # store temperature data from database to file
    pulled_data = pull_db_instance(target_date=selected_day, predictive=False)

    # check to see if non-null data was pulled upon request
    if(not(isinstance(pulled_data, str))):
        data_line = np.reshape(pulled_data, newshape=(17500))

        # couple with latitude and longitude data, save to arrays
        long_data, lat_data, temp_data = heatmap_utils.display_format(
            data_line)

        # generate folium map from three arrays: longitude, latitude, and temps
        folium_map = heatmap_utils.gen_folium_map(
            longitude=long_data,
            latitude=lat_data,
            data_line=temp_data,
            mapheight='100%'
        )
        # save folium map to templates folder (included in browse.html)
        folium_map.save('templates/forecastmap.html')
        return render_template('forecast.html', date=day, backdate=backdate, frontdate=frontdate)

    # if no valid data was pulled then render "no data" document
    else:
        with open('templates/forecastmap.html', 'w') as filename:
            filename.write(
                f"<p style='text-align:center;'>No data for {day}</p>")
        return render_template('forecast.html', date=day, backdate=backdate, frontdate=frontdate)


# forecast templates for iframes
@app.route('/forecast/predicted/map/img', methods=['GET'])
def forecast_map():
    return render_template('forecastmap.html')


# browse templates for iframes
@app.route('/browse/predicted/map/img', methods=['GET'])
def browse_pred_map():
    return render_template('pred_browsemap.html')


# browse templates for iframes
@app.route('/browse/actual/map/img', methods=['GET'])
def browse_actual_map():
    return render_template('actual_browsemap.html')


# search page allows searching by location, gives tabulated data
@app.route('/browse')
def search():
    today = datetime.now().strftime("%Y-%m-%d")
    return redirect('/browse/USA/' + str(today))


# location result given from location search, loc will likely be state number
@app.route('/browse/<string:loc>/<string:day>', methods=['GET', 'POST'])
def loc_result(loc, day):
    if request.method == 'POST':
        search_day = request.form['search-date']
        search_loc = request.form['search-loc']
        return redirect('/browse/' + str(search_loc) + '/' + str(search_day))
    else:
        # set front and backdate
        backdate = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        frontdate = (datetime.now() + timedelta(days=10)).strftime("%Y-%m-%d")

        # parse location code and assign start coordinates
        if(loc != "USA"):
            # pull required latitude and longitude from dict
            start_lat, start_long = statecode_dict[loc]
            zoom_start = 7
        else:
            start_lat, start_long = (39.8, -98.6)
            zoom_start = 4

        # strip date string and convert to datetime object
        try:
            selected_day = datetime.strptime(day, "%Y-%m-%d")
        except ValueError:
            abort(400)

        # pull and store temperature data from database
        pulled_data = pull_db_instance(
            target_date=selected_day, predictive=False)

        # if non null data was pulled from database then render maps
        if(not(isinstance(pulled_data, str))):
            # pull two days of data from csv
            pred_day = np.reshape(pulled_data, newshape=(17500))
            actual_day = np.reshape(pulled_data, newshape=(17500))

            # generate longitude, latitude and temperature lists
            long_data, lat_data, pred_data = heatmap_utils.display_format(
                pred_day)
            __, __, actual_data = heatmap_utils.display_format(actual_day)

            # generate folium html file for predicted map
            pred_map = heatmap_utils.gen_folium_map(
                longitude=long_data,
                latitude=lat_data,
                data_line=pred_data,
                mapheight='100%',
                zoomstart=zoom_start,
                startcords=(start_lat, start_long)
            )
            pred_map.save('templates/pred_browsemap.html')

            # generate actual temperature data map from database pull
            actual_map = heatmap_utils.gen_folium_map(
                longitude=long_data,
                latitude=lat_data,
                data_line=actual_data,
                mapheight='100%',
                zoomstart=zoom_start,
                startcords=(start_lat, start_long)
            )
            actual_map.save('templates/actual_browsemap.html')

            return render_template('browse.html', loc_code=loc, date=day, backdate=backdate, frontdate=frontdate)
        else:
            with open('templates/actual_browsemap.html', 'w') as filename:
                filename.write(
                    f"<p style='text-align:center;'>No data for {day}</p>")
            with open('templates/pred_browsemap.html', 'w') as filename:
                filename.write(
                    f"<p style='text-align:center;'>No data for {day}</p>")
            return render_template('browse.html', loc_code=loc, date=day, backdate=backdate, frontdate=frontdate)


# about page details more about webpage and us
@app.route('/about')
def about():
    return render_template('about.html')


# invalid url field error handler
@app.errorhandler(400)
def invalid_date(e):
    return render_template('invalid_field.html'), 400


# invalid URL address error handler
@app.errorhandler(404)
def invalid_page(e):
    return render_template('page_not_found.html'), 404


if __name__ == "__main__":
    app.run(debug=True)
