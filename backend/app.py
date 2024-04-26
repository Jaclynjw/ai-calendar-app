from flask import Flask, request, jsonify, send_from_directory
import os
from db.database import init_app

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
