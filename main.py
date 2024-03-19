from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)

# Database file path
DATABASE = 'demo.db'

def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row  # This enables name-based access to columns
    return db

def init_db():
    with app.app_context():
        db = get_db()
        db.execute('CREATE TABLE IF NOT EXISTS contacts (id INTEGER PRIMARY KEY, name TEXT, phone TEXT)')
        db.commit()

@app.route('/')
def index():
    return "Welcome to the Flask SQLite app. Use /add?name=NAME&phone=PHONE to add a contact."

@app.route('/add')
def add_contact():
    name = request.args.get('name', '')
    phone = request.args.get('phone', '')
    if not name or not phone:
        return "Missing name or phone number", 400
    
    db = get_db()
    db.execute('INSERT INTO contacts (name, phone) VALUES (?, ?)', (name, phone))
    db.commit()
    return jsonify({"success": True, "message": "Contact added successfully."})

@app.route('/contacts')
def list_contacts():
    db = get_db()
    contacts = db.execute('SELECT * FROM contacts').fetchall()
    return jsonify([{"id": row["id"], "name": row["name"], "phone": row["phone"]} for row in contacts])

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    init_db()  # Initialize the database and table
    app.run(debug=True, host='0.0.0.0', port=port)

