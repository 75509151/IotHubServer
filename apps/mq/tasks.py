import bson
from apis.models import Device

def disconnect_task(msg):
    payload = bson.decode(msg.body)
    print("disconnect...  msg: %s" % (payload))
    Device.remove_connection(payload)

def connect_task(msg):
    payload = bson.decode(msg.body)
    print("connected...  msg: %s" % (payload))
    Device.add_connection(payload)


def msg_task(msg):
    payload = bson.decode(msg.body)
    print("msg...  msg: %s" % (payload))

