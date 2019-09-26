import bson
import re
from apis.models import Device
from .mq_app import MQApp

__all__ = ["app"]

app = MQApp()

@app.route(_type="direct", rule="disconnect")
def disconnect_task(msg):
    payload = bson.decode(msg.body)
    print("disconnect...  msg: %s" % (payload))
    Device.remove_connection(payload)

@app.route(_type="direct", rule="connect")
def connect_task(msg):
    payload = bson.decode(msg.body)
    print("connected...  msg: %s" % (payload))
    Device.add_connection(payload)

    
@app.route(_type="rule", rule="^upload_data/(?P<product_name>.*?)/(?P<device_name>.*?)/(?P<_type>.*?)/(?P<msg_id>.*?$)")
def upload_data_task(msg, product_name, device_name, _type, msg_id):
    print("upload_data: %s" % (msg["payload"]))
    return

@app.route(_type="rule", rule="^update_status/(?P<product_name>.*?)/(?P<device_name>.*?)/(?P<msg_id>.*?$)")
def update_status_task(msg, product_name, device_name, msg_id):
    print("update_status: %s" % msg["payload"])
    return

@app.route(_type="rule", rule="^get/(?P<product_name>.*?)/(?P<device_name>.*?)/(?P<_type>.*?)/(?P<msg_id>.*?$)")
def get_task(msg, product_name, device_name, _type, msg_id):
    print("get: %s" % msg["payload"])
    return

@app.route(_type="rule", rule="^rpc_resp/(?P<product_name>.*?)/(?P<device_name>.*?)/(?P<_type>.*?)/(?P<msg_id>.*?$)")
def rpc_resp_task(msg, product_name, device_name, _type, msg_id):
    print("rpc_resp: %s" % msg["payload"])
    return

@app.route(_type="rule", rule="^cmd_resp/(?P<product_name>.*?)/(?P<device_name>.*?)/(?P<_type>.*?)/(?P<msg_id>.*?$)")
def cmd_resp_task(msg, product_name, device_name, _type, msg_id):
    print("cmd_resp: %s" % msg["payload"])
    return

@app.route(_type="rule", rule="^m2m/(?P<product_name>.*?)/(?P<sender_device>.*?)/(?P<device_name>.*?)/(?P<msg_id>.*?$)")
def m2m_task(msg, product_name, sender_device, device_name, msg_id):
    print("upload_data: %s" % msg["payload"])
    return

@app.route(_type="rule", rule="^updata_ota_status/(?P<product_name>.*?)/(?P<device_name>.*?)/(?P<msg_id>.*?$)")
def upload_ota_task(msg, product_name, device_name, msg_id):
    print("upload_ota: %s" % msg["payload"])
    return

