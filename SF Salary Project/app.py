import os

import pandas as pd
import numpy as np

from sqlalchemy import create_engine

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


#################################################
# Database Setup
#################################################

# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/lahman2016.sqlite"
# db = SQLAlchemy(app)

engine = create_engine("sqlite:///db/database.sqlite")

@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")

@app.route("/salaries/")
def salaries():
    conn = engine.connect()

    query = """SELECT *
            FROM Salaries
            WHERE TotalPay > 2000
            LIMIT 200"""

    df = pd.read_sql(query, conn) #execute query

    #debug log to console
    print(df.head())

    #close db connection
    conn.close()
    return df.to_json(orient="index")

# @app.route("/teams/<year>")
# def teams(year):
#     conn = engine.connect()

#     query = f"""SELECT 
#                     *
#                 FROM Teams
#                 WHERE yearID = {year}
#             """

#     df = pd.read_sql(query, conn) #execute query

#     #debug log to console
#     print(df.head())

#     #close db connection
#     conn.close()
#     return df.to_json(orient="index")

# @app.route("/people")
# def people():
#     conn = engine.connect()

#     query = """SELECT 
#                     *
#                 FROM Master
#                 LIMIT 100
#             """

#     df = pd.read_sql(query, conn) #execute query

#     #debug log to console
#     print(df.head())

#     #close db connection
#     conn.close()
#     return df.to_json(orient="index")

if __name__ == "__main__":
    app.run(debug=True)
