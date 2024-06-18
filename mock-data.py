import sqlite3

conn = sqlite3.connect('movie_house.db')
c = conn.cursor()

# If error occurs, delete the database file (run the create-tables.py script)
# run the create-tables.py script to create the tables

# PRACTICE DATA
#############################  NOT NECESSARY TO RUN THE PROGRAM     ##########################################

# Insert data into the movie table (NOT NECCESSARY TO RUN THE PROGRAM)
c.execute("""
INSERT INTO movie (id, title, genre, cost) VALUES
(1, 'How to make millions before grandma dies', 'Tragedy', 100),
(2, 'Inside Out2', 'Fantasy', 200),
(3, 'Private Benjamin', 'Comedy', 300),
(4, 'Adventure Time', 'Adventure', 400),
(5, 'Start Up', 'Romance', 500)
""")


# Insert data into the room_record table (NOT NECCESSARY TO RUN THE PROGRAM)
c.execute("""
INSERT INTO room_record (id, room_id, total_cost, is_finished) VALUES
(1, 1, 0, 1),
(2, 2, 0, 1),
(3, 3, 0, 1),
(4, 4, 0, 1),
(5, 5, 0, 1)
""")

# Insert data into the room_movie_record table (NOT NECCESSARY TO RUN THE PROGRAM)
c.execute("""
INSERT INTO room_movie_record (id, movie_id, room_record_id) VALUES
(1, 1, 1),
(2, 2, 2),
(3, 3, 3),
(4, 4, 4),
(5, 5, 5)
""")

############################################################################################################
 
conn.commit() # Commit the changes
conn.close() # Close the connection
