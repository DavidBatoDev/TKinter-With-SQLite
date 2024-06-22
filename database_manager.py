import sqlite3
from classes import Room, Movie, Record

class MovieHouseDatabaseManager:
    def __init__(self, database_file):
        self.database_file = database_file

    # This method is used to get a connection to the database
    def get_connection(self):
        return sqlite3.connect(self.database_file)
    
    # This method is used to register a movie
    def register_movie(self, title, genre, cost) -> bool:
        try:
            conn = self.get_connection() # Get a connection to the database
            c = conn.cursor()
            c.execute("""
                      INSERT INTO 
                      movie 
                      (title, genre, cost) 
                      VALUES (?,?,?)
                      """, (title, genre, cost)
                      ) # Insert the movie into the database
            conn.commit() # Commit the transaction
            return True # Return True if the movie was successfully registered
        except sqlite3.Error as e:
            return False # Return False if the movie was not successfully registered
        finally:
            conn.close() # Close the connection to the database

    def remove_movie(self, id) -> None:
        try:
            conn = self.get_connection() # Get a connection to the database
            c = conn.cursor() # Create a cursor object
            c.execute("UPDATE movie SET is_deleted = True WHERE id = ?", (id)) # Update the movie to be deleted
            conn.commit() # Commit the transaction
        finally:
            conn.close() # Close the connection to the database


    def retrieve_movies(self, genres) -> list [Movie]:
        conn = self.get_connection() # Get a connection to the database
        c = conn.cursor() # Create a cursor object
        if len(genres) == 0: # If there are no genres specified
            moviesFetched = c.execute("""SELECT 
                                        id, 
                                        title, 
                                        genre, 
                                        cost 
                                    FROM movie
                                    WHERE is_deleted = False
                                    """).fetchall() # Fetch all movies from the database
        else: # If there are genres specified
            moviesFetched = c.execute(f"""
                                      SELECT 
                                        id, 
                                        title, 
                                        genre, 
                                        cost 
                                      FROM movie 
                                      WHERE genre in ({",".join("?" * len(genres))}) AND is_deleted = False
                                      """, (genres)
                                      ).fetchall() # Fetch all movies from the genres specified
        movies = list(map(lambda x: Movie(*x), moviesFetched)) # Create a list of Movie objects from the fetched movies
        conn.close() # Close the connection to the database
        return movies # Return the list of Movie objects
    
    
    def retrieve_rooms(self) -> list [Room]: # Retrieve all rooms from the database
        conn = self.get_connection() # Get a connection to the database
        c = conn.cursor() # Create a cursor object
        rooomsFetched = c.execute('SELECT * FROM room').fetchall() # Fetch all rooms from the database
        rooms = [Room(*x) for x in rooomsFetched] # Create a list of Room objects from the fetched rooms
        conn.close() # Close the connection to the database
        return rooms # Return the list of Room objects
    
    
    def retrieve_record(self, room_id) -> Record:
        conn = self.get_connection() # Get a connection to the database
        c = conn.cursor() # Create a cursor object 
        room_record = c.execute(f"""
                                SELECT * 
                                FROM room_record 
                                WHERE room_id = {room_id} 
                                ORDER BY id DESC 
                                LIMIT 1
                                """).fetchall() # Fetch the room record from the database
        if len(room_record) == 0: # If there is no room record
            return Record(0, room_id, 0, [], True) # Return a Record object with is_finished set to True
        else:
            id, dummy_room_id, total_cost, is_finished = room_record[0] # Unpack the room record
            moviesFetched = c.execute(f"""
                                    SELECT 
                                        m.id,
                                        m.title,
                                        m.genre,
                                        m.cost
                                    FROM room_record rr
                                    JOIN room_movie_record rmr
                                        ON rr.id = rmr.room_record_id
                                    JOIN movie m
                                        ON rmr.movie_id = m.id
                                    WHERE rr.is_finished = False AND rr.id = {id}
                      """).fetchall() # Fetch the movies from the room record
            if len(moviesFetched) == 0: # If there are no movies 
                return Record(id, room_id, total_cost, [], True) # Return a Record object with is_finished set to True
            movies = [Movie(*x) for x in moviesFetched] # Create a list of Movie objects from the fetched movies
            return Record(id, room_id, total_cost, movies, is_finished) # Return a Record object with the fetched movies
        
        
    def check_in(self, room_id, movies: list[Movie]) -> bool: # Check in a room
        conn = self.get_connection() # Get a connection to the database
        c = conn.cursor() # Create a cursor object
        try:
            room_cost = c.execute("SELECT cost FROM room WHERE id = ?", (room_id,)).fetchone()[0] # Fetch the cost of the room
            movies_cost = sum([movie.cost for movie in movies])     # Calculate the cost of the movies
            total_cost = room_cost + movies_cost # Calculate the total cost
            c.execute("""
                      INSERT INTO 
                      room_record (room_id, total_cost, is_finished) 
                      VALUES (?, ?, ?)""", 
                      (room_id, total_cost, False)
                      ) # Insert the room record into the database
            room_record_id = c.lastrowid # Get the id of the room record
            for m in movies:
                c.execute("INSERT INTO room_movie_record (movie_id, room_record_id) VALUES (?, ?)", (m.id, room_record_id)) # Insert the movies into the room record
            conn.commit() # Commit the transaction
            return True # Return True if the room was successfully checked in
        except Exception as e:
            print(e.args[0]) # Print the error message
            return False # Return False if the room was not successfully checked in
        finally:
            conn.close() # Close the connection to the database
        
    def check_out(self, id):
        conn = self.get_connection() # Get a connection to the database
        c = conn.cursor() # Create a cursor object
        try:
            c.execute('UPDATE room_record SET is_finished = True WHERE id = ?', (id,)) # Update the room record to be finished
            conn.commit() # Commit the transaction
            return True # Return True if the room was successfully checked out
        except Exception as e:
            print(e.args[0]) # Print the error message
            return False # Return False if the room was not successfully checked out
        finally:
            conn.close()    # Close the connection to the database
    

# Eto mga pang testing

# For testing register_movie
# movieTest = MovieHouseDatabaseManager("movie_house.db")
# print(movieTest.register_movie("The Godfather", "Crime", 100))

# For testing retrieve_record
# movieTest = MovieHouseDatabaseManager("movie_house.db")
# record = movieTest.retrieve_record(3)
# movies = record.movies
# for movie in movies:
#     print(movie.title)

# For testing retrieve_movies
# movieTest = MovieHouseDatabaseManager("movie_house.db")
# movies = movieTest.retrieve_movies(["Crime", "Action"])
# for movie in movies:
#     print(movie.title)

# For testing retrieve_rooms
# movieTest = MovieHouseDatabaseManager("movie_house.db")
# rooms = movieTest.retrieve_rooms()
# for room in rooms:
#     print(room.id)

# For testing check_in
# movieTest = MovieHouseDatabaseManager("movie_house.db")
# movies = movieTest.retrieve_movies(["Crime", "Action"])
# for m in movies:
#     print(m.title)
# print(movieTest.check_in(1, movies))

# For testing check_out
# movieTest = MovieHouseDatabaseManager("movie_house.db")
# print(movieTest.check_out(1))



    