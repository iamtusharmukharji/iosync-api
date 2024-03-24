from fastapi import APIRouter
from fastapi.responses import JSONResponse
import app.schemas as schemas, app.utils as utils, app.scheduler as scheduler
from datetime import datetime, timedelta

router = APIRouter(prefix='/schedule',tags=["Schedule"])

@router.get('/')
def get_list():
    jobs = scheduler.get_job_list()
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
    
    if payload.email == "string":
        payload.email = None
    
    job_id = scheduler.add_new_job(event=utils.publish_mqtt, time=converted_date, kwargs=(payload.topic, payload.payload, payload.qos, payload.email))

    return JSONResponse(status_code=201, content={"detail":"sucess", "task_id":job_id})

@router.patch('/')
def edit(task_id:str , payload:schemas.EditSchedule):
    """
    **This endpoint can be used to schdule any mqtt message at a specific date-time**

    trigger should be in format DD-MM-YYYY HH:MM:SS(22-03-2024 21:24:16)
    Email is an optional parameter if used a notification will be sent on the mail
    """
    
    #converted_date = datetime.strptime(payload.trigger, "%d-%m-%Y %H:%M:%S")
    job_data = scheduler.get_job(job_id=task_id)
    
    if not job_data:
        return JSONResponse(status_code=404, content={"detail":"task not found"})
    
    
    payload = dict(payload)
    payload = {k:payload[k] for k in payload if payload[k] not in {"string", -1}}

    new_trigger = payload.get('trigger', job_data["scheduled_at"])
    new_trigger = datetime.strptime(new_trigger, "%d-%m-%Y %H:%M:%S")
    
    job_args = job_data['function_args']

    for i in job_args:
        if i in payload:
            job_args[i] = payload[i]

    new_args = (i for i in job_args.values())

    update = scheduler.edit_job(task_id, utils.publish_mqtt, new_trigger, new_args)
    if not update:
         return JSONResponse(status_code=404, content={"detail":"something went wrong, try later"})



    return {"detail":"task update sucess"}


@router.delete('/')
def delete(task_id:str):
    """
    **This endpoint can be used to delete any scheduled task**

    """
    
    del_job = scheduler.delete_job(job_id = task_id)
    if not del_job:
        return JSONResponse(status_code=404, content={"detail":"task not found"})
    
    return {"detail":"task removed"}