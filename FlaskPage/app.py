# import Flask and SQLAlchemy
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

# declare app
app = Flask(__name__)
# define database
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
#db = SQLAlchemy(app)

#class WeatherPred(db.Model):
#    mode = db.Column(db.Integer, nullable=False)
#    temps = db.Column(db.Integer, nullable=False)
#    date = db.Column(db.DateTime, nullable=False)



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
    ##
    #  get weather data for day requested
    ##

    ##
    #   generate csv or image
    ##
    return render_template('browse.html')

# search page allows searching by location, gives tabulated data
@app.route('/search')
def search():
    return render_template('search.html')

# location result given from location search, loc will likely be state number
@app.route('/search/<string:loc>/<string:day>')
def loc_result(loc, day):
    ##
    #   get map from db for search parameters, loc and string
    ##
    return render_template('search.html', location_map = search_loc)

# about page details more about webpage and us
@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == "__main__":
    app.run(debug=True)
