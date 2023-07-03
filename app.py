# Flask app for showing the database contents.
import datetime
import re
import psycopg2
from flask import Flask, render_template
import os
from dotenv import load_dotenv
from action import Action

load_dotenv()
app = Flask(__name__)
TIME_FORMAT = "%H:%M"
date_regex = r"\d{4}-\d{2}-\d{2}"

# Select Queries
today_query = "SELECT * FROM ACTIVITY WHERE DAY_DATE=CURRENT_DATE;"
week_query = "SELECT * FROM ACTIVITY WHERE DAY_DATE >= current_date - interval '1 week' AND DAY_DATE <= current_date;"


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/date/<date_param>")
def date(date_param):
    if not re.match(date_regex, date_param) and date_param != "today":
        return render_template("today.html", error="The format of the date is wrong")
    day = {}
    for hour in range(24):
        start_one, start_two = [f"{convert_hours_string(hour)}:00", f"{convert_hours_string(hour)}:30"]
        end_one, end_two = [f"{convert_hours_string(hour)}:30", f"{convert_hours_string(hour + 1)}:00"]
        day[f"{start_one}-{end_one}"] = Action(start_one, end_one,None, datetime.date)
        day[f"{start_two}-{end_two}"] = Action(start_two, end_two,None, datetime.date)

    # A connection to the PostgreSQL database
    conn = psycopg2.connect(
        host=os.environ.get("DB_HOST"),
        database=os.environ.get("DB_DATABASE"),
        user=os.environ.get("DB_USERNAME"),
        password=os.environ.get("DB_PASSWORD"))
    cur = conn.cursor()
    try:

        # Execute a select query
        if date_param == "today":
            cur.execute(today_query)
        else:
            cur.execute(f"SELECT * FROM ACTIVITY WHERE DAY_DATE='{date_param}'")

        # Fetch all the rows returned by the query
        rows = cur.fetchall()

        # Process the rows
        for row in rows:
            [text, start, end, date] = [row[1], row[2].strftime(TIME_FORMAT), row[3].strftime(TIME_FORMAT), row[4]]
            key = f"{start}-{end}"
            day[key] = Action(start, end, text, date)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Close the cursor and connection
        cur.close()
        conn.close()
    return render_template("today.html", day=day)


@app.route("/week")
def week():
    pass


def convert_hours_string(hour):
    if hour < 10:
        return f"0{hour}"
    return f"{hour}"


# running application
if __name__ == '__main__':
    app.run(debug=True)
