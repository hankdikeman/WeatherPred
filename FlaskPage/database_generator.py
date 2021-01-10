import json
import numpy as np
from datetime import datetime
from app import db, WeatherDay

# must be set before storing to the database
PREDICTIVE = False


# encoder class for numpy files
class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


if __name__ == '__main__':
    # create db file
    db.create_all()

    csv_file = np.genfromtxt('db_populate122820.csv', delimiter=',')[:, :-1]

    # iterate through lines in csv to be stored (where csv data stored in csv_file)
    for rownum in range(np.shape(csv_file)[0]):
        # collect temp data and turn to json text file
        temp_data = csv_file[rownum, :-3]
        temp_data_text = json.dumps(temp_data, cls=NumpyEncoder)
        # collect date data and store as datetime object
        line_month = csv_file[rownum, -2]
        line_day = csv_file[rownum, -1]
        line_year = csv_file[rownum, -3]
        line_date = datetime(year=int(line_year), month=int(
            line_month), day=int(line_day))
        # store in object format
        added_row = WeatherDay(
            date=line_date, temps=temp_data_text, predictive=PREDICTIVE)
        # add in new row
        db.session.add(added_row)
        # commit all rows to database
        db.session.commit()
    # print out all the rows that were added
    print(WeatherDay.query.all())
