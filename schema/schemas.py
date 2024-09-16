def account_serial(account) -> dict:
    return {
        "id": str(account["_id"]),
        "username": str(account["username"]),
        "password": str(account["password"]),
        "created_at": str(account["created_at"]),
        "updated_at": str(account["updated_at"]),
    }

def account_list_serial(accounts) -> list:
    return [account_serial(account) for account in accounts]

def device_serial(device) -> dict:
    return {
        "id": str(device["_id"]),
        "name": str(device['name']),
        "wifi_ssid": str(device['name']),
        "wifi_mac_address": str(device['name']),
        "password": str(device['name']),
        "created_at": str(device['name']),
        "updated_at": str(device['name'])
    }

def schedule_serial(schedule) -> dict:
    return {
        "id": str(schedule["_id"]),
        "name": str(schedule['name']),
        "time": str(schedule['time']),
        "repeat": str(schedule['repeat']),
        "timer": int(schedule['timer']),
        "is_enable": bool(schedule['is_enable']),
        "created_at": str(schedule['created_at']),
        "updated_at": str(schedule['updated_at'])
    }

def schedule_list_serial(schedules) -> list:
    return [schedule_serial(schedule) for schedule in schedules]

def notification_serial(notification) -> dict:
    return {
        "id": str(notification["_id"]),
        "message": str(notification['message']),
        "created_at": str(notification['created_at']),
    }

def notification_list_serial(notifications) -> list:
    return [notification_serial(notification) for notification in notifications]

def report_serial(report) -> dict:
    return {
        "id": str(report["_id"]),
        "sensor": str(report['sensor']),
        "data": str(report['data']),
        "created_at": str(report['created_at']),
    }

def report_list_serial(reports) -> list:
    return [report_serial(report) for report in reports]

