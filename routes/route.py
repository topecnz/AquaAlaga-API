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


@router.post("/update_report")
async def update_report(rep: Report, _id: str):
    data = dict(rep)
    data["updated_at"] = datetime.now()
    result = report.update_one({"_id": ObjectId(_id)}, {"$set": data})
    return {"code": 200 if result.modified_count > 0 else 204}




    

