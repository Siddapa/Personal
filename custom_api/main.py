from cmath import e
from typing import Dict
from unittest.util import strclass
from fastapi import FastAPI, Form, Response
from pydantic import BaseModel
import json

class Event(BaseModel):
    name : str
    date : str
    time : str
    tod : str
    all_day : bool

app = FastAPI()


"""
Writes Event model to json file
"""
@app.post("/new_event")
async def new_event(event : Event):
    events : dict
    with open('events.json', 'r') as events_file:
        events = json.loads(events_file.read())
    with open('events.json', 'w') as events_file:
        last_event_index = len(events.items())
        events[last_event_index] = event.dict()
        json.dump(events, events_file, indent=4)


@app.get('/get_events')
async def get_events():
    events : dict
    with open('events.json', 'r') as events_file:
        events = json.load(events_file)
    return Response(content=str(events), media_type='application/json')

