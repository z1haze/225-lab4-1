from flask import Flask, render_template
import os
import sqlite3

app = Flask(__name__)

DATABASE = 'demo.db'

def get_db():
    db = sqlite3.connect(DATABASE)
    return db

@app.route("/")
def home():
    db = get_db()
    # Ensure the table exists
    db.execute('CREATE TABLE IF NOT EXISTS my_table (id INTEGER PRIMARY KEY, data TEXT)')
    db.commit()
    
    # Fetch data from the table
    cursor = db.execute('SELECT id, data FROM my_table')
    rows = cursor.fetchall()  # This gets all rows of the query result
    
    # Pass the data to the template
    return render_template('index.html', rows=rows)

@app.route("/page2")
def page2():
    return render_template('page2.html')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)

