class Movie:
    def __init__(self, id, title, genre, cost):
        self.id = id
        self.title = title
        self.genre = genre
        self.cost = cost
    
    def __str__(self):
        return f"{self.id} - {self.title}"
    
class Room:
    def __init__(self, id, cost):
        self.id = id
        self.cost = cost


class Record:
    def __init__(self, id, room_id, total_cost, movies: list[Movie], is_finished=True):
        self.id = id
        self.room_id = room_id
        self.total_cost = total_cost
        self.movies = movies
        self.is_finished = is_finished