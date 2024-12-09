from apscheduler.schedulers.background import BackgroundScheduler

from app.tasks import send_daily_notifications

scheduler = BackgroundScheduler()


def start_scheduler():
    if not scheduler.running:
        scheduler.add_job(send_daily_notifications, 'cron', hour=9, minute=10)
        scheduler.start()
