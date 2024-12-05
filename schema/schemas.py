def account_serial(account) -> dict:
    return {
        "id": str(account["_id"]),
        "username": str(account["username"]),
        "password": str(account["password"]),
        "created_at": str(account["created_at"]),
        "updated_at": str(account["created_at"]),
    }

def account_list_serial(accounts) -> list:
    return [account_serial(account) for account in accounts]

def device_serial(device) -> dict:
    return {
        "id": str(device["_id"]),
        "name": str(device['name']),
        "type": str(device['type']),
        "mac_address": str(device['mac_address']),
        "ip_ddress": str(device['ip_ddress']),
        "created_at": str(device['created_at']),
        "updated_at": str(device['updated_at']),
        "account_id": str(device['account_id']),
    }

def schedule_serial(schedule) -> dict:
    return {
        "id": str(schedule["_id"]),
        "name": str(schedule['name']),
        "time": str(schedule['time']),
        "repeat": str(schedule['repeat']),
        "timer": int(schedule['timer']),
        "is_enable": bool(schedule['is_enable']),
        "device_id": str(schedule['device_id']),
        "created_at": str(schedule['created_at']),
        "updated_at": str(schedule['updated_at'])
    }

def schedule_list_serial(schedules) -> list:
    return [schedule_serial(schedule) for schedule in schedules]

def notification_serial(notification) -> dict:
    return {
        "id": str(notification["_id"]),
        "message": str(notification['message']),
        "device_id": str(notification['device_id']),
        "created_at": str(notification['created_at']),
    }

def notification_list_serial(notifications) -> list:
    return [notification_serial(notification) for notification in notifications]

def report_serial(report) -> dict:
    return {
        "id": str(report["_id"]),
        "sensor": str(report['sensor']),
        "data": str(report['data']),
        "device_id": str(report['device_id']),
        "created_at": str(report['created_at']),
    }

def report_list_serial(reports) -> list:
    return [report_serial(report) for report in reports]

def device_serial(device) -> dict:
    return {
        "id": str(device["_id"]),
        "name": str(device['name']),
        "type": str(device['type']),
        "mac_address": str(device['mac_address']),
        "ip_address": str(device['ip_address']),
        "fish_breed": str(device['fish_breed']),
        "temperature": int(device['temperature']),
        "ph_level": int(device['ph_level']),
        "created_at": str(device['created_at']),
        "updated_at": str(device['updated_at']),
    }

def device_list_serial(devices) -> list:
    return [device_serial(device) for device in devices]
