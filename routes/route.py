from fastapi import APIRouter
from models.account import Account, Verify, Reset, UpdateAccount, ResetPassword, Signup, SecurityAnswer, ChangePassword
from models.device import Device
from models.notification import Notification
from models.report import Report
from models.schedule import Schedule
from config import smtp
from config.database import *
from schema.schemas import *
from bson import ObjectId
from datetime import datetime, date
import time, random, bcrypt

router = APIRouter()

@router.get("/account")
async def get_account(_id: str):
    accounts = account_serial(account.find_one({"_id": ObjectId(_id)}))
    return accounts

@router.get("/login")
async def login_account(username: str, password: str):
    result = account.find_one({"username": username.lower()})
    
    if result:
        user = account_password(result)
        try:
            matched = bcrypt.checkpw(password.encode('utf-8'), str(user['password']).encode("utf-8"))
            if matched:
                data = {
                    "id": str(user["id"]),
                    "username": username,
                    "email": user['email'],
                    "is_verified": user['is_verified']
                }
            
                print(data)
        except:
            return {
                "access": False,
                "data": {}
            }
    
    return {
        "access": True if result and matched else False,
        "data": data if result and matched else {}
    }

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
    
@router.post("/signup")
async def signup(acc: Signup):
    data = dict(acc)
    data['username'] = str(data['username']).lower()
    data['email'] = str(data['email']).lower()
    data['password'] = bcrypt.hashpw(str(data['password']).encode('utf-8'), bcrypt.gensalt()).decode("utf-8")

    # check information
    is_found = account_list_serial(account.find({"$or": [
        {"username": data['username'], "is_verified": True},
        {"email": data['email'], "is_verified": True}
    ]}))
    
    if is_found:
        return { "code": 409 }
    
    data['is_verified'] = False
    data['created_at'] = datetime.now()
    data['updated_at'] = datetime.now()
    data['verification_code'] = random.randint(100000, 999999)
    result = account.update_one({"$or": [
        {"username": data['username'], "is_verified": False},
        {"email": data['email'], "is_verified": False}
        ]}, {"$set": data}, upsert=True)
       
    return {
        "code": 200 if result else 204
    }
    
@router.get("/checker")
async def checker():
    return checker_list_serial(account.find({"is_verified": True}))
    
@router.get("/verify")
async def get_verify(id: str):
    userid = ObjectId(id)
    user = account_serial(account.find_one({"_id": userid}))
    result = None
    
    if user:
        code = random.randint(100000, 999999) 
        result = account.update_one({"_id": userid}, {"$set": { "verification_code": code }})
        
        # send email
        await smtp.verification_code_email("AquaAlaga: Verification Code", [user['email']], code)
    
    return {
        "code": 200 if user and result else 204
    }
    
@router.post("/verify")
async def post_verify(verify: Verify):
    data = dict(verify)
    result = account.find_one({"_id": ObjectId(data['id']), "verification_code": int(data['verification_code'])})
    
    if result:
        account.update_one({"_id": ObjectId(data['id'])}, {"$set": { "is_verified": True }})
    
    return {
        "code": 200 if result else 204
    }

@router.get("/find")
async def find_email(email: str):
    is_found = account.find_one({'email': email.lower(), 'is_verified': True}, {'_id': 1})
    
    return {
        "code": 200 if is_found else 204,
        "id": str(is_found['_id']) if is_found else None
    }
    
@router.get("/reset")
async def get_reset(id: str):
    userid = ObjectId(id)
    user = account_serial(account.find_one({"_id": userid}))
    result = None
    
    if user:
        code = random.randint(100000, 999999) 
        result = account.update_one({"_id": userid}, {"$set": { "reset_code": code }})
        
        # send email
        await smtp.reset_code_email("AquaAlaga: Reset Code", [user['email']], code)
    
    return {
        "code": 200 if user and result else 204
    }
    
@router.post("/reset")
async def post_verify(reset: Reset):
    data = dict(reset)
    result = account.find_one({"_id": ObjectId(data['id']), "reset_code": int(data['reset_code'])})
    
    return {
        "code": 200 if result else 204
    }
    
@router.put("/reset")
async def reset_password(acc: ResetPassword):
    data = dict(acc)
    data['password'] = bcrypt.hashpw(str(data['password']).encode('utf-8'), bcrypt.gensalt()).decode("utf-8")
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
    current_password:str = data.pop('current_password')
    
    # Check if the current password matched
    is_found = account.find_one({"_id": ObjectId(acc_id)})
    
    if is_found:
        user = account_password(is_found)
        try:
            matched = bcrypt.checkpw(current_password.encode('utf-8'), str(user['password']).encode("utf-8"))
            if matched:
                data['password'] = bcrypt.hashpw(str(data['password']).encode('utf-8'), bcrypt.gensalt()).decode("utf-8")
                data['updated_at'] = datetime.now()
                
                result = account.update_one({"_id": ObjectId(acc_id)}, {"$set": data})
            
            return {
                "code": 200 if result and matched else 204
            }
        except:
            pass
        
    return {
        "code": 204
    }

@router.get("/schedule")
async def get_schedule(_id: str):
    schedules = schedule_list_serial(schedule.find({'device_id': _id}))
    return schedules

@router.post("/schedule")
async def post_schedule(sched: Schedule):
    data = dict(sched)
    print(data)
    data['created_at'] = datetime.now()
    data['updated_at'] = datetime.now()
    
    # Check if the time schedule is already existed.
    is_existed = schedule.find_one({'device_id': data['device_id'], 'time': data['time']}, {'_id': 0, 'time': 1})
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
    is_existed = schedule.find_one({'device_id': data['device_id'], 'time': data['time']}, {'_id': 1, 'time': 1})
    
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
    result_t = report.insert_one({
        "sensor": "Temperature",
        "data": data['temperature'],
        "device_id": data['id'],
        "created_at": data['created_at']
    })
    result_f = report.insert_one({
        "sensor": "Ultrasonic",
        "data": data['feed'],
        "device_id": data['id'],
        "created_at": data['created_at']
    })
    result_p = report.insert_one({
        "sensor": "pH",
        "data": data['ph_level'],
        "device_id": data['id'],
        "created_at": data['created_at']
    })
    return {
        "code": 200 if result_t and result_f and result_p else 204
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
    result = notification.delete_many({"device_id": _id})

    return {
        "code": 200 if result else 204
    }

@router.get("/device")
async def get_device(_id: str):
    devices = device_list_serial(device.find({"account_id": _id}))
    return devices

@router.get("/find_device")
async def find_device(_id: str):
    res = device.find_one({"_id": ObjectId(_id)})
    devices = device_serial(res) if res else {}
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
