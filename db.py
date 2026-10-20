import sqlite3

def initialize_database():
    connection = sqlite3.connect("volleytrack.db")
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS matches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            opponent TEXT NOT NULL,
            sets_played INTEGER NOT NULL,
            kills INTEGER NOT NULL,
            attack_errors INTEGER NOT NULL,
            attack_attempts INTEGER NOT NULL,
            assists INTEGER NOT NULL,
            digs INTEGER NOT NULL,
            aces INTEGER NOT NULL,
            blocks INTEGER NOT NULL
        )
    ''')

    connection.commit()
    connection.close()

def save_match(match):
    connection = sqlite3.connect("volleytrack.db")
    cursor = connection.cursor()

    cursor.execute('''
        INSERT INTO matches (
            opponent, sets_played, kills, attack_errors, attack_attempts,
            assists, digs, aces, blocks
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        match["opponent"], match["sets_played"], match["kills"],
        match["attack_errors"], match["attack_attempts"], match["assists"],
        match["digs"], match["aces"], match["blocks"]
    ))

    connection.commit()
    connection.close()

def load_matches():
    connection = sqlite3.connect("volleytrack.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM matches")
    rows = cursor.fetchall()

    matches = [dict(row) for row in rows]

    connection.close()
    return matches

def delete_match(match_id):
    connection = sqlite3.connect("volleytrack.db")
    cursor = connection.cursor()

    cursor.execute("DELETE FROM matches WHERE id = ?", (match_id,))

    connection.commit()
    connection.close()

if __name__ == "__main__":
    initialize_database()

    matches = load_matches()
    print(f"Total saved matches: {len(matches)}")

    for match in matches:
        print(match)
