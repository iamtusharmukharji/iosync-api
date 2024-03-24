from fastapi import APIRouter
from fastapi.responses import JSONResponse
import schemas, utils, scheduler_config
from datetime import datetime, timedelta

router = APIRouter(prefix='/schedule',tags=["Schedule"])

@router.get('/')
def get_list():
    jobs = scheduler_config.get_job_list()
    # print(jobs)
    # print(dir(jobs[0]))
    return JSONResponse(status_code=200, content={"detail":"sucess", "data":jobs})

@router.post('/')
def schedule(payload:schemas.Schedule):
    """
    **This endpoint can be used to schdule any mqtt message at a specific date-time**

    trigger should be in format DD-MM-YYYY HH:MM:SS(22-03-2024 21:24:16)
    Email is an optional parameter if used a notification will be sent on the mail
    """
    
    converted_date = datetime.strptime(payload.trigger, "%d-%m-%Y %H:%M:%S")

    job_id = scheduler_config.add_new_job(event=utils.publish_mqtt, time=converted_date, kwargs=(payload.topic, payload.payload, payload.qos, payload.email))

    return JSONResponse(status_code=201, content={"detail":"sucess", "task_id":job_id})

@router.patch('/')
def edit(task_id:str , payload:schemas.EditSchedule):
    """
    **This endpoint can be used to schdule any mqtt message at a specific date-time**

    trigger should be in format DD-MM-YYYY HH:MM:SS(22-03-2024 21:24:16)
    Email is an optional parameter if used a notification will be sent on the mail
    """
    
    converted_date = datetime.strptime(payload.trigger, "%d-%m-%Y %H:%M:%S")

    job_id = scheduler_config.add_new_job(event=utils.publish_mqtt, time=converted_date, kwargs=(payload.topic, payload.payload, payload.qos))

    return {"detail":"task update sucess"}