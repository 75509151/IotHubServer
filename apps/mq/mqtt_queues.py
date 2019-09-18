from kombu import Exchange, Queue
mqtt_exchange = Exchange('mqtt.events', type='direct')
disconnect_queue = Queue('disconnected', mqtt_exchange, routing_key='client.disconnected')
connect_queue = Queue('connected', mqtt_exchange, routing_key='client.connected')
publish_queue = Queue('publish', mqtt_exchange, routing_key='message.publish')
