# Flask app for showing the database contents.
import re
import psycopg2
from flask import Flask, render_template, request, redirect
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


@app.route("/", methods=["GET"])
def home():
    # A connection to the PostgreSQL database
    conn = psycopg2.connect(
        host=os.environ.get("DB_HOST"),
        database=os.environ.get("DB_DATABASE"),
        user=os.environ.get("DB_USERNAME"),
        password=os.environ.get("DB_PASSWORD"))
    cur = conn.cursor()
    most_popular = None
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
    return render_template("home.html", most_popular=most_popular)


@app.route("/date/<date_param>", methods=["GET", "POST"])
def date(date_param):
    if request.method == "POST":
        print("a")

        start, end, text = request.form.get("startTime"), request.form.get("endTime"), request.form.get("activity")
        if text == "None":
            return redirect(f"/date/{date_param}")
        currentDate = datetime.datetime.today().date() if date_param == "today" else date_param
        # A connection to the PostgreSQL database
        conn = psycopg2.connect(
            host=os.environ.get("DB_HOST"),
            database=os.environ.get("DB_DATABASE"),
            user=os.environ.get("DB_USERNAME"),
            password=os.environ.get("DB_PASSWORD"))
        cur = conn.cursor()
        try:
            cur.execute(
                f"SELECT * FROM ACTIVITY WHERE DAY_DATE = '{currentDate}' AND START_AT = '{start}' AND END_AT = '{end}';")

            # Fetch all the rows returned by the query
            row = cur.fetchall()
            # If the activity doesn't exist in the database add it
            if not row:
                cur.execute(f"INSERT INTO ACTIVITY(TEXT,START_AT,END_AT,DAY_DATE) VALUES ('{text}','{start}','{end}','{currentDate}')")
                conn.commit()
            # If the activity exists then just update it
            else:
                cur.execute(f"UPDATE ACTIVITY SET TEXT='{text}' WHERE START_AT='{start}' AND END_AT='{end}' AND DAY_DATE='{currentDate}';")
                conn.commit()
        except Exception as e:
            print(f"Error: {e}")
        finally:
            # Close the cursor and connection
            cur.close()
            conn.close()
        return redirect(f"/date/{date_param}")
    else:
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
        return render_template("today.html", day=day.day, chart_values=day.chart_values(),
                               date=(datetime.datetime.today().date() if date_param == "today" else date_param))


@app.route("/week", methods=["GET"])
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
