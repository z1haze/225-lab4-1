import sqlite3
import os

DATABASE = '/nfs/demo.db'

def connect_db():
    """Connect to the SQLite database."""
    return sqlite3.connect(DATABASE)

def clear_contacts():
    """Clear all entries in the contacts table."""
    db = connect_db()
    db.execute('DELETE FROM contacts')
    db.commit()
    db.close()

def generate_test_data(num_contacts):
    """Generate test data for the contacts table."""
    db = connect_db()
    for i in range(num_contacts):
        name = f'Test Name {i}'
        phone = f'123-456-789{i}'
        db.execute('INSERT INTO contacts (name, phone) VALUES (?, ?)', (name, phone))
    db.commit()
    print(f'{num_contacts} test contacts added to the database.')
    db.close()

if __name__ == '__main__':
    clear_contacts()  # Uncomment this line if you want to clear the table before inserting new test data.
    generate_test_data(10)  # Generate 10 test contacts.
