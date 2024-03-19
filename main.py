from flask import Flask, render_template
import os

app = Flask(__name__)

DATABASE = 'database.db'

def get_db():
    db = sqlite3.connect(DATABASE)
    return db

@app.route("/")
def home():
    return render_template('index.html')
    db = get_db()
    # Example operation: Ensure a table exists
    db.execute('CREATE TABLE IF NOT EXISTS my_table (id INTEGER PRIMARY KEY, data TEXT)')
    db.commit()
    return "SQLite3 database has been accessed and ensured 'my_table' exists."

@app.route("/page2")
def page2():
    return render_template('page2.html')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True,host='0.0.0.0',port=port)
