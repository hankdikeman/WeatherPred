# WEATHER DATA FETCHING FUNCTION
def get_weather(locationid, datasetid, datatype, begin_date, end_date, mytoken, base_url):
    import requests
    import pandas as pd

    begin_date = begin_date.strftime("%Y-%m-%d")
    end_date = end_date.strftime("%Y-%m-%d")

    token = {'token': mytoken}
    params = 'datasetid='+str(datasetid)+'&'+'locationid='+str(locationid)+'&'+'datatypeid='\
    +str(datatype)+'&'+'startdate='+str(begin_date)+'&'+'enddate='+str(end_date)+'&'+'limit=1000'\
    +'&'+'units=standard'

    r = requests.get(base_url, params = params, headers=token)
    print("Request status code: "+str(r.status_code))

    #results comes in json form. Convert to dataframe
    df = pd.DataFrame.from_dict(r.json()['results'])
    return df