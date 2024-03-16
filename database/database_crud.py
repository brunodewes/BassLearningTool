import sqlite3


def create_database():
    conn = sqlite3.connect('./database/database.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS user_history
                 (id TEXT, name TEXT, precision TEXT)''')

    conn.commit()
    conn.close()


def update_database(tab_id, tab_name, precision):
    conn = sqlite3.connect('./database/database.db')
    c = conn.cursor()

    # Check if tab_id already exists in the database
    c.execute("SELECT * FROM user_history WHERE id=?", (tab_id,))
    existing_row = c.fetchone()

    if existing_row:
        # Update the precision for the existing tab_id
        c.execute("UPDATE user_history SET precision=? WHERE id=?", (precision, tab_id))
    else:
        # Insert a new row with the tab_id and precision
        c.execute("INSERT INTO user_history (id, name, precision) VALUES (?, ?)", (tab_id, tab_name, precision))

    conn.commit()
    conn.close()


def query_database(tab_id):
    conn = sqlite3.connect('./database/database.db')
    c = conn.cursor()

    c.execute("SELECT precision FROM user_history WHERE id=?", (tab_id,))

    record = c.fetchone()
    conn.close()

    if record:
        return record
    else:
        return "0.00"
