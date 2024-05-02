from flask import Flask, request, jsonify, send_from_directory
import os
from db.database import init_app, create_event, get_db

app = Flask(__name__, static_folder='../frontend/build', static_url_path='/')

# Initialize the database
init_app(app)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        # Serve the specified path if it exists and is not a directory
        return send_from_directory(app.static_folder, path)
    else:
        # Serve index.html by default
        return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/events', methods=['POST'])
def create_new_event():
    data = request.get_json()
    print("Received data:", data)  # 打印接收到的数据
    if not data:
        return jsonify({"error": "No data provided"}), 400
    required_fields = ['title', 'start_time', 'end_time', 'location', 'description', 'category']
    if not all(field in data for field in required_fields):
        print("Missing fields:", [field for field in required_fields if field not in data])  # 打印缺失的字段
        return jsonify({"error": "Missing required fields"}), 400
    
    try:
        result = create_event(data)
        if result:
            return jsonify({"message": "Event created successfully", "event": result}), 201
        else:
            return jsonify({"error": "Failed to create event"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/api/events', methods=['GET'])
def get_events():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM events")
    events = cursor.fetchall()
    cursor.close()
    return jsonify(events)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
