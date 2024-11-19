from fastapi import APIRouter
from models.account import Account, UpdateAccount, ResetPassword, FirstSetup, SecurityAnswer, ChangePassword
from models.device import Device
from models.notification import Notification
from models.report import Report
from models.schedule import Schedule
from config.database import *
from schema.schemas import *
from bson import ObjectId
from datetime import datetime
import time

router = APIRouter()

@router.get("/account")
async def get_account(_id: str):
    accounts = account_serial(account.find_one({"_id": ObjectId(_id)}))
    return accounts

@router.get("/login")
async def login_account(username: str, password: str):
    result = account.find_one({"username": username, "password": password})
    
    if result:
        data = {
            "id": str(result["_id"]),
            "username": result["username"],
            "is_first_time": result['is_first_time']
        }
        
        print(data)
    
    return {
        "access": True if result else False,
        "data": data if result else {}
    }

# @router.post("/logout")
# async def logout():
#     return {
#         "message": "Logout successful!"
#     }
    
# @router.post("/update_account")
# async def update_acc(id: str, acc: Account):
#     data = dict(acc)
#     data['updated_at'] = datetime.now()
#     result = account.update_one({"_id": ObjectId(id)}, {"$set": data})
    
#     if result.matched_count == 1:
#         return {
#             "message": "Account updated successfully!"
#         }
#     else:
#         return {
#             "message": "Not found"
#         }

@router.post("/account")
async def post_account(acc: Account):
    data = dict(acc)
    data['is_first_time'] = True
    data['created_at'] = datetime.now()
    data['updated_at'] = datetime.now()
    print(data)
    account.insert_one(data)
    return {
        "message": "success!"
    }
    
@router.post("/first_setup")
async def post_first_setup(acc: FirstSetup):
    data = dict(acc)
    acc_id = data.pop('id')
    data['is_first_time'] = False
    data['updated_at'] = datetime.now()
    
    result = account.update_one({"_id": ObjectId(acc_id)}, {"$set": data})
    return {
        "code": 200 if result else 204
    }
    
@router.put("/account")
async def put_account(acc: UpdateAccount):
    data = dict(acc)
    acc_id = data.pop('id')
    data['updated_at'] = datetime.now()
    
    result = account.update_one({"_id": ObjectId(acc_id)}, {"$set": data})
    return {
        "code": 200 if result else 204
    }
    
@router.get("/find")
async def find_username(username: str):
    is_found = account.find_one({'username': username}, {'_id': 1})
    
    return {
        "code": 200 if is_found else 204,
        "id": str(is_found['_id']) if is_found else None
    }
    
@router.put("/reset")
async def reset_password(acc: ResetPassword):
    data = dict(acc)
    acc_id = data.pop('id')
    data['updated_at'] = datetime.now()
    
    result = account.update_one({"_id": ObjectId(acc_id)}, {"$set": data})
    return {
        "code": 200 if result else 204
    }
    
@router.put("/changepass")
async def reset_password(acc: ChangePassword):
    data = dict(acc)
    acc_id = data.pop('id')
    data['updated_at'] = datetime.now()
    
    result = account.update_one({"_id": ObjectId(acc_id)}, {"$set": data})
    return {
        "code": 200 if result else 204
    }

@router.get("/security")
async def security_question(_id: str):
    
    is_found = account.find_one({"_id": ObjectId(_id)})
    
    return {
        "code": 200 if is_found else 204,
        "security_question": is_found['security_question'] if is_found else None
    }

@router.post("/securityanswer")
async def security_answer(sec: SecurityAnswer):
    data = dict(sec)
    acc_id = data.pop('id')
    
    is_found = account.find_one({"_id": ObjectId(acc_id), "security_answer": data["security_answer"]})
    
    return {
        "code": 200 if is_found else 204,
    }

@router.get("/schedule")
async def get_schedule(_id: str):
    schedules = schedule_list_serial(schedule.find({'device_id': _id}))
    return schedules

