import click
import logging
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()
logging.getLogger('apscheduler.scheduler').setLevel(logging.ERROR)
logging.getLogger('apscheduler.executors.default').setLevel(logging.ERROR)
logging.basicConfig(
	filename="/sdcard/qlogger/app.log",		filemode="a",
	format="%(asctime)s :%(levelname)s:%(name)s:%(message)s",	datefmt="%d-%b-%y %I:%M:%S %p",			level='DEBUG',
)

def func_to_run():
	print("function is running...")

scheduler_status = {"running": False}

def start_scheduler(interval):
    global scheduler_status
    job_id = scheduler.add_job(func_to_run, trigger='interval', seconds=interval)
    scheduler.start()
    scheduler_status["running"]=True
    logging.info("Scheduler started...")



@click.command()
@click.option("-i", "--interval", default=5, help="Number of seconds for interval", type=int, show_default=True)
def start(interval):
    start_scheduler(interval)

    stop_flag = False
    try:
        while not stop_flag:
            x = input("$ ")
            if x.strip().lower() == 'stop':
                stop_flag = True
            elif x.strip().lower() == 'status':
            	if scheduler_status["running"]:
            		logging.info("scheduler is running...")
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        stop()
        logging.error("Scheduler has been shut down gracefully!")

@click.command()
def stop():
	if scheduler.running:
		scheduler.shutdown()
		logging.info("scheduler has been stopped!")
	else:
		logging.warning("scheduler is not running! from stop")

@click.command()
def status():
	if scheduler.running or scheduler_status["running"]:
		logging.info("scheduler is running...")
	else:
		logging.warning("scheduler is not running! from status")
	
