# Import the dependencies.
import numpy as np

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Starter_Code/Resources/hawaii.sqlite")

# reflect an existing database into a new model
base = automap_base()

# reflect the tables
base.prepare(engine, reflect=True)

# Save references to each table
measurement = base.classes.measurement
station = base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def Homepage():
    return (
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start_end<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    
    session = Session(engine)
    
    results = session.query(measurement.date, measurement.prcp).filter((measurement.date >= '2016-08-24') & (measurement.date <= '2017-08-23')).all()

    session.close()

    prcp_list = []
    for date, prcp_value in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp_value   
        prcp_list.append(prcp_dict)

    return jsonify(prcp_list)

@app.route("/api/v1.0/stations")
def stations():
    
    session = Session(engine)

    results = session.query(station.station).order_by(station.station).all()

    session.close()

    all_stations = [result.station for result in results]

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():

    session = Session(engine)

    results = session.query(measurement.date, measurement.tobs, measurement.prcp).filter(measurement.date >= "2016-08-23").filter(measurement.station == 'USC00519281').all()

    session.close()

    tobs = []
    for prcp, date,tobs in results:
        tobs_dict = {}
        tobs_dict["prcp"] = prcp
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        
        tobs.append(tobs_dict)

    return jsonify(tobs)

@app.route("/api/v1.0/<start_date>")
def start(start_date):

    session = Session(engine)
    # I had to put in the actual dates becuase that seemed easier for me based on my jupyter code. 
    # I am confused if these should be the same or not? 
    # Is this question wanting me to take the whole data set now instead of just one year?
    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date >= '2016-08-24').all()

    session.close()

    start_date_tobs_list = []

    for min, max, avg in results:
        temp_dict = {}
        temp_dict["min_temp"] = min
        temp_dict["avg_temp"] = avg
        temp_dict["max_temp"] = max
        start_date_tobs_list.append(temp_dict) 

    return jsonify(start_date_tobs_list)

@app.route("/api/v1.0/<start_date>/<end_date>")
def start_end(start_date, end_date):

    session = Session(engine)
    
    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter((measurement.date >= '2016-08-24') & (measurement.date <= '2017-08-23')).all()

    session.close()

    start_end_tobs_list = []
    
    for min, max, avg in results:
        temp_dict = {}
        temp_dict["min_temp"] = min
        temp_dict["avg_temp"] = avg
        temp_dict["max_temp"] = max
        start_end_tobs_list.append(temp_dict) 

    return jsonify(start_end_tobs_list)

if __name__ == "__main__":
    app.run(debug=True)