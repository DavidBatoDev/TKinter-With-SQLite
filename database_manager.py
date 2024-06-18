import sqlite3
from classes import Room, Movie, Record

class MovieHouseDatabaseManager:
    def __init__(self, database_file):
        self.database_file = database_file

    def get_connection(self):
        return sqlite3.connect(self.database_file)
    
    def register_movie(self, title, genre, cost) -> bool:
        try:
            conn = self.get_connection()
            c = conn.cursor()
            c.execute("""
                      INSERT INTO 
                      movie 
                      (title, genre, cost) 
                      VALUES (?,?,?)
                      """, (title, genre, cost)
                      )
            conn.commit()
            return True
        except sqlite3.Error as e:
            return False
        finally:
            conn.close()

    def remove_movie(self, id) -> None:
        try:
            conn = self.get_connection()
            c = conn.cursor()
            c.execute("UPDATE movie SET is_deleted = True WHERE id = ?", (id))
            conn.commit()
        finally:
            conn.close()


    def retrieve_movies(self, genres) -> list [Movie]:
        conn = self.get_connection()
        c = conn.cursor()
        if len(genres) == 0:
            moviesFetched = c.execute("""SELECT 
                                        id, 
                                        title, 
                                        genre, 
                                        cost 
                                    FROM movie
                                    WHERE is_deleted = False
                                    """).fetchall()
        else:
            moviesFetched = c.execute(f"""
                                      SELECT 
                                        id, 
                                        title, 
                                        genre, 
                                        cost 
                                      FROM movie 
                                      WHERE genre in ({",".join("?" * len(genres))}) AND is_deleted = False
                                      """, (genres)
                                      ).fetchall()
        movies = list(map(lambda x: Movie(*x), moviesFetched))
        conn.close()
        return movies
    
    
    def retrieve_rooms(self) -> list [Room]:
        conn = self.get_connection()
        c = conn.cursor()
        rooomsFetched = c.execute('SELECT * FROM room').fetchall()
        rooms = [Room(*x) for x in rooomsFetched]
        conn.close()
        return rooms
    
    
    def retrieve_record(self, room_id) -> Record:
        conn = self.get_connection()
        c = conn.cursor()
        room_record = c.execute(f"""
                                SELECT * 
                                FROM room_record 
                                WHERE room_id = {room_id} 
                                ORDER BY id DESC 
                                LIMIT 1
                                """).fetchall()
        if len(room_record) == 0:
            return Record(0, room_id, 0, [], True)
        else:
            id, dummy_room_id, total_cost, is_finished = room_record[0]
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
                                        ON rmr.movie_id = m.id AND m.is_deleted = False
                                    WHERE rr.is_finished = False AND rr.id = {id}
                      """).fetchall()
            if len(moviesFetched) == 0:
                return Record(id, room_id, total_cost, [], True)
            movies = [Movie(*x) for x in moviesFetched]
            return Record(id, room_id, total_cost, movies, is_finished)
        
        
    def check_in(self, room_id, movies: list[Movie]) -> bool:
        conn = self.get_connection()
        c = conn.cursor()
        try:
            total_cost = sum([movie.cost for movie in movies])
            c.execute("""
                      INSERT INTO 
                      room_record (room_id, total_cost, is_finished) 
                      VALUES (?, ?, ?)""", 
                      (room_id, total_cost, False)
                      )
            room_record_id = c.lastrowid
            for m in movies:
                c.execute("INSERT INTO room_movie_record (movie_id, room_record_id) VALUES (?, ?)", (m.id, room_record_id))
            conn.commit()
            return True
        except Exception as e:
            print(e.args[0])
            return False
        finally:
            conn.close()
        
    def check_out(self, id):
        conn = self.get_connection()
        c = conn.cursor()
        try:
            c.execute('UPDATE room_record SET is_finished = True WHERE id = ?', (id,))
            conn.commit()
            return True
        except Exception as e:
            print(e.args[0])
            return False
        finally:
            conn.close()
    

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



    