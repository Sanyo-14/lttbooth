# utils.py
import sqlite3
import base64
import os
import openai

from openai import OpenAI
def calculate_elo(player_a_elo, player_b_elo, result):
    """Calculate new ELO ratings using the Elo rating system.

    Args:
        player_a_elo (int): Current ELO rating of player A.
        player_b_elo (int): Current ELO rating of player B.
        result (float): Result of the match (1 for player A win, 0 for player B win, 0.5 for a draw).

    Returns:
        tuple: New ELO ratings for player A and player B.
    """
    k_factor = 32  # You can adjust the K-factor as needed

    # Calculate expected scores
    expected_a = 1 / (1 + 10 ** ((player_b_elo - player_a_elo) / 400))
    expected_b = 1 / (1 + 10 ** ((player_a_elo - player_b_elo) / 400))

    # Calculate new ELO ratings
    new_elo_a = round(player_a_elo + k_factor * (result - expected_a))
    new_elo_b = round(player_b_elo + k_factor * ((1 - result) - expected_b))

    return new_elo_a, new_elo_b


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
            PathToImage TEXT NOT NULL,
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
    #except sqlite3.IntegrityError:
        #print(f"Error: Gallery image with path '{path}' or name '{name}' already exists.")
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

def update_gallery_elo_wins(name, new_elo, new_wins):
    """Updates the ELO and Wins for a gallery image."""
    conn = sqlite3.connect('treehouse.db')
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE Gallery SET ELO = ?, Wins = ? WHERE Name = ?",
                       (new_elo, new_wins, name))
        conn.commit()
        print(f"Gallery image '{name}' updated successfully!")
    except Exception as e:
        print(f"Error updating gallery image '{name}': {e}")
    finally:
        conn.close()


def update_behaviour_elo_wins(name, new_elo, new_wins):
    """Updates the ELO and Wins for a behaviour."""
    conn = sqlite3.connect('treehouse.db')
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE Behaviour SET ELO = ?, Wins = ? WHERE name = ?",
                       (new_elo, new_wins, name))
        conn.commit()
        print(f"Behaviour '{name}' updated successfully!")
    except Exception as e:
        print(f"Error updating behaviour '{name}': {e}")
    finally:
        conn.close()

def get_gallery_elo_wins(name):
    """Retrieves the ELO and Wins for a gallery image.

    Args:
        name (str): The name of the gallery image.

    Returns:
        tuple: A tuple containing the ELO and Wins (ELO, Wins) or None if the image is not found.
    """
    conn = sqlite3.connect('treehouse.db')
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT ELO, Wins FROM Gallery WHERE Name = ?", (name,))
        result = cursor.fetchone()
        return result if result else None
    except Exception as e:
        print(f"Error retrieving data for gallery image '{name}': {e}")
        return None
    finally:
        conn.close()


def get_behaviour_elo_wins(name):
    """Retrieves the ELO and Wins for a behaviour.

    Args:
        name (str): The name of the behaviour.

    Returns:
        tuple: A tuple containing the ELO and Wins (ELO, Wins) or None if the behaviour is not found.
    """
    conn = sqlite3.connect('treehouse.db')
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT ELO, Wins FROM Behaviour WHERE name = ?", (name,))
        result = cursor.fetchone()
        return result if result else None
    except Exception as e:
        print(f"Error retrieving data for behaviour '{name}': {e}")
        return None
    finally:
        conn.close()

def get_gallery_leaderboard(limit=10):
    """Returns a leaderboard of gallery images sorted by ELO.

    Args:
        limit (int, optional): The maximum number of entries to return.
                             Defaults to 10.

    Returns:
        list: A list of lists, where each inner list represents a gallery image
              and its data in the format [PathToImage, Name, ELO, Wins].
    """
    conn = sqlite3.connect('treehouse.db')
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT PathToImage, Name, ELO, Wins FROM Gallery ORDER BY ELO DESC LIMIT ?", (limit,))
        leaderboard = cursor.fetchall()
        return leaderboard
    except Exception as e:
        print(f"Error retrieving gallery leaderboard: {e}")
        return []
    finally:
        conn.close()


def get_behaviour_leaderboard(limit=10):
    """Returns a leaderboard of behaviours sorted by ELO.

    Args:
        limit (int, optional): The maximum number of entries to return.
                             Defaults to 10.

    Returns:
        list: A list of lists, where each inner list represents a behaviour
              and its data in the format [name, ELO, Wins].
    """
    conn = sqlite3.connect('treehouse.db')
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT name, ELO, Wins FROM Behaviour ORDER BY ELO DESC LIMIT ?", (limit,))
        leaderboard = cursor.fetchall()
        return leaderboard
    except Exception as e:
        print(f"Error retrieving behaviour leaderboard: {e}")
        return []
    finally:
        conn.close()

