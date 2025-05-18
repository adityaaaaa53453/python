from flask import Blueprint, request, jsonify
from models import db, Notification
from service import save_notification, send_to_queue

bp = Blueprint('api', __name__)

@bp.route('/notifications', methods=['POST'])
def send_notification():
    data = request.json
    required_fields = ['user_id', 'type', 'message']
    if not all(k in data for k in required_fields):
        return {'error': 'Missing fields'}, 400

    save_notification(data['user_id'], data['type'], data['message'])
    send_to_queue(data)
    return {'status': 'Notification queued'}, 200

@bp.route('/users/<int:user_id>/notifications', methods=['GET'])
def get_user_notifications(user_id):
    notifications = Notification.query.filter_by(user_id=user_id).all()
    return jsonify([{
        'id': n.id,
        'type': n.type,
        'message': n.message,
        'timestamp': n.timestamp.isoformat()
    } for n in notifications])
