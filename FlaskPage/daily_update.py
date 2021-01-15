import json
import numpy as np
from datetime import datetime
from app import db, WeatherDay, pull_db_instance, unpack_db_entry
from tensorflow.keras import models
from current_TOBS_weather_pull import current_TOBS_weather_pull

LONG_DIMS = 175
LAT_DIMS = 100
MODEL_DAY_NUM = 7


# redimensionalize output of model
def redimensionalize_output(output_array):
    return output_array


# nondimensionalize input of model
def nondimensionalize_input(input_array):
    return input_array


# delete targeted day
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


def check_exists(target_date, predictive):
    return db.session.query(WeatherDay.id).filter(
        WeatherDay.date == target_date,
        WeatherDay.predictive == predictive).scalar() is not None


# encoder class for numpy files
class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


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
    pull_date = curr_date - datetime.timedelta(days=30)
    while pull_date < datetime.now():
        # query the date in question
        actual_data_exists = check_exists(
            target_date=pull_date, predictive=False)
        if(not actual_data_exists):
            # pull new day of data
            current_TOBS = current_TOBS_weather_pull(curr_date)
            new_day_pull = json.dumps(current_TOBS[:-3], cls=NumpyEncoder)
            # create new WeatherDay object
            new_data_row = WeatherDay(
                date=pull_date, temps=new_day_pull, predictive=False)
            # add in new row
            db.session.add(new_data_row)
            # commit all rows to database
            db.session.commit()
        pull_date += datetime.timedelta(days=1)

    # set back limit for temperature data to be pulled
    query_date = curr_date - datetime.timedelta(days=21)
    array_index = 0
    # create empty 2D array for temperature data
    unformatted_temp_data = np.empty(
        shape=((front_limit - pull_date, LONG_DIMS * LAT_DIMS)))
    # loop through range of days and store any actual days of data
    while query_date < front_limit:
        # pull actual data if it exists
        if check_exists(target_date=query_date, predictive=False):
            unformatted_temp_data[array_index, :] = np.reshape(pull_db_instance(
                target_date=query_date, predictive=False), newshape=(1, LONG_DIMS * LAT_DIMS))
        # make new predictions if there is enough days to make new predictions
        if array_index >= MODEL_DAY_NUM:
            # generate new prediction inputs from existing data in unformatted_temp_data
            model_inputs = np.reshape(
                unformatted_temp_data[array_index - MODEL_DAY_NUM:array_index, :], newshape=(1, MODEL_DAY_NUM, LONG_DIMS * LAT_DIMS))
            # nondimensionalize model inputs to fit requirements of model
            model_inputs = nondimensionalize_input(model_inputs)
            # generate new prediction from number of days of existing data
            new_prediction = np.reshape(weather_model.predict(
                model_inputs)[0, :], newshape=(LONG_DIMS, LAT_DIMS))
            # redimensionalize outputs of predictive model
            new_prediction_temps = redimensionalize_output(new_prediction)
            # encode prediction in JSON file
            encoded_new_prediction = json.dumps(
                new_prediction, cls=NumpyEncoder)
            # generate new WeatherDay object with existing data
            new_predicted_row = WeatherDay(
                date=query_date, temps=encoded_new_prediction, predictive=True)
            # add in new predicted row
            db.session.add(new_predicted_row)
            # commit all rows to database
            db.session.commit()

        # otherwise pull existing data
        elif check_exists(target_date=query_date, predictive=True):
            unformatted_temp_data[array_index, :] = np.reshape(pull_db_instance(
                target_date=query_date, predictive=True), newshape=(1, LONG_DIMS * LAT_DIMS))
        query_date += datetime.timedelta(days=1)
        array_index += 1

    # pull together data for predictions
    formatted_xdata = np.empty(shape=(sample_ind, day_num, x_nodes * y_nodes))
    # loop through all days minus day_num allocation
    for ind in range(sample_ind):
        # reshape "day_num" section to shape required for x output
        sample = np.reshape(
            rawdata[ind:ind + day_num, :], newshape=(1, day_num, long_nodes * lat_nodes))
        # store x input values in formatted data
        formatted_xdata[ind, :, :] = sample
    # predict next ten days and commit

    # use pull_db_instance and weather_model.predict for this
