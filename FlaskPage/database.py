from flask import Flask, render_template, request, redirect, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta


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
    x_coordinate = Column(Integer, primary_key=True, nullable=False)
    y_coordinate = Column(Integer, nullable=False)
    temperature = Column(Integer, nullable=False)

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
        file_name = "/Trail CSV/MNTrainData.csv" #sample CSV file used:
        data = Load_Data(file_name)

        for r in data:
            record = Weather_History(**{
            for c in record:
                'x_coordinate : r
                'y_coordinate : c
                'temperature : r[c]
                s.add(record) #Add all the records
            })
            c = 0

        s.commit() #Attempt to commit all the records
    except:
        s.rollback() #Rollback the changes on error
    finally:
        s.close() #Close the connection
