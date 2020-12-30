def get_station_info(locationid, datasetid, mytoken, base_url):
    import requests
    import pandas as pd

    token = {'token': mytoken}
    stations = 'locationid='+str(locationid)+'&'+'datasetid='+str(datasetid)+'&'+'units=standard'+'&'\
    +'limit=1000'
    r = requests.get(base_url, headers = token, params=stations)
    # print("Request status code: "+str(r.status_code))

    if r.status_code == 200:
        df = pd.DataFrame.from_dict(r.json()['results'])

        count = 1
        num = len(df)

        while num >= count*1000:

            stations = 'locationid='+str(locationid)+'&'+'datasetid='+str(datasetid)+'&'+'units=standard'+'&'\
            +'limit=1000' + '&' + 'offset=' + str(count*1000)
            r = requests.get(base_url, headers = token, params=stations)
            # print("Request status code: "+str(r.status_code))

            if r.status_code == 200:
                #results comes in json form. Convert to dataframe
                df_pull = pd.DataFrame.from_dict(r.json()['results'])
                num += len(df_pull)
                count += 1
                df = df.append(df_pull)
            else:
                stations = 'locationid='+str(locationid)+'&'+'datasetid='+str(datasetid)+'&'+'units=standard'+'&'\
                +'limit=1000' + '&' + 'offset=' + str(count*1000)
                r = requests.get(base_url, headers = token, params=stations)
                # print("Request status code: "+str(r.status_code))
                df_pull = pd.DataFrame.from_dict(r.json()['results'])
                num += len(df_pull)
                count += 1
                df = df.append(df_pull)

        # print("Successfully retrieved "+str(len(df['id'].unique()))+" stations")
        return(df)

    else:
        token = {'token': mytoken}
        stations = 'locationid='+str(locationid)+'&'+'datasetid='+str(datasetid)+'&'+'units=standard'+'&'\
        +'limit=1000'
        r = requests.get(base_url, headers = token, params=stations)
        # print("Request status code: "+str(r.status_code))


        df = pd.DataFrame.from_dict(r.json()['results'])

        count = 1
        num = len(df)

        while num >= count*1000:

            stations = 'locationid='+str(locationid)+'&'+'datasetid='+str(datasetid)+'&'+'units=standard'+'&'\
            +'limit=1000' + '&' + 'offset=' + str(count*1000)
            r = requests.get(base_url, headers = token, params=stations)
            # print("Request status code: "+str(r.status_code))

            if r.status_code == 200:
                #results comes in json form. Convert to dataframe
                df_pull = pd.DataFrame.from_dict(r.json()['results'])
                num += len(df_pull)
                count += 1
                df = df.append(df_pull)
            else:
                stations = 'locationid='+str(locationid)+'&'+'datasetid='+str(datasetid)+'&'+'units=standard'+'&'\
                +'limit=1000' + '&' + 'offset=' + str(count*1000)
                r = requests.get(base_url, headers = token, params=stations)
                # print("Request status code: "+str(r.status_code))
                df_pull = pd.DataFrame.from_dict(r.json()['results'])
                num += len(df_pull)
                count += 1
                df = df.append(df_pull)

        # print("Successfully retrieved "+str(len(df['id'].unique()))+" stations")
        return(df)
