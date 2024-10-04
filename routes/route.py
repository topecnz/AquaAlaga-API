from fastapi import APIRouter, requests
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
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
from fastapi.responses import HTMLResponse
from typing import List
import logging
import json
import requests


router = APIRouter()
websocket_connections: List[WebSocket] = []

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
        return {"access": True, "data": data}
    else:
        print("No matching account found")
    
    return {"access": False, "data": {}}


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


@router.post("/update_schedule")
async def update_schedule(sched: Schedule, _id: str):
    data = dict(sched)
    data["updated_at"] = datetime.now()
    result = schedule.update_one({"_id": ObjectId(_id)}, {"$set": data})
    return {
        "code": 200 if result.modified_count > 0 else 204
    }

@router.delete("/delete_schedule")
async def delete_schedule(_id: str):
    result = schedule.delete_one({"_id": ObjectId(_id)})

    if result.deleted_count == 1:
        return {
            "message": "Schedule deleted successfully!"
        }
    else:
        return {
            "message": "Schedule not found"
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
    websocket_connections.append(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        websocket_connections.remove(websocket)
        
        
async def notify_clients(data: dict):
    message = json.dumps(data, default=str)
    for client in websocket_connections:
        await client.send_text(message)

class SensorData(BaseModel):
    sensor: str
    data: str

EXPO_PUSH_URL = "https://exp.host/--/api/v2/push/send"

@router.post("/sensor_data")
async def receive_sensor_data(sensor_data: SensorData):
    data = sensor_data.model_dump()  
    data['created_at'] = datetime.now()
    report_result = report.insert_one(data)
    data['_id'] = str(report_result.inserted_id)
    
    notif_message = f"New sensor data: {data['sensor']} is {data['data']}"

    notification_data = {
        "message": notif_message,
        "created_at": datetime.now()
    }
    notification.insert_one(notification_data)
    

    tokens_cursor = notification.find({"expo_token": {"$exists": True}}, {"expo_token": 1, "_id": 0})
    tokens = list(tokens_cursor)

    if tokens:
        for token in tokens:
            if "expo_token" in token:
                response = await send_push_notification(token["expo_token"], notif_message)
                logging.info(f"Notification sent to {token['expo_token']}: {response}")
    
    for connection in websocket_connections:
        try:
            await connection.send_text(notif_message)
        except WebSocketDisconnect:
            websocket_connections.remove(connection)

    return {"status": "Data received and notification sent", "data": jsonable_encoder(data)}


async def send_push_notification(token, message):
    payload = {
        "to": token,
        "sound": "default",
        "title": "New Sensor Data",
        "body": message,
    }
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    response = requests.post(EXPO_PUSH_URL, json=payload, headers=headers)
    return response.json()
    
@router.get("/sensor_data")
async def get_sensor_data():
    sensor_data = sensor_data_list_serial(report.find())
    return sensor_data

class SensorData(BaseModel):
    sensor: str
    data: str

class PushToken(BaseModel):
    expo_token: str

@router.post("/register_push_token")
async def register_push_token(token: PushToken):
    
    try:
        notification.update_one(
            {"expo_token": token.expo_token},
            {"$set": {"expo_token": token.expo_token, "created_at": datetime.now()}},
            upsert=True
        )
        return {"message": "Token registered successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

