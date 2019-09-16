import json
from django.conf import settings

from utils.mongo import Mongo


#TODO: MongoModel



class Device():
    CLIENT = Mongo(settings.MONGO_URL, settings.MONGO_PORT)
    COLLECTION = CLIENT["mqtt"]["device"]

    def init(self, product_name,
                 device_name,
                 username,
                 password,
                 status="",
                 device_status="{}",
                 last_status_update=0,
                 tags=None,
                 tags_version = 1,
                 shadow=None):

        self.product_name = product_name
        self.device_name = device_name
        self.username = username
        self.password = password
        self.status = status  # 可接入状态
        self.device_status = device_status
        self.last_status_update = last_status_update #("最新更新时间")
        self.tags = tags if tags is not None else []
        self.tags_version = tags_version
        self.shadow = shadow if shadow is not None else json.dumps({"state": {},"metadata": {},"version":0})
        return self

    def to_doc(self):
        return {"product_name": self.product_name,
                "device_name": self.device_name,
                "username": self.username,
                "password": self.password,
                "status": self.status,
                "device_status": self.device_status,
                "last_status_update": self.last_status_update,
                "tags": self.tags,
                "tags_version": self.tags_version,
                "shadow": self.shadow}

    @classmethod
    def find(cls, condition):
        return cls.COLLECTION.find(condition)

    @classmethod
    def find_one(cls, condition=None):
        return cls.COLLECTION.find_one(condition=None)

    def insert_one(self):
        return Device.COLLECTION.insert_one(self.to_doc())


class Connections(object):
    def __init__(self, client_id, connected,
                 device,
                 connected_at,
                 keepalive,
                 ipaddress
                 ):
        self.client_id = client_id
        self.device = device
        self.connected = connected
        self.keepalive = keepalive
        self.ipaddress = ipaddress
        self.connected_at = connected_at




