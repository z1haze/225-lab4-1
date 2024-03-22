from flask import Flask, request, jsonify, render_template_string, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# Database file path
DATABASE = '/nfs/demo.db'

def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row  # This enables name-based access to columns
    return db

def init_db():
    with app.app_context():
        db = get_db()
        db.execute('''
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL
            );
        ''')
        db.commit()

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ''  # Message indicating the result of the operation
    contacts = []
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        if name and phone:
            db = get_db()
            db.execute('INSERT INTO contacts (name, phone) VALUES (?, ?)', (name, phone))
            db.commit()
            message = 'Contact added successfully.'
        else:
            message = 'Missing name or phone number.'

    # Always display the contacts table
    db = get_db()
    contacts = db.execute('SELECT * FROM contacts').fetchall()

    # Display the HTML form along with the contacts table
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Add Contact</title>
        </head>
        <body>
            <h2>Add Contact</h2>
            <form method="POST" action="/">
                <label for="name">Name:</label><br>
                <input type="text" id="name" name="name" required><br>
                <label for="phone">Phone Number:</label><br>
                <input type="text" id="phone" name="phone" required><br><br>
                <input type="submit" value="Submit">
            </form>
            <p>{{ message }}</p>
            {% if contacts %}
                <table border="1">
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Phone Number</th>
                        <th>Actions</th>
                    </tr>
                    {% for contact in contacts %}
                        <tr>
                            <td>{{ contact['id'] }}</td>
                            <td>{{ contact['name'] }}</td>
                            <td>{{ contact['phone'] }}</td>
                            <td>
                                <a href="{{ url_for('modify_contact', contact_id=contact['id']) }}">Modify</a> |
                                <a href="{{ url_for('delete_contact', contact_id=contact['id']) }}">Delete</a>
                            </td>
                        </tr>
                    {% endfor %}
                </table>
            {% else %}
                <p>No contacts found.</p>
            {% endif %}
        </body>
        </html>
    ''', message=message, contacts=contacts)

@app.route('/modify/<int:contact_id>', methods=['GET', 'POST'])
def modify_contact(contact_id):
    db = get_db()
    contact = db.execute('SELECT * FROM contacts WHERE id = ?', (contact_id,)).fetchone()

    # If the contact doesn't exist, redirect to the index
    if contact is None:
        return redirect(url_for('index'))

    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        db.execute('UPDATE contacts SET name = ?, phone = ? WHERE id = ?', (name, phone, contact_id))
        db.commit()
        return redirect(url_for('index'))

    # Show a form to modify a contact
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Modify Contact</title>
        </head>
        <body>
            <h2>Modify Contact</h2>
            <form method="POST" action="{{ url_for('modify_contact', contact_id=contact['id']) }}">
                <label for="name">Name:</label><br>
                <input type="text" id="name" name="name" value="{{ contact['name'] }}" required><br>
                <label for="phone">Phone Number:</label><br>
                <input type="text" id="phone" name="phone" value="{{ contact['phone'] }}" required><br><br>
                <input type="submit" value="Save Changes">
            </form>
        </body>
        </html>