def get_random_items(table_name, num_items=2):
    """Retrieves random items (images or behaviours) from the specified table.

    Args:
        table_name (str): The name of the table to retrieve items from
                          ('Gallery' for images, 'Behaviour' for behaviours).
        num_items (int, optional): The number of random items to retrieve.
                                  Defaults to 2.

    Returns:
        list: A list of random items.
              - If table_name is 'Gallery', each item is a list:
                [PathToImage, Name, Description]
              - If table_name is 'Behaviour', each item is a string (behaviour name).
              Returns an empty list if there's an error or no items found.
    """

    conn = sqlite3.connect('treehouse.db')
    cursor = conn.cursor()
    try:
        if table_name == 'Gallery':
            cursor.execute(f"SELECT PathToImage, Name, Description FROM Gallery ORDER BY RANDOM() LIMIT {num_items}")
            return cursor.fetchall()
        elif table_name == 'Behaviour':
            cursor.execute(f"SELECT name FROM Behaviour ORDER BY RANDOM() LIMIT {num_items}")
            return [row[0] for row in cursor.fetchall()]  # Extract names from tuples
        else:
            print(f"Invalid table name: {table_name}")
            return []
    except Exception as e:
        print(f"Error retrieving random items from {table_name}: {e}")
        return []
    finally:
        conn.close()


client = OpenAI(api_key='sk-proj-iqIenJ2D7p99oMUc5wj4T3BlbkFJE5U3pmE8PquPiTcAt4v3')

# Set your OpenAI API key here
openai.api_key = os.getenv('OPENAI_API_KEY')




def generate_and_save_image(title, description, specific_elements, additional_details, output_image_path):
    """Generates an image using DALL-E 3 and saves it to the specified path.

    Args:
        title (str): The title of the image.
        description (str): A description of the image.
        specific_elements (str): Specific elements to include in the image.
        additional_details (str): Additional details for the image.
        output_image_path (str): The path to save the generated image.
    """

    prompt = f'A detailed cartoon image in a black and white style with red accents. The image is titled "{title}" and portrays {description} The scene should include specific elements such as {specific_elements} and additional details like {additional_details}. The overall composition should maintain a satirical and humorous tone, similar to the style of an old newspaper/cartoon.'


    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
        response_format="b64_json"
    )

    try:
        image_data = response.data[0].b64_json
        decoded_image = base64.b64decode(image_data)
        with open(output_image_path, 'wb') as f:
            f.write(decoded_image)
        print(f"Image saved as {output_image_path}")

    except KeyError:
        print(f"Error: 'b64_json' field not found in response. Response: {response}")


def generate_image_details(title, description=""):
    """Generates details for an image based on the title and description.

    Args:
        title (str): The title of the image.
        description (str): A description of the image (can be empty).

    Returns:
        tuple: A tuple containing the description, specific_elements, additional_details, file path, and database path.
    """

    # Default values
    specific_elements = generate_text(description, 'specific elements')
    additional_details = generate_text(description, 'additional details')
    file_path = f"static/images/{title.replace(' ', '_')}.jpg"
    database_path = f"images/{title.replace(' ', '_')}.jpg"

    # Generate a description if none is provided

    description_full = f"A depiction of the concept '{title}'. {description}"

    return description_full, specific_elements, additional_details, file_path, database_path


def generate_text(prompt, type):
    response = client.chat.completions.create(
        model="gpt-4o",
        # or the engine you are using
        messages=[
            {"role": "system", "content": f'You describe {type} of a given scene. keep it short.'},
            {"role": "user", "content": prompt}
        ]
    )
    # Extract the text from the response
    text = response.choices[0].message.content
    return text

if __name__ == '__main__':
    '''create_databases()

    add_gallery_image('images/amazon_law.jpg','Amazon Law','this is a description of amazon law')
    add_gallery_image('images/change_happens_fast.jpg', 'Change Happens Fast', 'this is a description of change happens fast')
    add_gallery_image('images/law_on_demand.jpg', 'Law On Demand', 'this is a description of law on demand')
    add_gallery_image('images/the_source_of_truth.jpg', 'The Source Of Truth', 'this is a description of the source of truth')
    add_comment('Amazon Law', 'this is the future!')
    add_behaviour('agile')
    add_behaviour('persistent')
    add_behaviour('optimistic')
    add_behaviour('tech-savvy')'''

    #display_databases()
    name = "netflix law"
    description = "on demand feed of documents on all your devices at home"
    description_full, specific_elements, additional_details, file_path, database_path = generate_image_details(name,
                                                                                                               description)
    generate_and_save_image(name, description_full, specific_elements, additional_details,
                            file_path)
    #print(get_random_items('Gallery'))
    # Example usage:
    # add_behaviour("Smiling", elo=1250, wins=5)
    # add_gallery_image("images/photo1.jpg", "Courtroom Scene", "A dramatic courtroom scene.")
    # add_comment("Courtroom Scene", "This is an interesting photo!")
