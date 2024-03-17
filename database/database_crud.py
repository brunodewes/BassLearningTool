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
        c.execute("INSERT INTO user_history (id, name, precision) VALUES (?, ?, ?)", (tab_id, tab_name, precision))

    conn.commit()
    conn.close()


def get_precision_from_tab_id(tab_id):
    conn = sqlite3.connect('./database/database.db')
    c = conn.cursor()

    c.execute("SELECT precision FROM user_history WHERE id=?", (tab_id,))

    record = c.fetchone()
    conn.close()

    if record:
        return record[0]
    else:
        return ""


def get_id_list():
    conn = sqlite3.connect('./database/database.db')
    c = conn.cursor()

    c.execute("SELECT id FROM user_history")

    id_list = c.fetchall()
    conn.close()

    if id_list:
        return id_list
    else:
        return []


def get_tab_name_from_id(tab_id):
    conn = sqlite3.connect('./database/database.db')
    c = conn.cursor()

    c.execute("SELECT name FROM user_history WHERE id=?", (tab_id,))

    tab_name = c.fetchone()
    conn.close()

    if tab_name:
        return tab_name[0]
    else:
        return ""
