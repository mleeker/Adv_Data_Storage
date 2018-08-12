import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from sqlalchemy import distinct
from sqlalchemy import desc
from sqlalchemy import create_engine, func, inspect

from flask import Flask, jsonify


engine = create_engine("sqlite:///hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

app = Flask(__name__)

@app.route("/")
def  welcome():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/end<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    results = session.query(Measurement.prcp, Measurement.date).all()
    all_prcp = list(np.ravel(results))
    return jsonify(all_prcp)

@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Measurement.station).all()
    all_stations = list(np.ravel(results))
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    results = session.query(Measurement.tobs, Measurement.date).all()
    all_temps = list(np.ravel(results))
    return jsonify(all_temps)

@app.route("/api/v1.0/<start>")
def start(startdate, enddate):
    minimum_temp = session.query(func.min(Measurement.tobs)).filter(Measurement.date > startdate)\
                             .filter(Measurement.date < enddate).all()
    maximum_temp = session.query(func.max(Measurement.tobs)).filter(Measurement.date > startdate)\
                             .filter(Measurement.date < enddate).all()
    average_temp = session.query(func.avg(Measurement.tobs)).filter(Measurement.date > startdate)\
                             .filter(Measurement.date < enddate).all()
    return jsonify(minimum_temp, maximum_temp, average_temp)

if __name__ == '__main__':
	app.run(debug=False)