from app.mqtt_config import connect_mqtt
from app.email_config import send_mail




def publish_mqtt(topic, payload, qos, email=None):
    client = connect_mqtt()
    client.publish(topic=topic, payload=payload, qos=qos)
    if email:
        with open('sucess.html', 'r') as file:
            file_data = file.read()
            send_mail(to=email, subject="IOSync Schedule", mail_body= file_data)
    print("published")
