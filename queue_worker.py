import pika, json, time
from models import db, Notification
from config import Config
from flask import Flask

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

def callback(ch, method, properties, body):
    data = json.loads(body)
    print(f"Processing notification: {data}")
    # Retry logic can go here
    ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    connection = pika.BlockingConnection(pika.URLParameters(Config.RABBITMQ_URL))
    channel = connection.channel()
    channel.queue_declare(queue=Config.RABBITMQ_QUEUE, durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=Config.RABBITMQ_QUEUE, on_message_callback=callback)

    print("Waiting for messages...")
    channel.start_consuming()

if __name__ == "__main__":
    main()
