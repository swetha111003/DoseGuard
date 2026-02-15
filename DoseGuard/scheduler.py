from apscheduler.schedulers.background import BackgroundScheduler
import datetime

scheduler = BackgroundScheduler()
scheduler.start()

def check_missed(dose_time_str, taken_flag_callback):
    """
    Checks if dose missed after 15 min
    """

    hour, minute = map(int, dose_time_str.split(":"))

    def job():
        taken = taken_flag_callback()
        if not taken:
            print("🚨 ALERT: Dose missed!")

    scheduler.add_job(
        job,
        'cron',
        hour=hour,
        minute=(minute + 15) % 60
    )
