# Flask app for showing the database contents.
import re
import psycopg2
from flask import Flask, render_template
import os
from dotenv import load_dotenv
from action import Day
import datetime

load_dotenv()
app = Flask(__name__)
TIME_FORMAT = "%H:%M"
date_regex = r"\d{4}-\d{2}-\d{2}"

# Select Queries
today_query = "SELECT * FROM ACTIVITY WHERE DAY_DATE=CURRENT_DATE;"
week_query = "SELECT * FROM ACTIVITY WHERE DAY_DATE >= current_date - interval '1 week' AND DAY_DATE <= current_date;"
week_activities_query = "SELECT TEXT,COUNT(*) FROM ACTIVITY WHERE DAY_DATE >= current_date - interval '1 week' AND DAY_DATE <= current_date GROUP BY TEXT ORDER BY COUNT(*);"
month_activities_query = "SELECT TEXT,COUNT(*) FROM ACTIVITY WHERE DAY_DATE >= current_date - interval '1 month' AND DAY_DATE <= current_date GROUP BY TEXT ORDER BY COUNT(*);"


@app.route("/")
def home():

    # A connection to the PostgreSQL database
    conn = psycopg2.connect(
        host=os.environ.get("DB_HOST"),
        database=os.environ.get("DB_DATABASE"),
        user=os.environ.get("DB_USERNAME"),
        password=os.environ.get("DB_PASSWORD"))
    cur = conn.cursor()
    most_popular=None
    try:

        # Execute a select query
        cur.execute(month_activities_query)

        # Fetch all the rows returned by the query
        most_popular = cur.fetchall()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Close the cursor and connection
        cur.close()
        conn.close()
    return render_template("home.html",most_popular=most_popular)


@app.route("/date/<date_param>")
def date(date_param):
    if not re.match(date_regex, date_param) and date_param != "today":
        return render_template("today.html", error="The format of the date is wrong")
    day = Day()

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
            day.add_value(key, start, end, text, date)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Close the cursor and connection
        cur.close()
        conn.close()
        print(day.top_actions())
    return render_template("today.html", day=day.day, chart_values=day.chart_values())


@app.route("/week")
def week():
    # Get the current date
    current_date = datetime.date.today()

    # Calculate the date 7 days ago
    seven_days_ago = current_date - datetime.timedelta(days=7)

    # Generate a list of the last 7 days
    last_7_days = [seven_days_ago + datetime.timedelta(days=i) for i in range(7)]
    most_popular = None
    week_days = {}
    final = {}
    # Print the last 7 days
    for day in last_7_days:
        week_days[str(day)] = Day()
        final[(str(day), str(day).split("-")[2])] = None

    # A connection to the PostgreSQL database
    conn = psycopg2.connect(
        host=os.environ.get("DB_HOST"),
        database=os.environ.get("DB_DATABASE"),
        user=os.environ.get("DB_USERNAME"),
        password=os.environ.get("DB_PASSWORD"))
    cur = conn.cursor()
    try:

        # Execute a select query
        cur.execute(week_query)

        # Fetch all the rows returned by the query
        rows = cur.fetchall()
        # Process the rows
        for row in rows:
            [text, start, end, date] = [row[1], row[2].strftime(TIME_FORMAT), row[3].strftime(TIME_FORMAT), row[4]]
            key = f"{start}-{end}"
            week_days[str(date)].add_value(key, start, end, text, date)
        for key, val in week_days.items():
            final[(str(key), str(key).split("-")[2])] = val.top_actions()

        cur.execute(week_activities_query)
        most_popular = cur.fetchall()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Close the cursor and connection
        cur.close()
        conn.close()
    return render_template("week.html", week=final, most_popular=most_popular)


# running application
if __name__ == '__main__':
    app.run(debug=True)
