import paho.mqtt.client as mqtt

c_mqtt = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

@c_mqtt.connect_callback()
def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print(f"Unexpected disconnection from broker. Reconnecting...")
        c_mqtt.reconnect()

c_mqtt.on_disconnect = on_disconnect

c_mqtt.connect('test.mosquitto.org', 1883, 60)



