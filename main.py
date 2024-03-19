from flask import Flask, request, redirect, url_for, render_template_string
import sqlite3
import os

app = Flask(__name__)

DATABASE = 'demo.db'

def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

def init_db():
    with app.app_context():
        db = get_db()
        db.execute('CREATE TABLE IF NOT EXISTS contacts (id INTEGER PRIMARY KEY, name TEXT, phone TEXT)')
        db.commit()

@app.route('/')
def index():
    # HTML form for submitting a new contact
    form_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Add Contact</title>
    </head>
    <body>
        <h2>Add Contact</h2>
        <form method="POST" action="/add">
            <label for="name">Name:</label><br>
            <input type="text" id="name" name="name" required><br>
            <label for="phone">Phone Number:</label><br>
            <input type="text" id="phone" name="phone" required><br><br>
            <input type="submit" value="Submit">
        </form>
    </body>
    </html>
    """
    return render_template_string(form_html)

@app.route('/add', methods=['GET', 'POST'])
def add_contact():
    if request.method == 'POST':
        try:
            name = request.form['name']
            phone = request.form['phone']
            db = get_db()
            db.execute('INSERT INTO contacts (name, phone) VALUES (?, ?)', (name, phone))
            db.commit()
            return redirect(url_for('index'))
        except Exception as e:
            return f"An error occurred: {e}"
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
