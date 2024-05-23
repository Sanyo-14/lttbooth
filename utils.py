# utils.py
import sqlite3
def calculate_elo(player_a_elo, player_b_elo, result):
    """Calculate new ELO ratings using the Elo rating system.

    Args:
        player_a_elo (int): Current ELO rating of player A.
        player_b_elo (int): Current ELO rating of player B.
        result (float): Result of the match (1 for player A win, 0 for player B win, 0.5 for a draw).

    Returns:
        tuple: New ELO ratings for player A and player B.
    """
    # (Implement ELO calculation logic here)
    pass


def create_databases():
    """Creates the Behaviour and Gallery databases with the improved structure."""

    conn = sqlite3.connect('treehouse.db')
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Behaviour (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            ELO INTEGER DEFAULT 1000,
            Wins INTEGER DEFAULT 0
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Gallery (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            PathToImage TEXT NOT NULL UNIQUE,
            Name TEXT NOT NULL,
            Description TEXT,
            ELO INTEGER DEFAULT 1000,
            Wins INTEGER DEFAULT 0
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            gallery_id INTEGER, 
            comment_text TEXT NOT NULL,
            FOREIGN KEY (gallery_id) REFERENCES Gallery(id) 
        )
    """)

    conn.commit()
    conn.close()

    print("Databases created successfully!")


def add_behaviour(name, elo=1000, wins=0):
    """Adds a new behaviour to the Behaviour database."""
    conn = sqlite3.connect('treehouse.db')
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO Behaviour(name, ELO, Wins) VALUES (?, ?, ?)", (name, elo, wins))
        conn.commit()
        print(f"Behaviour '{name}' added successfully!")
    except sqlite3.IntegrityError:
        print(f"Error: Behaviour '{name}' already exists in the database.")
    finally:
        conn.close()


def add_gallery_image(path, name, description, elo=1000, wins=0):
    """Adds a new gallery image to the Gallery database."""
    conn = sqlite3.connect('treehouse.db')
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO Gallery(PathToImage, Name, Description, ELO, Wins) VALUES (?, ?, ?, ?, ?)",
                       (path, name, description, elo, wins))
        conn.commit()
        print(f"Gallery image '{name}' added successfully!")
    except sqlite3.IntegrityError:
        print(f"Error: Gallery image with path '{path}' or name '{name}' already exists.")
    finally:
        conn.close()


def add_comment(gallery_name, comment_text):
    """Adds a comment to a gallery image in the Comments database."""
    conn = sqlite3.connect('treehouse.db')
    cursor = conn.cursor()

    # First, get the gallery_id from the Gallery table
    cursor.execute("SELECT id FROM Gallery WHERE Name=?", (gallery_name,))
    gallery_id = cursor.fetchone()

    if gallery_id is None:
        print(f"Error: Gallery image '{gallery_name}' not found.")
        return

    cursor.execute("INSERT INTO Comments(gallery_id, comment_text) VALUES (?, ?)",
                   (gallery_id[0], comment_text))
    conn.commit()
    conn.close()
    print(f"Comment added to gallery image '{gallery_name}' successfully!")

def display_databases():
    """Connects to the database and displays the contents of each table."""

    conn = sqlite3.connect('treehouse.db')
    cursor = conn.cursor()

    # Display Behaviour table
    print("\n--- Behaviour Table ---")
    cursor.execute("SELECT * FROM Behaviour")
    behaviour_data = cursor.fetchall()
    for row in behaviour_data:
        print(f"ID: {row[0]}, Name: {row[1]}, ELO: {row[2]}, Wins: {row[3]})")

    # Display Gallery table
    print("\n--- Gallery Table ---")
    cursor.execute("SELECT * FROM Gallery")
    gallery_data = cursor.fetchall()
    for row in gallery_data:
        print(f"ID: {row[0]}, Path: {row[1]}, Name: {row[2]}, Description: {row[3]}, ELO: {row[4]}, Wins: {row[5]}")

    # Display Comments table
    print("\n--- Comments Table ---")
    cursor.execute("SELECT * FROM Comments")
    comments_data = cursor.fetchall()
    for row in comments_data:
        print(f"ID: {row[0]}, Gallery ID: {row[1]}, Comment: {row[2]}")

    conn.close()


if __name__ == '__main__':
    #create_databases()
    '''
    add_gallery_image('static/images/amazon_law.jpg','Amazon Law','this is a description of amazon law')
    add_gallery_image('static/images/change_happens_fast.jpg', 'Change Happens Fast', 'this is a description of change happens fast')
    add_gallery_image('static/images/law_on_demand.jpg', 'Law On Demand', 'this is a description of law on demand')
    add_gallery_image('static/images/the_source_of_truth.jpg', 'The Source Of Truth', 'this is a description of the source of truth')
    add_comment('Amazon Law', 'this is the future!')
    add_behaviour('agile')
    add_behaviour('persistent')
    add_behaviour('optimistic')
    add_behaviour('tech-savvy')
    '''
    display_databases()

    # Example usage:
    # add_behaviour("Smiling", elo=1250, wins=5)
    # add_gallery_image("images/photo1.jpg", "Courtroom Scene", "A dramatic courtroom scene.")
    # add_comment("Courtroom Scene", "This is an interesting photo!")
