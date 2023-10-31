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
def last_year_date():
    # creating session (link) from python to the database
    session = Session(engine)
    # getting most recent measurement date from climate_starter.ipynb of this work
    # possible to get with; most_recent_date = session.query(func.max(Measurement.date)).first()[0]
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
@app.route("/api/v1.0/precipitation")
def precipitation():
    # creating session (link) from python to the database
    session = Session(engine)

    """List of date (as key) and precipitation (prcp) (as value) from data"""
    # query precipitation data from last_year_date
    query_results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= last_year_date()).all()
    
    #closing session
    session.close
    
    # Create a dictionary from the row data and append to a list of precipitation
    precipitation_list = []
    for date, prcp in query_results:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["precipitation"] = prcp
        precipitation_list.append(precipitation_dict)

    # only returns the jsonified precipitation data for the last year in the database 
    return jsonify(Precipitations=precipitation_list)

# creating a stations route that returns jsonified data of all of the stations in the database 
@app.route("/api/v1.0/stations")
def station():
    # creating session (link) from python to the database
    session = Session(engine)

    # query all station data
    station_data = session.query(Station.station).all()

    #closing session
    session.close()
    station_data=list(np.ravel(station_data))
    
    # only returns the jsonified list of stations from the dataset
    return jsonify(Stations=station_data)

# creating a tobs route that returns jsonified data from the most active station which is USC00519281 for the previous year
@app.route("/api/v1.0/tobs")
def tobs():
    # creating session (link) from python to the database
    session = Session(engine)

    """Return a list of tobs data for station USC00519281"""
    # query tobs data for station USC00519281 from last_year_date 
    tobs_data = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == 'USC00519281').\
                filter(Measurement.date >= last_year_date()).all()

    #closing session
    session.close()

    # Create a dictionary from the row data and append to a list of tobs
    tobs_list = []
    for date, tobs in tobs_data:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        tobs_list.append(tobs_dict)

    # only returns the jsonified data for the last year of data 
    return jsonify(Tobs=tobs_list)

# creating a start route that accepts the start date as a parameter from the URL
@app.route("/api/v1.0/<start>")
def start_date(start):
    # creating session (link) from python to the database
    session = Session(engine)

    """Return the min, max and average temperatures calculated from the given start date"""
    # query data for tmin, tmax and tavg from a given start date 
    start_date_tobs = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    
    #closing session
    session.close()

    # creating a dictionary for query above 
    start_date_tobs_values = []
    for min, max, avg in start_date_tobs:
        start_date_tobs_dict = {}
        start_date_tobs_dict["min temp"] = min
        start_date_tobs_dict["max temp"] = max
        start_date_tobs_dict["average temp"] = avg
        start_date_tobs_values.append(start_date_tobs_dict)

    # returns the min, max, and average temperatures calculated from the given start date
    return jsonify(start_date_tobs_values)

# creating a start/end route that accepts the start and end dates as parameters from the URL
@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):
    # creating session (link) from python to the database
    session = Session(engine)

    """Return the min, max and average temperatures calculated from the entered start date to an entered end date"""
    # query data for tmin, tmax and tavg from start date to end date entered in the URL 
    start_end_date_tobs = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()

    #closing session
    session.close()

    # creating a dictionary for query above 
    start_end_date_tobs_values = []
    for min, max, avg in start_end_date_tobs:
        start_end_date_tobs_dict = {}
        start_end_date_tobs_dict["min temp"] = min
        start_end_date_tobs_dict["max temp"] = max
        start_end_date_tobs_dict["average temp"] = avg
        start_end_date_tobs_values.append(start_end_date_tobs_dict)

    # returns the tmin, tmax, and tavg calculated from the entered start date and end date 
    return jsonify(start_end_date_tobs_values)

if __name__ == '__main__':
    app.run(debug=True)