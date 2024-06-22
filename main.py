from tkinter import *
from database_manager import MovieHouseDatabaseManager
from classes import Room, Movie, Record
from tkinter import messagebox

class MovieHouseWindow(Tk):
    def __init__(self, database_file_name: str):
        super().__init__()
        self._database_manager = MovieHouseDatabaseManager(database_file_name)
        self.title("Movie House")
        self.geometry("500x500")
        self.configure(padx=15, pady=15)

        # Frames
        self.left_frame = Frame(self)
        self.left_frame.pack(side="left", fill="both", expand=True)

        self.register_lf = LabelFrame(self.left_frame, text="Register")
        self.register_lf.pack(side="top", fill="both", expand=True)

        self.register_input_frame = Frame(self.register_lf)
        self.register_input_frame.pack(expand=True)

        # register entries
        self.title_label = Label(self.register_input_frame, text="Movie Title")
        self.movie_title_entry = Entry(self.register_input_frame)
        self.title_label.grid(row=0, column=0, sticky='w')
        self.movie_title_entry.grid(row=0, column=1, sticky='ew')

        self.genre_label = Label(self.register_input_frame, text="Genre")
        self.genre_entry = Entry(self.register_input_frame)
        self.genre_label.grid(row=1, column=0, sticky='w')
        self.genre_entry.grid(row=1, column=1, sticky='ew')

        self.cost_label = Label(self.register_input_frame, text="Cost")
        self.cost_entry = Entry(self.register_input_frame)
        self.cost_label.grid(row=2, column=0, sticky='w')
        self.cost_entry.grid(row=2, column=1, sticky='ew')

        # add movie button
        self.add_movie_button = Button(self.register_input_frame, text="Add Movie", command=self.register_movie)
        self.add_movie_button.grid(row=3, column=0, columnspan=2, sticky='ew')

        # Movie Section
        self.movies_lf = LabelFrame(self.left_frame, text="Movies", padx=15, pady=15)
        self.movies_lf.pack(side="bottom", fill="both", expand=True)
        self.movies_lf.columnconfigure(0, weight=1)
        self.movies_lf.columnconfigure(1, weight=1)
        self.movies_lf.rowconfigure(0, weight=1)
        self.movies_lf.rowconfigure(1, weight=1)

        # listboxes
        self.movies_list = Listbox(self.movies_lf, selectmode=SINGLE)
        self.movies_list.grid(row=0, column=0, sticky='nsew')

        # bind the remove_movie_buttom
        self.movies_list.bind("<<ListboxSelect>>", self.update_remove_button_state)

        # remove movie button
        self.remove_movie_button = Button(self.movies_lf, text="Remove Movie", command=self.remove_movie, state=DISABLED)
        self.remove_movie_button.grid(row=1, column=0, sticky='ew')

        # filter container
        self.filter_container = Frame(self.movies_lf, padx=10, pady=10)
        self.filter_container.grid(row=0, column=1, sticky='nsew', rowspan=2)
        self.genre_filter_label = Label(self.filter_container, text="Genres")
        self.genre_filter_label.pack(side="top", fill="both")
        
        # variables for checkbuttons
        self.adventure_checked = BooleanVar()
        self.comedy_checked = BooleanVar()
        self.fantasy_checked = BooleanVar()
        self.romance_checked = BooleanVar()
        self.tragedy_checked = BooleanVar()

        # genres to be used in checkbuttons
        genres = [{
                "variable_name": "adventure_checkbutton",
                "name": "Adventure",
                "selected": False,
                "variable": self.adventure_checked
            }, {
                "variable_name": "comedy_checkbutton",
                "name": "Comedy",
                "selected": False,
                "variable": self.comedy_checked
            }, {
                "variable_name": "fantasy_checkbutton",
                "name": "Fantasy",
                "selected": False,
                "variable": self.fantasy_checked
            }, {
                "variable_name": "romance_checkbutton",
                "name": "Romance",
                "selected": False,
                "variable": self.romance_checked,
            }, {
                "variable_name": "tragedy_checkbutton",
                "name": "Tragedy",
                "selected": False,
                "variable": self.tragedy_checked
            }]
        
        # create checkbox container
        self.checkbox_container = Frame(self.filter_container)
        self.checkbox_container.pack(side='top', fill='both', expand=True)

        # create checkbuttons
        genre_vars = {}

        # loop through genres and create checkbuttons
        i = 0
        for genre in genres:
            genre_vars[genre["name"]] = Checkbutton(self.checkbox_container, text=genre["name"], variable=genre["variable"], command=self.update_list)
            genre_vars[genre["name"]].grid(row=i, column=0, sticky='w')
            i += 1

        # Rooms Section
        self.rooms_lf = LabelFrame(self, text="Rooms", padx=15, pady=15)
        self.rooms_lf.pack(side="right", fill="both", expand=True)
        # rooms button
        for i in range(1, 5):
            room_button = Button(self.rooms_lf, text=f"Room {i}", command=lambda i=i: self.open_room(i))
            room_button.pack(side="top", fill="both", expand=True, padx=10, pady=10)

        self.update_list()

    # For registering a movie
    def register_movie(self):
        movie_title = self.movie_title_entry.get()
        genre = self.genre_entry.get()
        cost = self.cost_entry.get()
        try:
            # Check if the fields are empty
            if movie_title == "" or genre == "" or cost == "":
                raise Exception("All fields are required")
            # register the movie to the database
            self._database_manager.register_movie(movie_title, genre, cost)
            # update the listbox
            self.update_list()
            # clear the entries
            movie_title = self.movie_title_entry.delete(0, END)
            genre = self.genre_entry.delete(0, END) 
            cost = self.cost_entry.delete(0, END) # Clear the cost entry
        except Exception as e:
            messagebox.showerror("Error", str(e))
        
    # For updating the list
    def update_list(self):
        # Clear the listbox
        self.movies_list.delete(0, END)
        # Get the genres
        genres = []
        #  Check if the checkbuttons are checked
        if self.adventure_checked.get():
            genres.append("Adventure")
        if self.comedy_checked.get():
            genres.append("Comedy")
        if self.fantasy_checked.get():
            genres.append("Fantasy")
        if self.romance_checked.get():
            genres.append("Romance")
        if self.tragedy_checked.get():
            genres.append("Tragedy")
        # Retrieve the movies
        movies = self._database_manager.retrieve_movies(genres)
        for movie in movies:
            self.movies_list.insert(END, movie)

    # For updating the remove button state
    def update_remove_button_state(self, event):
        if self.movies_list.curselection():
            self.remove_movie_button.config(state=NORMAL)
        else:
            self.remove_movie_button.config(state=DISABLED)

    # For removing a movie
    def remove_movie(self):
        # Get the movie id
        movie_id = self.movies_list.get(self.movies_list.curselection())[0]
        # Remove the movie
        self._database_manager.remove_movie(movie_id)
        # Update the list
        self.update_list()

    def open_room(self, room_id):
        # Get the record
        record = self._database_manager.retrieve_record(room_id)
        # Get the room
        room = self._database_manager.retrieve_rooms()[room_id - 1]
        # Open the record window
        record_window = RecordWindow(room, self._database_manager, record)
        record_window.mainloop()


