from app.mqtt_config import c_mqtt
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from routers import schedule, automation


api = FastAPI(
    title="IOSync",
    description="This is a automation and scheduling system for custom made IOT home switchiing devices",
    version="0.1.0",)

@api.get('/', include_in_schema=False)
def index():
    return RedirectResponse(url='/docs/')



api.include_router(schedule.router)
api.include_router(automation.router)