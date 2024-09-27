from fastapi import APIRouter
from models.account import Account
from models.device import Device
from models.notification import Notification
from models.report import Report
from models.schedule import Schedule
from config.database import *
from schema.schemas import *
from bson import ObjectId
from datetime import datetime
from fastapi import FastAPI, WebSocket, WebSocketDisconnect


router = APIRouter()
app = FastAPI()

connected_clients=[]


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


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    connected_clients.append(websocket)

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        connected_clients.remove(websocket)


@router.post("/sensor_data")
async def post_sensor_data(rep: Report):
    # insert sensor data
    data = dict(rep)
    data['created_at'] = datetime.now()
    result = report.insert_one(data)

    # insert notification data
    if result:
        notification_message = f"New message: {rep.sensor} - {rep.data}"
        notification_data = {
            "message": notification_message,
            "created_at": datetime.now()
        }
        notification.insert_one(notification_data)

        await manager.broadcast(notification_message)

    return {
        "code": 200 if result else 204
    }

@router.get("/sensor_data")
async def get_sensor_data():
    sensor_data = sensor_data_list_serial(report.find())
    return sensor_data


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


