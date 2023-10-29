# Import the dependencies.
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
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)
# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
# # Create our session (link) from Python to the DB
# session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

# Defining a function to find the date one year from recent date 
# as like in climate_starter.ipynb of this project to be used in below lines
def last_year_date():
    session = Session(engine)
    most_recent_date = session.query(func.max(Measurement.date)).first()[0]
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    session.close
    
    return(year_ago)
#################################################
# Flask Routes
#################################################
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

@app.route("/api/v1.0/precipitation")
def precipitation():

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

    return jsonify(precipitation_list)

@app.route("/api/v1.0/stations")
def station():

    session = Session(engine)

    station_data = session.query(Station.station, Station.id).all()

    session.close()
    
    stations_list = []
    for station, id in station_data:
        stations_list_dict = {}
        stations_list["station"] = station
        stations_list["id"] = id
        stations_list.append(stations_list_dict)

    return jsonify(stations_list)


# @app.route("/api/v1.0/tobs")

# @app.route("/api/v1.0/<start>")

# @app.route("/api/v1.0/<start>/<end>")

if __name__ == '__main__':
    app.run(debug=True)