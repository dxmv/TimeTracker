from input import main
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime


# Check if the time is 12:00, 12:30, 13:00, etc...
def check_time():
    current_time = datetime.now().strftime("%H:%M")
    if current_time.endswith(":00") or current_time.endswith(":30"):
        main()


# Create a scheduler
scheduler = BackgroundScheduler()

# Schedule the check_time function to run every minute
scheduler.add_job(check_time, 'cron', minute='*')

# Start the scheduler
scheduler.start()

# Keep the program running until the user presses Ctrl+C
try:
    while True:
        pass
except KeyboardInterrupt:
    scheduler.shutdown()