class RecordWindow(Toplevel):
    # Initialize the RecordWindow
    def __init__(self, room: Room, database_manager: MovieHouseDatabaseManager, record: Record):
        self.room: Room = room
        self.database_manager = database_manager
        self.record = record

        super().__init__()
        self.title(f"Room {self.room.id}") # Set the title of the window
        self.geometry("640x400") # Set the geometry of the window
        self.configure(padx=15, pady=15) # Set the padding of the window

        # Configure the window
        for i in range(2): # Configure 2 rows and 2 columns to expand equally
            self.rowconfigure(i, weight=1)
            self.columnconfigure(i, weight=1)

        ################################################ MOVIES SECTION ################################################
        # Create a frame for the movies
        self.movies_frame = Frame(self)
        self.movies_frame.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)  # Add padx and pady for padding

        # Create a label for the movies
        self.movies_label = Label(self.movies_frame, text="Movies")
        self.movies_label.pack(side="top", fill="x", expand=True)

        # Create a listbox for the movies
        self.movies_list = Listbox(self.movies_frame)
        self.movies_list.pack(side="top", fill="both", expand=True)

        # Create an add movie button
        self.add_movie_button = Button(self.movies_frame, text="Add Movie", command=self.add_movie, width = 25, state=DISABLED)
        self.add_movie_button.pack(side="top")

        # Bind the listbox to the add movie button
        self.movies_list.bind("<<ListboxSelect>>", self.add_movie_button_state)

        ################################################ MOVIES TO WATCH SECTION ################################################
        # Create a frame for the movies to watch
        self.movies_to_view_frame = Frame(self)
        self.movies_to_view_frame.grid(row=0, column=1, sticky='nsew', padx=10, pady=10)  # Add padx and pady for padding

        # Create a label for the movies to watch
        self.movies_to_watch_label = Label(self.movies_to_view_frame, text="Movies to Watch")
        self.movies_to_watch_label.pack(side="top", fill="x", expand=True)

        # Create a listbox for the movies to watch
        self.movies_to_view_list = Listbox(self.movies_to_view_frame)
        self.movies_to_view_list.pack(side="top", fill="both", expand=True)

        # Create a remove movie button
        self.remove_movie_button = Button(self.movies_to_view_frame, text="Remove Movie", command=self.remove_movie, width = 25, state=DISABLED)
        self.remove_movie_button.pack(side="top")

        # Bind the listbox to the remove movie button
        self.movies_to_view_list.bind("<<ListboxSelect>>", self.remove_movie_button_state)

        ################################################ ROOM ACTION BUTTTONS ################################################
        # Create a frame for the room action buttons
        self.room_action_frame = Frame(self)
        self.room_action_frame.grid(row=1, column=0, columnspan=2, sticky='nsew', padx=10, pady=10)  # Add padx and pady for padding
        self.room_action_frame.columnconfigure(0, weight=1)
        self.room_action_frame.rowconfigure(0, weight=1)

        # Create a label for the total cost
        self.total_cost = StringVar()
        self.total_cost_label = Label(self.room_action_frame, textvariable=self.total_cost)
        self.total_cost_label.pack(side="top", fill="both")

        # Create a frame for the check buttons
        self.check_frame = Frame(self.room_action_frame)
        self.check_frame.pack(side="top", expand=True, pady=10)
        self.check_frame.columnconfigure(0, weight=1)
        self.check_frame.columnconfigure(1, weight=1)

        # Create a check in button
        self.check_in_button = Button(self.check_frame, text="Check In", command=self.check_in, width = 25)
        self.check_in_button.grid(row=0, column=0, padx=10)

        # Create a check out button
        self.check_out_button = Button(self.check_frame, text="Check Out", command=self.check_out, width = 25)
        self.check_out_button.grid(row=0, column=1, padx=10)

        ################################################################################################

        # Update Elements Upon Load
        self.load_listboxes()
        self.update_total_cost()
        self.check_button_is_available()

    # Add a movie
    def add_movie(self):
        movies = self.database_manager.retrieve_movies([])
        movie_id = self.movies_list.get(self.movies_list.curselection())[0]
        movie = None
        for m in movies:
            if str(m.id) == str(movie_id):
                movie = m
                break
        self.record.movies.append(Movie(movie.id, movie.title, movie.genre, movie.cost))
        self.load_listboxes()
        self.update_total_cost()
        self.check_button_is_available()
        self.add_movie_button_state(None)

    # Load the listboxes
    def load_listboxes(self):
        # Clear the listboxes
        self.movies_list.delete(0, END)
        self.movies_to_view_list.delete(0, END)

        # Retrieve the movies
        movies = self.database_manager.retrieve_movies([])

        # Get the movie titles in the record
        movie_titles_in_record_movies = [movie.title for movie in self.record.movies]

        # Get the unchecked movies
        unchecked_movies = map(str, [movie for movie in movies if movie.title not in movie_titles_in_record_movies])
        self.movies_list.insert(END, *unchecked_movies)
        
        # Get the checked movies
        if self.record.movies:
            self.movies_to_view_list.insert(END, *self.record.movies)

    # Update the total cost
    def update_total_cost(self):
        self.total_cost.set(f"Total Cost: {sum([movie.cost for movie in self.record.movies]) + self.room.cost}")

    # Add movie button state
    def add_movie_button_state(self, event):
        if self.movies_list.curselection():
            self.add_movie_button.config(state=NORMAL)
        else:
            self.add_movie_button.config(state=DISABLED)

    # Remove movie button state
    def remove_movie_button_state(self, event):
        if self.movies_to_view_list.curselection():
            self.remove_movie_button.config(state=NORMAL)
        else:
            self.remove_movie_button.config(state=DISABLED)

    # Check in
    def remove_movie(self):
        # Retrieve the movies
        movies = self.database_manager.retrieve_movies([])
        # Get the movie id
        movie_id = self.movies_to_view_list.get(self.movies_to_view_list.curselection())[0]
        movie = None
        # Get the movie
        for m in movies:
            if str(m.id) == str(movie_id):
                movie = m
                break
        # Remove the movie
        self.record.movies = [m for m in self.record.movies if m.id != movie.id]
        self.load_listboxes() # Load the listboxes
        self.update_total_cost() # Update the total cost
        self.check_button_is_available() # Check if the button is available
        self.remove_movie_button_state(None) # Remove the movie button state

    # Check in
    def check_button_is_available(self):
        # Check if the record is finished
        if self.record.is_finished == False:
            self.check_in_button.config(state=DISABLED)
            self.check_out_button.config(state=NORMAL)
        # Check if the record is not finished
        elif len(self.record.movies) > 0 and self.record.is_finished == True:
            self.check_in_button.config(state=NORMAL)
            self.check_out_button.config(state=DISABLED)
        # Check if the record is finished and there are no movies
        elif len(self.record.movies) == 0:
            self.check_in_button.config(state=DISABLED)
            self.check_out_button.config(state=DISABLED)
    
    # Check in
    def check_in(self):
        self.record.is_finished = False
        # Check in
        result = self.database_manager.check_in(room_id=self.room.id, movies=self.record.movies)
        # Check if the check in is successful
        if result:
            messagebox.showinfo("Success", "Checkin Successful, Enjoy your movie!")
        else:
            messagebox.showerror("Error", "Checkin Failed")
            self.load_listboxes()
        # Check if the button is available
        self.check_button_is_available()
        
    # Check out
    def check_out(self):
        # Check out
        self.record.is_finished = True
        # Retrieve the record id
        record_id = self.database_manager.retrieve_record(self.room.id).id
        # Check out
        result = self.database_manager.check_out(id=record_id)
        if result:
            self.record.movies = [] # Clear the movies
            self.load_listboxes() # Load the listboxes
            self.movies_list = self.database_manager.retrieve_movies([]) # Retrieve the movies
            messagebox.showinfo("Success", "Checkout Successful, Please come again!") # Show a success message
        else:
            messagebox.showerror("Error", "Checkout Failed") # Show an error message
            self.load_listboxes() # Load the listboxes
        self.check_button_is_available() # Check if the button is available

if __name__ == "__main__":
    window = MovieHouseWindow("movie_house.db") # Create a window
    window.mainloop() # Run the window

