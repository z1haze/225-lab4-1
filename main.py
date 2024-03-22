from flask import Flask, request, render_template_string, redirect, url_for
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

@app.route('/')
def home():
    # Fetch all contacts to display
    db = get_db()
    contacts = db.execute('SELECT * FROM contacts').fetchall()
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Contacts Home</title>
        </head>
        <body>
            <h2>Contacts</h2>
            <a href="{{ url_for('add_contact') }}">Add New Contact</a>
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
                <p>No contacts found. Add a new contact.</p>
            {% endif %}
        </body>
        </html>
    ''', contacts=contacts)

@app.route('/add', methods=['GET', 'POST'])
def add_contact():
    message = ''
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        if name and phone:
            db = get_db()
            db.execute('INSERT INTO contacts (name, phone) VALUES (?, ?)', (name, phone))
            db.commit()
            return redirect(url_for('home'))
        else:
            message = 'Name and phone number are required.'

    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Add Contact</title>
        </head>
        <body>
            <h2>Add Contact</h2>
            <form method="POST" action="{{ url_for('add_contact') }}">
                <label for="name">Name:</label><br>
                <input type="text" id="name" name="name" required><br>
                <label for="phone">Phone Number:</label><br>
                <input type="text" id="phone" name="phone" required><br><br>
                <input type="submit" value="Add Contact">
            </form>
            <p>{{ message }}</p>
            <a href="{{ url_for('home') }}">Back to Contacts</a>
        </body>
        </html>
    ''', message=message)

@app.route('/modify/<int:contact_id>', methods=['GET', 'POST'])
def modify_contact(contact_id):
    # ... existing modify_contact code ...

@app.route('/delete/<int:contact_id>')
def delete_contact(contact_id):
    db = get_db()
    db.execute('DELETE FROM contacts WHERE id = ?', (contact_id,))
    db.commit()
    return redirect(url_for('home'))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    init_db()  # Initialize the database and table
    app.run(debug=True, host='0.0.0.0', port=port)
