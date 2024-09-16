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

router = APIRouter()

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
