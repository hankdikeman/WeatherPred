import json
import numpy
import datetime
from FlaskPage/app.py import db

# must be set before storing to the database
PREDICTIVE = True

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

if __name__ == '__main__':
    # create db file
    db.create_all()

    ##
    #   need to load in csv file here
    ##

    # iterate through lines in csv to be stored (where csv data stored in csv_file)
    for rownum in range(np.shape(csv_file)[0]):
        # collect temp data and turn to json text file
        temp_data = csv_file[rownum,:-4]
        temp_data_text = json.dumps(temp_data, cls=NumpyEncoder)
        # collect date data and store as datetime object
        line_month = csv_file[rownum,-4]
        line_day = csv_file[rownum,-3]
        line_year = csv_file[rownum,-2]
        line_date = datetime(year = line_year, month = line_month, day = line_day)
        # store in object format
        added_row = WeatherDay(date = line_date, temps = temp_data_text, predictive = PREDICTIVE)
        # add in new row
        db.session.add(added_row)
    # commit all rows to database
    db.commit()
    # print out all the rows that were added
    print(WeatherDay.query.all())