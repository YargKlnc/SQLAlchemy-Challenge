# designing a Flask API based on the queries that were developed using Flask to create routes 

# importing the dependencies
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
import datetime as dt

#################################################
# Database Setup
#################################################
# generating the engine to the correct sqlite file 
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflecting an existing database into a new model
Base = automap_base()

# reflecting the tables
Base.prepare(autoload_with=engine)

# saving references to each table in sqlite file
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

# defining a function to be used in below lines to find the date that is one year from recent date
# binding the session between the python app and database  
def last_year_date():
    session = Session(engine)
    most_recent_date = session.query(func.max(Measurement.date)).first()[0]
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    session.close
    
    return(year_ago)

#################################################
# Flask Routes
#################################################

# displaying available routes on the landing page which is homepage
@app.route("/")
def homepage():
    """Available api routes"""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

# creating a precipitation route that returns json with the date as the key and the value as the precipitation 
# only returns the jsonified precipitation data for the last year in the database 
@app.route("/api/v1.0/precipitation")
def precipitation():
    # creating session (link) from python to the database
    session = Session(engine)

    """List of date (as key) and precipitation (prcp) (as value) from data"""
    query_results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= last_year_date()).all()
    session.close

    precipitation_list = []
    for date, prcp in query_results:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["precipitation"] = prcp
        precipitation_list.append(precipitation_dict)

    return jsonify(Precipitations=precipitation_list)

# creating a stations route that returns jsonified data of all of the stations in the database 
@app.route("/api/v1.0/stations")
def station():
    # creating session (link) from python to the database
    session = Session(engine)

    station_data = session.query(Station.station).all()

    session.close()
    station_data=list(np.ravel(station_data))

    return jsonify(Stations=station_data)

# creating a tobs route that returns jsonified data for the most active station which is USC00519281
# only returns the jsonified data for the last year of data 
@app.route("/api/v1.0/tobs")
def tobs():
    # creating session (link) from python to the database
    session = Session(engine)

    """Return a list of passenger data including the name, age, and sex of each passenger"""
    # Query all passengers
    results = session.query(Passenger.name, Passenger.age, Passenger.sex).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_passengers = []
    for name, age, sex in results:
        passenger_dict = {}
        passenger_dict["name"] = name
        passenger_dict["age"] = age
        passenger_dict["sex"] = sex
        all_passengers.append(passenger_dict)

    return jsonify(all_passengers)


# creating a start route that accepts the start date as a parameter from the URL
# and returns the min, max, and average temperatures calculated from the given start date to the end of the dataset
# @app.route("/api/v1.0/<start>")

# creating a start/end route that accepts the start and end dates as parameters from the URL
# and returns the min, max, and average temperatures calculated from the given start date to the given end date 
# @app.route("/api/v1.0/<start>/<end>")

if __name__ == '__main__':
    app.run(debug=True)