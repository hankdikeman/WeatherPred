from numpy import genfromtxt
from time import time
from datetime import datetime
from sqlalchemy import Column, Integer, Float, Date, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#database.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
#db = SQLAlchemy(database)

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
    day =  Column(Integer, nullable=False)
    month =  Column(Integer, nullable=False)
    year =  Column(Integer, nullable=False)
    temperature = Column(Text, nullable=False)

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
        #file_name = "/Trail CSV/MNTrainData.csv" #sample CSV file used:
        csv_line= np.genfromtxt('/Users/uvman/OneDrive/Documents/School/2020/WeatherPred/USTrainData1_1_2002TO9_17_2004.csv', delimiter=',')[-30:,:-1]

        for row in range(np.shape(csv_line)[0]):
            concat_str = []
            for col in range(np.shape(csv_line)[1]-3):
                concat_str.append(str(csv_line[row,col]))
                concat_str.append(',')
            concat_str.pop()
            # save entry date into db
            record = Weather_History(**{
                'day' : csv_line[-1],
                'month' : csv_line[-2],
                'year' : csv_line[-3],
                'temperature' : ''.join(concat_str)
            })
            s.add(record) #Add all the records

        s.commit() #Attempt to commit all the records
    except:
        s.rollback() #Rollback the changes on error
    finally:
        s.close() #Close the connection

  # Query Stuff
  weather_range = (
    session.query(Weather_History)
    .filter(Weather_History.day == 01)
    .filter(Weather_History.month == 03)
    .filter(Weather_History.year == 2020)
    )
  if weather_range is not None:
      return
