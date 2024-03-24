from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ProcessPoolExecutor
from apscheduler.events import EVENT_JOB_MISSED
from app.email_config import send_missed_mail

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class APScheduler():
    def __init__(self) -> None:
        conn_engine = create_engine('mysql://root:mysql@localhost/iosync')

        self.jobstores = {
            'default': SQLAlchemyJobStore(engine=conn_engine) #url='mysql://root:mysql@localhost/blogu'
            }
        self.executors = {
                'default': {'type': 'threadpool', 'max_workers': 20},
                'processpool': ProcessPoolExecutor(max_workers=5)
        }    
        self.job_defaults = {
                'coalesce': False,
                'max_instances': 1
        }

    def get_scheduler(self):
        scheduler = BackgroundScheduler()
        scheduler.configure(jobstores=self.jobstores, executors=self.executors, job_defaults=self.job_defaults)
        return scheduler


def job_missed_event(event):
    
    print(f'Job id={event.job_id} is missed')

sched = APScheduler()
scheduler = sched.get_scheduler()
scheduler.add_listener(job_missed_event, EVENT_JOB_MISSED)

scheduler.start()


def add_new_job(event, time, kwargs):
    job = scheduler.add_job(event, 'date', run_date = time, args=[*kwargs])
    return job.id

def edit_job(job_id, event, time, kwargs):

    existing_job = scheduler.get_job(job_id)

    if existing_job:
        existing_job.remove()
        scheduler.add_job(event, 'date', run_date = time ,id=job_id, args=[*kwargs])

        return True
    else:
       return False

def delete_job(job_id):
    existing_job = scheduler.get_job(job_id)

    if existing_job:
        existing_job.remove()
        return True
    else:
       return False

def get_job(job_id):
    job = scheduler.get_job(job_id)

    if not job:
        return False
    res = {
            "task_id":job.id,
            "target_function":job.name,
            "function_args":{"topic":job.args[0],"payload":job.args[1],"qos":job.args[2],"email":job.args[3]},
            "scheduled_at":job.next_run_time.strftime("%Y-%d-%m-%H:%M:%S")
            }
    return res

def get_job_list():
    job_list = scheduler.get_jobs()
    data = []
    for i in job_list:
        res = {
            "task_id":i.id,
            "target_function":i.name,
            "function_args":{"topic":i.args[0],"payload":i.args[1],"qos":i.args[2],"email":i.args[3]},
            "scheduled_at":i.next_run_time.strftime("%Y-%d-%m-%H:%M:%S")
            }

        data.append(res)
    return data



