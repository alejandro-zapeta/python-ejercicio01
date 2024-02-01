from tinydb import TinyDB, Query
from flask import Flask, request, jsonify
from src.auth.auth_middleware import token_required
from flask_cors import CORS

db = TinyDB('/tinydb/exercise1')
leads = db.table('lead')
app = Flask(__name__)
CORS(app)

@app.route("/api/lead", methods=['POST'])
@token_required
def create_lead():
    lead_payload = request.json
    leads.insert(lead_payload)
    return jsonify({'status': 200})

@app.route("/api/lead", methods=['GET'])
@token_required
def get_leads():
    return jsonify({'status': 200, 'data': leads.all()})

if __name__ == '__main__':
    app.run(host= '0.0.0.0', debug=True)