from flask import Flask, request, jsonify
from uuid import uuid4
from collections import defaultdict

app = Flask(__name__)

# In-memory storage for notifications
notifications_db = defaultdict(list)

# Supported notification types
NOTIFICATION_TYPES = {"email", "sms", "in-app"}

@app.route('/notifications', methods=['POST'])
def send_notification():
    data = request.json
    user_id = data.get("user_id")
    notification_type = data.get("type")
    message = data.get("message")

    if not user_id or not notification_type or not message:
        return jsonify({"error": "Missing required fields: user_id, type, message"}), 400
    
    if notification_type not in NOTIFICATION_TYPES:
        return jsonify({"error": f"Unsupported notification type. Supported types: {NOTIFICATION_TYPES}"}), 400

    # Create a notification entry
    notification = {
        "id": str(uuid4()),
        "type": notification_type,
        "message": message,
        "status": "pending"  # you could update status later (e.g., sent, failed)
    }

    # Save notification to "DB"
    notifications_db[user_id].append(notification)

    # Here you would add logic to send the notification asynchronously (queue etc.)
    # For now, we just simulate sending by setting status to sent
    notification["status"] = "sent"

    return jsonify({"message": "Notification sent", "notification": notification}), 201


@app.route('/users/<user_id>/notifications', methods=['GET'])
def get_user_notifications(user_id):
    user_notifications = notifications_db.get(user_id, [])
    return jsonify(user_notifications), 200


if __name__ == '__main__':
    app.run(debug=True)
