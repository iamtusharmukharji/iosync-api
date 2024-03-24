from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Schedule(BaseModel):
    topic:str = "mqttdev16620923tss"
    payload:str = "s/0/0"
    qos:int = 1
    trigger:str = datetime.now().strftime("%d-%m-%Y %H:%M:%S")#"22-03-2024 21:24:16"
    email:Optional[str] = None

class EditSchedule(BaseModel):
    topic:Optional[str]
    payload:Optional[str]
    qos:Optional[int]
    trigger:Optional[str]
    email:Optional[str] = None

class Automate(BaseModel):
    source_topic:str
    source_threshold:str
    target_topic:str
    taret_payload_upper:str
    taret_payload_lower:str
    qos:int
    email:Optional[str] = None