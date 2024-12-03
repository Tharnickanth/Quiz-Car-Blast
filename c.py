import sqlite3


conn = sqlite3.connect('users.db')
cursor = conn.cursor()
cursor.execute(
    """
    CREATE TABLE game_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    level INTEGER,
    score INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
    """
    )
conn.commit()
conn.close()

