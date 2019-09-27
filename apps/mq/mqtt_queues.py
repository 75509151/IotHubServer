from kombu import Exchange, Queue, Connection
#TODO:
KEY =  "iothub"
AMQ_URI = 'amqp://guest:guest@localhost:5672//'

conn = Connection(AMQ_URI)



mqtt_exchange = Exchange('mqtt.events', type='direct')
disconnect_queue = Queue('disconnected', mqtt_exchange, routing_key='client.disconnected')
connect_queue = Queue('connected', mqtt_exchange, routing_key='client.connected')
publish_queue = Queue('publish', mqtt_exchange, routing_key='message.publish')


iot_upload_data_exchange = Exchange("iothub.events.upload_data", type="direct")
upload_data_queue = Queue("iot_upload_data", iot_upload_data_exchange,
                          routing_key=KEY)

iot_upload_status_exchange = Exchange("iothub.events.upload_status", type="direct")
upload_status_queue = Queue("iot_upload_status", iot_upload_status_exchange,
       routing_key=KEY )

iot_cmd_res_exchange = Exchange("iothub.events.cmd_res", type="direct")
cmd_res_queue = Queue("iot_cmd_res", iot_cmd_res_exchange,
       routing_key=KEY)

iot_data_request_exchange = Exchange("iothub.events.data_request", type="direct")
data_request_queue = Queue("data_request", iot_data_request_exchange,
        routing_key=KEY)

with conn:
    upload_data_queue(conn).declare()
    upload_status_queue(conn).declare()
    cmd_res_queue(conn).declare()
    data_request_queue(conn).declare()


