import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

from flask import Flask, jsonify
import datetime as dt

# Setting up the database

engine = create_engine("sqlite:///Resources/hawaii.sqlite", connect_args={'check_same_thread': False}, echo=True)
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station
# Create our session (link) from Python to the DB
session = Session(engine)

# Flask app

app = Flask(__name__)

@app.route("/")
def welcome():
    return(
        f"These routes are available:<br/>"
        f"<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"<br/>"
        f"/api/v1.0/stations<br/>"
        f"<br/>"
        f"/api/v1.0/tobs<br/>"
        f"<br/>"
        f"For the following, write a date in the Year-Month-Day format. For example: /api/v1.0/2017-01-01 <br/>"
        f"<br/>"    
        f"/api/v1.0/<start><br/>"
        f"<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Design a query to retrieve the last 12 months of precipitation data and plot the results
    maxdate = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    maxdate = maxdate[0]

    # Calculate the date 1 year ago from today
    year_ago = dt.datetime.strptime(maxdate, "%Y-%m-%d") - dt.timedelta(days=365)
    
    # Perform a query to retrieve the data and precipitation scores
    query = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= year_ago).all()

    # Turn into a list
    precipitation_dict = dict(query)

    return jsonify(precipitation_dict)

@app.route("/api/v1.0/stations")
def stations(): 

    # Query stations
    results_stations =  session.query(Measurement.station).group_by(Measurement.station).all()

    stations_list = list(np.ravel(results_stations))

    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs(): 
    # Design a query to retrieve the last 12 months of precipitation data and plot the results
    maxdate = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    maxdate = maxdate[0]

    # Calculate the date 1 year ago from today
    year_ago = dt.datetime.strptime(maxdate, "%Y-%m-%d") - dt.timedelta(days=365)
    # Query tobs
    results_tobs = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= year_ago).all()

    # Convert into list
    tobs = list(results_tobs)

    return jsonify(tobs)



@app.route("/api/v1.0/<start>")
def start(start=None):


    start = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).group_by(Measurement.date).all()
    from_start_list=list(start)
    return jsonify(from_start_list)

    

if __name__ == '__main__':
    app.run(debug=True)