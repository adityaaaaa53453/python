from models import db, Notification
import pika
import json
from config import Config

def save_notification(user_id, notif_type, message):
    notif = Notification(user_id=user_id, type=notif_type, message=message)
    db.session.add(notif)
    db.session.commit()
    return notif

def send_to_queue(data):
    connection = pika.BlockingConnection(pika.URLParameters(Config.RABBITMQ_URL))
    channel = connection.channel()
    channel.queue_declare(queue=Config.RABBITMQ_QUEUE, durable=True)
    channel.basic_publish(
        exchange='',
        routing_key=Config.RABBITMQ_QUEUE,
        body=json.dumps(data),
        properties=pika.BasicProperties(delivery_mode=2),
    )
    connection.close()
