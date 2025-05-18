import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:Aditya@42@localhost:5432/notification_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    RABBITMQ_QUEUE = 'notification_queue'
    RABBITMQ_URL = 'amqp://guest:guest@localhost:5672/'
