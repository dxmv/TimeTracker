from input import main
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime


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

# Keep the program running
try:
    while True:
        pass
except KeyboardInterrupt:
    scheduler.shutdown()