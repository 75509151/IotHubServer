import json
from bson.objectid import ObjectId

from django.conf import settings

from utils.mongo import Mongo


# TODO: MongoModel

class MongoMixin():
    CLIENT = Mongo(settings.MONGO_URL, settings.MONGO_PORT)
    COLLECTION = None

    @classmethod
    def find(cls, condition):
        return cls.COLLECTION.find(condition)

    @classmethod
    def find_one(cls, condition=None):
        return cls.COLLECTION.find_one(condition)

    @classmethod
    def insert_one(cls, doc):
        return cls.COLLECTION.insert_one(doc)

    @classmethod
    def delete_one(cls, condition):
        return cls.COLLECTION.delete_one(condition)


    @classmethod
    def delete_many(cls, condition):
        return cls.COLLECTION.delete_many(condition)


class Device(MongoMixin):
    CLIENT = Mongo(settings.MONGO_URL, settings.MONGO_PORT)
    COLLECTION = CLIENT["mqtt"]["devices"]

    def __init__(self, product_name,
                 device_name,
                 username,
                 password,
                 status="",
                 device_status="{}",
                 last_status_update=0,
                 tags=None,
                 tags_version=1,
                 shadow=None,
                 _id=None):

        self.product_name = product_name
        self.device_name = device_name
        self.username = username
        self.password = password
        self.status = status  # 可接入状态
        self.device_status = device_status
        self.last_status_update = last_status_update  # ("最新更新时间")
        self.tags = tags if tags is not None else []
        self.tags_version = tags_version
        self.shadow = shadow if shadow is not None else json.dumps({"state": {}, "metadata": {}, "version": 0})
        self._id = _id


    def to_doc(self):
        if self._id:
            return {"product_name": self.product_name,
                    "device_name": self.device_name,
                    "username": self.username,
                    "password": self.password,
                    "status": self.status,
                    "device_status": self.device_status,
                    "last_status_update": self.last_status_update,
                    "tags": self.tags,
                    "tags_version": self.tags_version,
                    "shadow": self.shadow,
                    "_id": self._id}
        else:
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



    def get_acl(self):
        publish = [
            "upload_data/{product_name}/{device_name}/+/+".format(product_name=self.product_name,
                                                                  device_name=self.device_name),
            "update_status/{product_name}/{device_name}/+".format(product_name=self.product_name,
                                                                  device_name=self.device_name),
            "cmd_resp/{product_name}/{device_name}/+/+/+".format(product_name=self.product_name,
                                                                 device_name=self.device_name),
            "rpc_resp/{product_name}/{device_name}/+/+/+".format(product_name=self.product_name,
                                                                 device_name=self.device_name),
            "get/{product_name}/{device_name}/+/+".format(product_name=self.product_name,
                                                          device_name=self.device_name),
            "m2m/{product_name}/+/{device_name}/+".format(product_name=self.product_name,
                                                          device_name=self.device_name),
            "update_ota_status/{product_name}/{device_name}/+".format(product_name=self.product_name,
                                                                      device_name=self.device_name),
        ]
        subscribe = ["tags/{product_name}/+/cmd/+/+/+/#".format(product_name=self.product_name)]
        pubsub = []
        return {
            "publish": publish,
            "subscribe": subscribe,
            "pubsub": pubsub
        }

    def disconnect(self):
        if self._id:
            pass

    def remove(self):
        if self._id:
            _id = ObjectId(self._id)
            Device.delete_one({"_id": _id})
            DeviceAcl.delete_many({"username": self.username})
            Connections.delete_many({"device":_id})

class DeviceAcl(MongoMixin):
    CLIENT = Mongo(settings.MONGO_URL, settings.MONGO_PORT)
    COLLECTION = CLIENT["mqtt"]["device_acl"]

    def __init__(self, username, publish,
                subscribe, pubsub):
        self.username = username
        self.publish = publish
        self.subscribe = subscribe
        self.pubsub = pubsub

    def to_doc(self):
        return {
            "username": self.username,
            "publish": self.publish,
            "subscribe": self.subscribe,
            "pubsub": self.pubsub
        }



class Connections(MongoMixin):
    CLIENT = Mongo(settings.MONGO_URL, settings.MONGO_PORT)
    COLLECTION = CLIENT["mqtt"]["connections"]
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
