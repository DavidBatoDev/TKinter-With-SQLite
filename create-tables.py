import sqlite3

# Create a connection to the database
connection = sqlite3.connect('movie_house.db')

# Create a cursor object for the connection
c = connection.cursor()

# Delete the tables if they exist, so that we can recreate them
c.execute('DROP TABLE IF EXISTS room')
c.execute('DROP TABLE IF EXISTS movie')
c.execute('DROP TABLE IF EXISTS room_record')
c.execute('DROP TABLE IF EXISTS room_movie_record')

# Create a table room
room_table = """
CREATE TABLE IF NOT EXISTS room (
    id INTEGER PRIMARY KEY,
    cost FLOAT 
)
"""

# Create a table movie
movie_table = """
CREATE TABLE IF NOT EXISTS movie (
    id INTEGER PRIMARY KEY,
    title VARCHAR(255),
    genre VARCHAR(255),
    is_deleted BOOLEAN DEFAULT FALSE,
    cost FLOAT 
)
"""

# Create a table room_record
room_record = """
CREATE TABLE IF NOT EXISTS room_record (
    id INTEGER PRIMARY KEY,
    room_id INTEGER,
    total_cost REAL NOT NULL,
    is_finished BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (room_id) REFERENCES room(id)
)
"""

# Create a table room_movie_record
room_movie_record = """
CREATE TABLE IF NOT EXISTS room_movie_record (
    id INTEGER PRIMARY KEY,
    movie_id INTEGER,
    room_record_id INTEGER,
    FOREIGN KEY (movie_id) REFERENCES movie(id),
    FOREIGN KEY (room_record_id) REFERENCES room_record(id)
)
"""

# Execute the SQL commands
c.execute(room_table)
c.execute(movie_table)
c.execute(room_record)
c.execute(room_movie_record)

# Insert data into the room table (THIS ONE IS NECCESSARY TO RUN THE PROGRAM) please run this to 
c.execute("""
INSERT INTO room (id, cost) VALUES
(1, 100),
(2, 200),
(3, 300),
(4, 400)
""")

# Commit the changes
connection.commit()
