# import Flask and SQLAlchemy
from flask import Flask, render_template, request, redirect, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import os

# declare app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
db = SQLAlchemy(app)

# Check if there is a header in csv file.
def Load_Data(file_name):
    data = genfromtxt(file_name, delimiter=',', skip_header=0, converters={0: lambda s: str(s)})
    return data.tolist()

Base = declarative_base()

class Weather_History(Base):
    #Tell SQLAlchemy what the table name is and if there's any table-specific arguments it should know about
    __tablename__ = 'Weather_History'
    __table_args__ = {'sqlite_autoincrement': True}
    #tell SQLAlchemy the name of column and its attributes:
    id = Column(Integer, primary_key=True, nullable=False)
    date = Column(Date)
    temp = Column(Float)

if __name__ == "__main__":
    t = time()

    #Create the database
    engine = create_engine('sqlite:///weather.db')
    Base.metadata.create_all(engine)

    #Create the session
    session = sessionmaker()
    session.configure(bind=engine)
    s = session()

    try:
        file_name = "t.csv" #sample CSV file used:
        data = Load_Data(file_name)

        for i in data:
            record = Weather_History(**{
                'date' : datetime.strptime(i[0], '%d-%b-%y').date(),
                'temp : i[1]
            })
            s.add(record) #Add all the records

        s.commit() #Attempt to commit all the records
    except:
        s.rollback() #Rollback the changes on error
    finally:
        s.close() #Close the connection


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
    ##
    #   Generate images and store them here
    ##
    actual_map_filename = os.path.join(app.config['MAPS'], 'lg_mts.jpg')
    print(actual_map_filename)
    predicted_map_filename = os.path.join(app.config['MAPS'], 'ye.png')
    print(predicted_map_filename)
    return render_template('browse.html', date = day)

# this is stand-in functionality when image generation code is added
# html image url references will be replaced from static to these

# browse images
@app.route('/browse/predicted/<string:day>/map')
def browse_pred_img(day):
    filename = 'browse-pred-map.jpg'
    return send_from_directory(app.config['MAPS'], filename)
@app.route('/browse/actual/<string:day>/map')
def browse_actual_img(day):
    filename = 'browse-actual-map.jpg'
    return send_from_directory(app.config['MAPS'], filename)
# search images
# add lookup table to properly format searched maps by state
@app.route('/search/<string:loc>/<string:day>/predicted/map')
def search_pred_img(loc, day):
    filename = 'search-pred-map.jpg'
    return send_from_directory(app.config['MAPS'], filename)
@app.route('/browse/<string:loc>/<string:day>/actual/map')
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
