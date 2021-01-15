import json
import numpy as np
from datetime import datetime
from app import db, WeatherDay, pull_db_instance, unpack_db_entry
from tensorflow.keras import models
from current_TOBS_weather_pull import current_TOBS_weather_pull


# placeholder function for deleting predicted/actual day
def delete_day(target_date, predictive):
    WeatherDay.query.filter(
        WeatherDay.date == target_date,
        WeatherDay.predictive == predictive
    ).delete()
    db.session.commit()


# function to load and return neural network for weather prediction
def load_weather_model(filename):
    # load weather model from file
    weather_model = models.load_model(filename)
    # return loaded model
    return weather_model


##
# This is a function to update the database for weather prediction data
##
if __name__ == "__main__":
    # load and store model
    filename = "models/placeholder"
    weather_model = load_weather_model(filename=filename)
    # store current date and date limits
    curr_date = datetime.now()
    back_limit = curr_date - datetime.timedelta(days=31)
    front_limit = curr_date + datetime.timedelta(days=10)

    # initialize weather prediction table
    db.create_all()

    # delete old predictions more than one day out and commit
    del_date = datetime.now()
    while del_date <= front_limit:
        delete_day(target_date=del_date, predictive=True)
        del_date = del_date + datetime.timedelta(days=1)

    # delete oldest actual data day and commit
    delete_day(target_date=back_limit, predictive=False)
    delete_day(target_date=back_limit, predictive=False)

    # pull new day of data and commit, use existing function
    current_TOBS = current_TOBS_weather_pull(curr_date)

    # predict next ten days and commit
    # use pull_db_instance and weather_model.predict for this
