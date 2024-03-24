from mqtt_config import c_mqtt


def publish_mqtt(topic, payload, qos):
    c_mqtt.publish(topic=topic, payload=payload, qos=qos)
    print("published")