@router.post("/schedule")
async def post_schedule(sched: Schedule):
    data = dict(sched)
    data['created_at'] = datetime.now()
    data['updated_at'] = datetime.now()
    
    # Check if the time schedule is already existed.
    is_existed = schedule.find_one({'time': data['time']}, {'_id': 0, 'time': 1})
    if is_existed:
        return {
            "code": 409, # 409 means Conflict
            "message": "Time Schedule already existed."
        }    
    
    result = schedule.insert_one(data)
    return {
        "code": 200 if result else 204
    }

@router.put("/schedule")
async def toggle_schedule(_id: str):
    # get current id
    data = schedule.find_one({'_id': ObjectId(_id)}, {'_id': 1, 'is_enable': 1})
    data['is_enable'] = not data['is_enable']
    data['updated_at'] = datetime.now()
    
    result = schedule.update_one({"_id": ObjectId(_id)}, {"$set": data})
    return {
        "code": 200 if result else 204
    }

@router.patch("/schedule")
async def update_schedule(sched: Schedule, _id: str):
    data = dict(sched)
    data["updated_at"] = datetime.now()
    
    # Check if the time schedule is already existed before updating.
    is_existed = schedule.find_one({'time': data['time']}, {'_id': 1, 'time': 1})
    
    if is_existed:
        # if it is not the same ObjectId
        if str(is_existed['_id']) != _id:
            return {
                "code": 409, # 409 means Conflict
                "message": "Time Schedule already existed."
            }
    
    result = schedule.update_one({"_id": ObjectId(_id)}, {"$set": data})
    return {
        "code": 200 if result else 204
    }

@router.delete("/schedule")
async def delete_schedule(_id: str):
    result = schedule.delete_one({"_id": ObjectId(_id)})

    return {
        "code": 200 if result else 204
    }

@router.get("/report")
async def get_report(_id: str):
    reports = report_list_serial(report.find({"device_id": _id}))
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
async def get_notification(_id: str):
    notifications = notification_list_serial(notification.find({"device_id": _id}))
    return notifications

@router.post("/notification")
async def post_notification(notif: Notification):
    data = dict(notif)
    data['created_at'] = datetime.now()
    result = notification.insert_one(data)
    return {
        "code": 200 if result else 204
    }
    
@router.delete("/notification") 
async def get_notification(_id: str):
    result = notification.delete_one({"device_id": _id})

    return {
        "code": 200 if result else 204
    }

@router.get("/device")
async def get_device():
    devices = device_list_serial(device.find())
    return devices

@router.post("/device")
async def post_device(dev: Device):
    data = dict(dev)
    data['created_at'] = datetime.now()
    data['updated_at'] = datetime.now()
    
    # Check if the Device name is already existed.
    is_existed = device.find_one({'name': data['name']}, {'_id': 0, 'name': 1})
    if is_existed:
        return {
            "code": 409, # 409 means Conflict
            "message": "Device name already existed."
        }    
    
    result = device.insert_one(data)
    return {
        "code": 200 if result else 204,
        "id": str(result.inserted_id)
    }

@router.patch("/device")
async def update_device(dev: Device, _id: str):
    data = dict(dev)
    data["updated_at"] = datetime.now()
    
    # Check if the Device name is already existed before updating.
    is_existed = device.find_one({'name': data['name']}, {'_id': 1, 'name': 1})
    
    if is_existed:
        # if it is not the same ObjectId
        if str(is_existed['_id']) != _id:
            return {
                "code": 409, # 409 means Conflict
                "message": "Device name already existed."
            }
    
    result = device.update_one({"_id": ObjectId(_id)}, {"$set": data})
    return {
        "code": 200 if result else 204
    }

@router.delete("/device")
async def delete_device(_id: str):
    result = device.delete_one({"_id": ObjectId(_id)})

    return {
        "code": 200 if result else 204
    }
    
@router.get("/synctime")
async def sync_time():
    return { "timestamp": int(time.time()) }
    