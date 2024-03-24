from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ProcessPoolExecutor
from apscheduler.events import EVENT_JOB_MISSED
from pytz import utc




jobstores = {
    'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
    }
executors = {
        'default': {'type': 'threadpool', 'max_workers': 20},
        'processpool': ProcessPoolExecutor(max_workers=5)
}    
job_defaults = {
        'coalesce': False,
        'max_instances': 1
}


scheduler = BackgroundScheduler()
scheduler.configure(jobstores=jobstores, executors=executors, job_defaults=job_defaults)

def job_missed_event(event):

    print(f'Job id={event.job_id} is missed')


def add_new_job(event, time, kwargs):
    job = scheduler.add_job(event, 'date', run_date = time, args=[*kwargs])
    return job.id


def edit_job(job_id, event, time, **kwargs):

    existing_job = scheduler.get_job(job_id)

    if existing_job:
        existing_job.remove()
        scheduler.add_job(event, 'date', run_date = time ,id=job_id, args=[*kwargs])

        return True
    else:
       return False

def get_job_list():
    job_list = scheduler.get_jobs()
    data = []
    for i in job_list:
        res = {
            "task_id":i.id,
            "target_function":i.name,
            "function_args":i.args,
            "scheduled_at":i.next_run_time.strftime("%Y-%d-%m-%H:%M:%S")
            }

        data.append(res)
    return data



scheduler.add_listener(job_missed_event, EVENT_JOB_MISSED)

scheduler.start()
