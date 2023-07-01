# Flask app for showing the database contents.
import psycopg2
from flask import Flask, render_template
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
TIME_FORMAT = "%H:%M"

# Select Queries
today_query = "SELECT * FROM ACTIVITY WHERE DAY_DATE=CURRENT_DATE;"
week_query = "SELECT * FROM ACTIVITY WHERE DAY_DATE >= current_date - interval '1 week' AND DAY_DATE <= current_date;"

# A connection to the PostgreSQL database
conn = psycopg2.connect(
    host=os.environ.get("DB_HOST"),
    database=os.environ.get("DB_DATABASE"),
    user=os.environ.get("DB_USERNAME"),
    password=os.environ.get("DB_PASSWORD"))


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/today")
def today():
    cur = conn.cursor()

    # Execute a select query
    cur.execute(today_query)

    # Fetch all the rows returned by the query
    rows = cur.fetchall()

    # Process the rows
    for row in rows:
        [text,start,end,date]=[row[1],row[2].strftime(TIME_FORMAT),row[3].strftime(TIME_FORMAT),row[4]]
        print(text,start,end,date)

    # Close the cursor and connection
    cur.close()
    conn.close()
    return render_template("today.html")


# running application
if __name__ == '__main__':
    app.run(debug=True)
