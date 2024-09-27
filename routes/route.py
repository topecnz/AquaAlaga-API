from fastapi import APIRouter
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from models.account import Account
from models.device import Device
from models.notification import Notification
from models.report import Report
from models.schedule import Schedule
from config.database import *
from schema.schemas import *
from bson import ObjectId
from datetime import datetime
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
import json


router = APIRouter()
connected_clients = []

@router.get("/account")
async def get_account():
    accounts = account_list_serial(account.find())
    return accounts

@router.get("/login")
async def login_account(username: str, password: str):
    result = account.find_one({"username": username, "password": password})
    
    if result:
        data = {
            "id": str(result["_id"]),
            "username": result["username"]
        }
        
        print(data)
    
    return {
        "access": True if result else False,
        "data": data if result else {}
    }

@router.post("/logout")
async def logout():
    return {
        "message": "Logout successful!"
    }
    
@router.post("/update_account")
async def update_acc(id: str, acc: Account):
    data = dict(acc)
    data['updated_at'] = datetime.now()
    result = account.update_one({"_id": ObjectId(id)}, {"$set": data})
    
    if result.matched_count == 1:
        return {
            "message": "Account updated successfully!"
        }
    else:
        return {
            "message": "Not found"
        }

@router.post("/account")
async def post_account(acc: Account):
    data = dict(acc)
    data['created_at'] = datetime.now()
    data['updated_at'] = datetime.now()
    print(data)
    account.insert_one(data)
    return {
        "message": "success!"
    }

@router.get("/schedule")
async def get_schedule():
    schedules = schedule_list_serial(schedule.find())
    return schedules

@router.post("/schedule")
async def post_schedule(sched: Schedule):
    print('test')
    data = dict(sched)
    data['created_at'] = datetime.now()
    data['updated_at'] = datetime.now()
    print(data)
    result = schedule.insert_one(data)
    return {
        "code": 200 if result else 204
    }

@router.get("/report")
async def get_report():
    reports = report_list_serial(report.find())
    return reports

@router.post("/report")
async def post_report(rep: Report):
    data = dict(rep)
    data['created_at'] = datetime.now()
    result = report.insert_one(data)
    return {
        "code": 200 if result else 204
    }

@router.get("/notification") 
async def get_notification():
    notifications = notification_list_serial(notification.find())
    return notifications

@router.post("/notification")
async def post_notification(notif: Notification):
    data = dict(notif)
    data['created_at'] = datetime.now()
    result = notification.insert_one(data)
    return {
        "code": 200 if result else 204
    }

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        connected_clients.remove(websocket)
        
async def notify_clients(data: dict):
    message = json.dumps(data, default=str)
    for client in connected_clients:
        await client.send_text(message)

class SensorData(BaseModel):
    sensor: str
    data: str

@router.post("/sensor_data")
async def receive_sensor_data(sensor_data: SensorData):
    data = sensor_data.model_dump()
    data['created_at'] = datetime.now()
    result = report.insert_one(data)
    data["_id"] = str(result.inserted_id)
    notif_message = f"New sensor data: {data['sensor']} is {data['data']}"
    notification_data = {
        "message": notif_message,
        "created_at": datetime.now()
    }
    notification_result = notification.insert_one(notification_data)
    notification_data["_id"] = str(notification_result.inserted_id)
    await notify_clients(notification_data)
    return {
        "status": "Data received, notification sent!",
        "data": data
    }
    
@router.get("/sensor_data")
async def get_sensor_data():
    sensor_data = sensor_data_list_serial(report.find())
    return sensor_data

