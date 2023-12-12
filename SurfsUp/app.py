# Import the dependencies.
import numpy as np
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from datetime import datetime, timedelta
import datetime as dt
from flask import Flask, jsonify

# Database Setup

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model

Base = automap_base()

# reflect the tables

Base.prepare(autoload_with=engine)

# Save references to each table

measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB

session = Session(engine)

# Flask Setup

app = Flask(__name__)

# Flask Routes

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Welcome to the SQL-Alchemy APP API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start> and /api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    
    """retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value."""
    
    # Query all passengers
    latest_dt =session.query(measurement.date).order_by(measurement.date.desc()).first()
    year_ago = dt.date(2017,8, 23) - dt.timedelta(days=365)
    
    results = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date >= year_ago).all()
    

    session.close()

    # Convert results into a dictionary
    
    precipitation_dict = {date: prcp for date, prcp in results}

    return jsonify(precipitation_dict)

## doing the second route 

@app.route("/api/v1.0/stations")
def stations():
    
    """Return a JSON list of stations from the dataset."""
    
    # Query all passengers
    results =session.query(measurement.station, func.count(measurement.station)).\
                 group_by(measurement.station).order_by(func.count(measurement.station).desc()).all()
    

    session.close()


    # Convert results into a dictionary

    stations_dict = {station: count for station, count in results}


    return jsonify(stations_dict)

@app.route("/api/v1.0/tobs")
def tobs():
    
   #Query the dates and temperature observations of the most-active station for the previous year of data
    
   results = session.query(measurement.station, measurement.date, measurement.tobs)\
            .filter(measurement.station == 'USC00519281')\
            .filter(measurement.date >= '2016-08-23', measurement.date <= '2017-08-23')\
            .all()
   
   
   session.close()

    # Convert results into a list comprenhension (key:value)
    
    
   tobs_list = [{'station': station, 'date': date, 'tobs': tobs} for station, date, tobs in results]
    
   return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")

def Start(start):

    """Return a list of min, avg and max tobs for a start date"""
    
    # Query all tobs

    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
                filter(measurement.date >= '2017-08-23').all()

    session.close()
    
    # Extract results so that i can create the dic
    
    min_tobs, avg_tobs, max_tobs = results[0]

    
    #Dictorionary with start list 
    start_stats = {
    "min_temperature": min_tobs,
    "average_temperature": avg_tobs,
    "max_temperature": max_tobs
}
    return jsonify(start_stats)

if __name__ == '__main__':
    app.run(debug=True)
