def get_station_info(locationid, datasetid, mytoken, base_url):
  import requests
  import pandas as pd

  token = {'token': mytoken}
  stations = 'locationid='+str(locationid)+'&'+'datasetid='+str(datasetid)+'&'+'units=standard'+'&'+'limit=1000'
  r = requests.get(base_url, headers = token, params=stations)
  print("Request status code: "+str(r.status_code))

  #results comes in json form. Convert to dataframe
  df = pd.DataFrame.from_dict(r.json()['results'])
  print("Successfully retrieved "+str(len(df['id'].unique()))+" stations")
  return df
