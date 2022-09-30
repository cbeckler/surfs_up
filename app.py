################# FLASK #####################

# routes are the paths a search can take

# import
from flask import Flask, jsonify
import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# set up the database

## create engine
### needed to add check_same_thread arg to solve bug about mismatched threads in cnxn
engine = create_engine("sqlite:///hawaii.sqlite", connect_args={'check_same_thread': False})
## reflect the tables with base
Base = automap_base()
Base.prepare(engine, reflect=True)
## create vars for classes
Measurement = Base.classes.measurement
Station = Base.classes.station
## create a session link
session = Session(engine)

# set up Flask

# create a new Flask instance
## __name__ is a magic method that will determine if code is being run from command line or imported into other code
### __name__ is the name of the current function
app = Flask(__name__)

# build Flask routes

## create the first route--most important to ensure we can access ALL of the analysis
### '/' denotates that the data is at the root of our route
@app.route('/')

### a function will set up our other routes
#### routes following the naming convention /api/v1.0/ -- 1.0 is specifying app version
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')

## create second route--precipitation
@app.route("/api/v1.0/precipitation")

### a function will provide analysis data
def precipitation():
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   precipitation = session.query(Measurement.date, Measurement.prcp).\
      filter(Measurement.date >= prev_year).all()

   # need to create a dict with date as key and precipitation as vlue using jsonify()
   precip = {date: prcp for date, prcp in precipitation}
   return jsonify(precip)

## create third route--stations
@app.route("/api/v1.0/stations")

### a function will provide analysis data
def stations():
    results = session.query(Station.station).all()
    # we are using np.ravel to get our results in a one dimensional array and converting to list
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

## create fourth route--monthly temp
@app.route("/api/v1.0/tobs")

### a function will provide analysis data
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

## create fifth route--stats
### need to provide both start AND end date
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

## a function will provide analysis data
def stats(start=None, end=None):
    # list of desired stats
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    # if no end date provided:
    if not end:
        # query data--*sel indicates there will be multiple results
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        # convert to 1D list
        temps = list(np.ravel(results))
        return jsonify(temps)
    
    # query data with start and end filters
    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    # convert to 1D list
    temps = list(np.ravel(results))
    return jsonify(temps)