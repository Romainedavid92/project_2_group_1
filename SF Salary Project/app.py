import pandas as pd
import numpy as np

from sqlalchemy import create_engine
from flask import Flask, jsonify, render_template
import gender_guesser.detector as gender

app = Flask(__name__)


#################################################
# Database Setup
#################################################

# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/lahman2016.sqlite"
# db = SQLAlchemy(app)

engine = create_engine("sqlite:///db/database.sqlite")
d = gender.Detector(case_sensitive=False)

@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")

@app.route("/genderSalaryPage")
def genderSalaryPage():
    """Return the homepage."""
    return render_template("genderSalary.html")

@app.route("/jobTitlePage")
def jobTitlePage():
    """Return the homepage."""
    return render_template("jobTitle.html")

@app.route("/baseOvertimePage")
def baseOvertimePage():
    """Return the homepage."""
    return render_template("baseOvertime.html")

@app.route("/salaries/<year>")
def salaries(year):
    conn = engine.connect()

    query = f"""SELECT *
            FROM Salaries
            WHERE TotalPay > 2000
            AND Year = {year}"""

    df = pd.read_sql(query, conn) #execute query

    #debug log to console
    print(df.head())

    #close db connection
    conn.close()
    return df.to_json(orient="index")


@app.route("/jobTitles/<year>/<topBottom>")
def jobTitles(year, topBottom):
    conn = engine.connect()

    asc = "DESC"

    if topBottom == "Bottom":
        asc = "ASC"

    query = f"""
            SELECT 
                JobTitle, 
                round(avg(TotalPay)) as "Mean_Salary"                        
            FROM
                Salaries
            WHERE 
                TotalPay > 2000
                AND Year = {year}
            GROUP BY 
                JobTitle
            ORDER BY
                avg(TotalPay) {asc}
            """

    df = pd.read_sql(query, conn) #execute query
    df["JobTitle"] = df.JobTitle.map(lambda x: trimJobTitle(x));

    #debug log to console
    print(df.head())

    #close db connection
    conn.close()
    return df.to_json(orient="index")

def trimJobTitle(word):
    tooLong = 35
    newWord = word.title();
    if len(newWord) > tooLong:
        newWord = newWord[0:tooLong] + "...  "
    else:
        newWord = newWord + "  "
    return newWord

@app.route("/genders/<year>")
def genders(year):
    conn = engine.connect()

    query = f"""SELECT *
        FROM Salaries
        WHERE TotalPay > 2000
        AND Year = {year}"""

    df = pd.read_sql(query, conn) #execute query
    genders = df.EmployeeName.map(lambda x: d.get_gender(x.split(" ")[0]))

    df["Gender"] = genders
    df["Gender"] = df["Gender"].replace("mostly_male", "male")
    df["Gender"] = df["Gender"].replace(["mostly_female","unknown", "andy"], "female")

    maleAvg = df.loc[df.Gender == "male", "TotalPay"].mean()
    maleMed = df.loc[df.Gender == "male", "TotalPay"].median()
    maleMax = df.loc[df.Gender == "male", "TotalPay"].max()

    femaleAvg = df.loc[df.Gender == "female", "TotalPay"].mean()
    femaleMed = df.loc[df.Gender == "female", "TotalPay"].median()
    femaleMax = df.loc[df.Gender == "female", "TotalPay"].max()

    df2 = pd.DataFrame()
    df2["Gender"] = ["Male", "Female"]
    df2["AveragePay"] = [maleAvg, femaleAvg]
    df2["MedianPay"] = [maleMed, femaleMed]
    df2["MaxPay"] = [maleMax, femaleMax]
    df2["Year"] = [year, year]

    #close db connection
    conn.close()
    return df2.to_json(orient="index")

if __name__ == "__main__":
    app.run(debug=True)
