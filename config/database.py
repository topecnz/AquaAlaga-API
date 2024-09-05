from pymongo import MongoClient
from dotenv import dotenv_values

config = dotenv_values(".env")


try:
    client = MongoClient(config["ATLAS_URI"])
    db = client['aqua_alaga']
    print('MongoDB Database connected!')
except:
    print('MongoDB not connected.')

account = db['account']
device = db['device']
report = db['report']
notification = db['notification']
schedule = db['schedule']
