***********************************
Useless but Fun: Command Line Snake
***********************************

:date: 2020-12-14 00:00
:modified: 2020-12-14 00:00
:tags: Programming
:category: Programming
:authors: Adams Rosales
:summary: Building a really bad CLI Snake game from start to finish for the lols
:header_cover: /static/post6/header.jpg

Design
######

Nobody: ...

Me on a Sunday night: I think I'll build a command line Snake game.

What does this have to do with big data? Probably nothing but the heart wants what it wants. Let's get started!

In usual object-oriented fashion, we'll have the following classes.

- Game - contains the game loop and manages interactions between the objects involved in the game
- Snake - represents the actual Snake by managing its movement and eating functionality
- Board - contains the state of the Snake grid (location of the snake and food items)
- Player - represents the single Snake player by handling key events
- Food - little yummy bits that the snake eats to grow

Snake Implementation
####################
I have chosen Python as the programming language because the python is a type of snake. There are many kinds of python -
ball python, Burmese python, Borneo python, Timor python...the list goes on.

Anyway let's start by implementing the ssssnake itself.

.. image:: https://media.giphy.com/media/sjr7k1uuO0B0c/giphy.gif
  :width: 50%
  :alt: I'm a ssssnake

When the snake moves, different segments of its body can be moving in different directions (left, up, right, or down)
on the grid. Representing the snake as a linked list will allow us to manage the snake as a collection of individual
nodes where each node encapsulates information about its coordinates on the grid and direction of movement.

.. code-block:: python

    class Node(object):
    """ Represents each node in the body of the snake """

    def __init__(self, x_coordinate: int, y_coordinate: int, direction: str,
                 representation: str = '*', next_node=None, prev_node=None) -> None:
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        self.direction = direction
        self.representation = representation
        self.next_node = next_node
        self.prev_node = prev_node

    def __repr__(self):
        return self.representation

    def __str__(self):
        return self.__repr__()

Cool, we have a way to keep some state about each individual component of the snake's body. Now let's implement the
body of the snake.

.. code-block:: python

    class Body(object):
    """ Represents the body of the snake; Defines common functionality for growing and moving """

    def __init__(self, x_coordinate: int, y_coordinate: int, length: int = 1, direction: str = "left") -> None:
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        self.head = Node(x_coordinate, y_coordinate, direction)
        self.tail = self.head
        self.length = 1
        self.direction = direction
        # Grow the body to the desired initial length
        if length > 1:
            self.grow(length - 1)

    @property
    def coordinates(self) -> list:
        coordinates_list = []
        tmp_node = self.head
        while tmp_node:
            coordinates_list.append((tmp_node.x_coordinate, tmp_node.y_coordinate))
            tmp_node = tmp_node.next_node
        return coordinates_list

    def change_direction(self, new_direction: str) -> None:
        """ Changes the current body's direction of movement
        :param new_direction - one of four possible directions to move the body in
        """
        opposite_direction = {"left": "right", "right": "left", "down": "up", "up": "down"}[self.direction]
        # Only change the current direction if it's not opposite of the current direction
        if new_direction != opposite_direction:
            self.direction = new_direction

    @staticmethod
    def _create_new_node(direction: str, prev_node: Node):
        x_coordinate = None
        y_coordinate = None
        if direction == "left":
            x_coordinate = prev_node.x_coordinate + 1
            y_coordinate = prev_node.y_coordinate
        elif direction == "right":
            x_coordinate = prev_node.x_coordinate - 1
            y_coordinate = prev_node.y_coordinate
        elif direction == "up":
            x_coordinate = prev_node.x_coordinate
            y_coordinate = prev_node.y_coordinate + 1
        elif direction == "down":
            x_coordinate = prev_node.x_coordinate
            y_coordinate = prev_node.y_coordinate - 1
        new_node = Node(x_coordinate, y_coordinate, direction, prev_node=prev_node)
        return new_node

    def grow(self, by: int = 1) -> None:
        """ Grows the current body by the specified amount of nodes
        :param by - the number of nodes to grow the body by
        """
        assert by > 0
        new_node_chain = None
        last_node = None
        # Create a new chain of nodes to append to the end of the body
        for new_node_num in range(by):
            # Create the first node in the chain
            if new_node_num == 0:
                new_node_chain = self._create_new_node(direction=self.tail.direction, prev_node=self.tail)
                last_node = new_node_chain
            # Create all the other nodes after the first one and add them to the chain
            else:
                tmp_node = self._create_new_node(direction=last_node.direction, prev_node=last_node)
                last_node.next_node = tmp_node
                last_node = tmp_node
        # Integrate the new chain as part of the current body
        self.tail.next_node = new_node_chain
        self.tail = last_node
        self.length += by

    def slither(self, speed: float = 1.0) -> None:
        """ Moves the body in its current direction of movement
        :param speed - the speed to move the body in
        """
        # Each node will assign its direction and coordinate to the next node
        tmp_node = self.head.next_node
        tmp_x_coordinate = self.head.x_coordinate
        tmp_y_coordinate = self.head.y_coordinate
        while tmp_node:
            new_x_coordinate = tmp_node.x_coordinate
            new_y_coordinate = tmp_node.y_coordinate
            tmp_node.x_coordinate = tmp_x_coordinate
            tmp_node.y_coordinate = tmp_y_coordinate
            tmp_node = tmp_node.next_node
            tmp_x_coordinate = new_x_coordinate
            tmp_y_coordinate = new_y_coordinate
        # Once all other nodes have moved, the head moves to new location
        self.head.x_coordinate, self.head.y_coordinate = movement.resolve_movement(
            self.head.x_coordinate, self.head.y_coordinate, self.direction)

    def __repr__(self):
        node_list = []
        tmp_node = self.head
        while tmp_node:
            node_list.append(str(tmp_node))
            tmp_node = tmp_node.next_node
        return "-".join(node_list)

    def __str__(self):
        return self.__repr__()

This just takes a starting location for the head of the snake and direction of movement. It implements the core methods
of eating/growing and moving.

We will emulate movement with the slither method as follows:

1. Iterate over each node in the snake
2. Get the previous node's coordinates and direction of movement and assign them to the current node
3. Move the head of the snake to a new coordinate based on the direction of movement

The last step of assigning a new coordinate to the head based on the direction of movement is implemented with the following
utility function.

.. code-block:: python

    def resolve_movement(x_coordinate: int, y_coordinate: int, direction: str) -> tuple:
    """ Given current coordinates and a movement around a 2D grid, this function will return new coordinates that
    reflect that movement in 2 dimensional space
    :param x_coordinate - x-coordinate identifying the starting point on a 2D grid
    :param y_coordinate - y-coordinate identifying the starting point on a 2D grid
    :param direction - one of four possible directions to move in
    :returns a tuple of integers representing a new point (x-coordinate, y-coordinate)
    """
    assert direction in {'up', 'right', 'down', 'left'}
    if direction == "up":
        return x_coordinate, y_coordinate - 1
    elif direction == "right":
        return x_coordinate + 1, y_coordinate
    elif direction == "down":
        return x_coordinate, y_coordinate + 1
    elif direction == "left":
        return x_coordinate - 1, y_coordinate

The body's grow method simply creates a given number of new node and appends it to the end of the linked list. This
method will be called whenever the snake eats a tasty boi on the grid.

Finally there is the Snake class itself which implements a higher level API that the game will communicate with. This
includes methods for eating and moving. The snake class will manage its body accordingly when these methods are called.

.. code-block:: python

    class Snake(object):
    """ Represents the snake itself
    Constructor arguments:
    :param x_coordinate - the starting x-coordinate of the snake's head
    :param y_coordinate - the starting y-coordinate of the snake's head
    :param starting_length - the snake's starting node length
    :param starting_direction - the starting direction of movement that the snake will immediately head in
    """
    def __init__(self,
                 x_coordinate: int, y_coordinate: int,
                 starting_length: int = 1, starting_direction: str = "left") -> None:
        self.body = Body(x_coordinate, y_coordinate, length=starting_length, direction=starting_direction)

    @property
    def current_location(self) -> list:
        """ Retrieves a list of coordinate tuples representing the snake's location on a snake grid
        Example: [(0,1), (1,1)] is a 2 node long snake and on a 3 x 3 grid will look like this:
        _ _ _
        * * _
        _ _ _
        :returns a list of coordinate tuples
        """
        return self.body.coordinates

    @property
    def current_direction(self) -> str:
        """ Retrieves the snake's current direction of movement
        :returns a direction string (left, up, right, down)
        """
        return self.body.direction

    def eat(self, food_to_eat: any) -> None:
        """ Eats a given food and makes the snake grow by the food's growth value
        :param food_to_eat - a food object as defined in food.py
        """
        self.body.grow(food_to_eat.growth_value)

    def move(self, new_direction: str) -> None:
        """ Moves the snake by changing the direction to the new direction and altering the corresponding
        coordinates based on that direction of movement
        :param new_direction - the direction of movement (left, up, right, down)
        """
        # Change direction
        self.body.change_direction(new_direction)
        # Move
        self.body.slither()

    def __repr__(self):
        return self.body.__repr__()

    def __str__(self):
        return self.body.__str__()

Player Implementation
#####################
The player in the game of Snake just presses up, down, left, and right arrow keys on their keyboard to move the snake.
We can implement that by adding a listener that runs in a separate thread which will populate a queue with key presses.
Back in the original game thread, we will keep the state of the last key that was pressed in a map of key name to a
pressed boolean. Whenever a new event comes through the status will be updated for the corresponding key in the map.

.. code-block:: python

    import uuid
    import threading

    from curtsies import Input


    class Player(object):

        def __init__(self, player_id: uuid.UUID = uuid.uuid1(), computer=True):
            self.player_id = str(player_id)
            self.finished_game = False
            self.computer = computer
            self.keys = {"up": "'<UP>'", "right": "'<RIGHT>'", "left": "'<LEFT>'", "down": "'<DOWN>'"}
            self.event_to_key_map = {val: key for key, val in self.keys.items()}
            self.key_pressed_map = {key: False for key in self.keys}
            self.monitoring_lock = threading.Lock()
            self.thread = None

        def _detect_key_pressed(self) -> None:
            """ Detects presses of individual keys and marks those keys as pressed in common object """
            while True:
                # Check to see if any keys have been pressed
                with Input(keynames='curtsies') as input_generator:
                    for e in input_generator:
                        # Iterate over the applicable keys the player can press
                        for key in self.event_to_key_map:
                            pretty_key = self.event_to_key_map[key]
                            # If the player has pressed a key that is being tracked
                            if repr(e) == key:
                                # Signal that the key has been pressed in common object
                                self.key_pressed_map = {key: False for key in self.key_pressed_map}
                                self.key_pressed_map[pretty_key] = True
                        break
                if self.finished_game:
                    break

        def monitor_key_presses(self, key: str = None, how: str = "thread") -> None:
            assert how in {"thread", "block"}
            if how == "block" and not key:
                raise ValueError("A keyboard key name must be provided to block until key is pressed")
            if how == "thread":
                self.thread = threading.Thread(target=self._detect_key_pressed, args=())
                self.thread.start()
            # TODO blocking key press

        def wait_for_player_to_finish(self):
            self.thread.join()

Here I'm using the Input class from the curtsies library which handles the event listening for me. The _detect_key_pressed
method will simply iterate over each generated key and update the map of pressed keys. It will always update the map with
the last key pressed only. There cannot be multiple keys pressed at one time since that doesn't make sense in the context
of snake.

The monitor_key_presses method just launches a new thread that runs the _detect_key_pressed method. The thread here is
not an actual thread because of the GIL (check out my `previous post <https://decipheringbigdata.com/python-parallelism.html>`_)
but it works well enough for our purposes.

Food Implementation
###################
This will consist of two types of classes - individual food objects and a collection of food objects to generate them
at random.

First up we have the abstract food class. This just defines an interface that all food classes should abide by. In each
one of these we'll collect the coordinates where they are on the grid, how to represent the food objects in the terminal,
and each food type's nutritional value.

.. code-block:: python

    import random
    import uuid

    from abc import ABC, abstractmethod

    from pygme.utils import space


    class Food(ABC):
        """ Represents snake food by keeping track of each food object's location on a Snake grid, its character
        representation in the game (how it's shown to the user on the grid), and whether the food object has been eaten
        or not.
        This class defines a common interface for different types of concrete food classes.
        Constructor arguments:
        :param food_type - the type of food
        :param representation - a string representation of the given type of food
        :param x_coordinate - the x-coordinate of the food's location on the grid
        :param y_coordinate - the y-coordinate of the food's location on the grid
        :param food_id - a unique ID that identifies the food object (generated by default)
        """

        def __init__(self,
                     food_type: str, representation: str, x_coordinate: int, y_coordinate: int,
                     food_id: uuid.UUID = uuid.uuid1()) -> None:
            self.food_type = food_type
            self.representation = representation
            self.food_id = str(food_id)
            self.x_coordinate = x_coordinate
            self.y_coordinate = y_coordinate
            self.eaten = False

        @property
        def coordinates(self) -> tuple:
            """ Retrieves the food's location on the grid
            :returns a tuple of point coordinates (x-coordinate, y-coordinate)
            """
            return self.x_coordinate, self.y_coordinate

        @abstractmethod
        def growth_value(self) -> int:
            """ Defines how much consumers of the food grow by after eating it which will depend on the subclass """
            pass

        def __repr__(self) -> str:
            """ repr() on food objects will resolve to the given string representation of each food """
            return self.representation

        def __str__(self) -> str:
            """ str() on food objects will resolve to the given string representation of each food  """
            return self.__repr__()

        def __eq__(self, other) -> bool:
            """ Two food objects are equal if their type, unique_id, and representation are the same
            :param other - a different Food object
            :returns true if the foods are the same, false otherwise
            """
            return (self.food_type == other.food_type and self.food_id == other.food_id
                    and self.representation == other.representation)

I got lazy here and just created two types of food - crickets and mice. Each generates a random value to grow the snake
by. The mouse is obviously the most nutritious for the snake (do snakes even eat crickets?).

.. code-block:: python

    class Cricket(Food):
        """ Represents the cricket type of snake food which is the most common of the types and provides the least
        amount of nutritional value for snakes
        Class attributes:
        SPAWN_WEIGHT - defines the relative frequency that crickets spawn with
        Constructor arguments:
        :param representation - a string representation for how to show crickets on the snake grid
        :param x_coordinate - the x-coordinate of the food's location on the grid
        :param y_coordinate - the y-coordinate of the food's location on the grid
        """
        SPAWN_WEIGHT = 3

        def __init__(self, representation: str = "#", x_coordinate: int = None, y_coordinate: int = None) -> None:
            super().__init__(
                food_type="crickets", x_coordinate=x_coordinate, y_coordinate=y_coordinate, representation=representation)

        @property
        def growth_value(self) -> int:
            """ Defines by how many nodes the snake grows when it consumes a cricket
            :returns a random number of nodes the snake will grow by if it eats a cricket
            """
            return random.randint(1, 2)


    class Mouse(Food):
        """ Represents the mouse type of snake food which is the least common of the foods and provides the most
        nutritional value
        Class attributes:
        SPAWN_WEIGHT - defines the relative frequency that mice spawn with
        Constructor arguments:
        :param representation - a string representation for how to show mice on the snake grid
        :param x_coordinate - the x-coordinate of the food's location on the grid
        :param y_coordinate - the y-coordinate of the food's location on the grid
        """
        SPAWN_WEIGHT = 1

        def __init__(self, representation: str = "&", x_coordinate: int = None, y_coordinate: int = None):
            super().__init__(
                food_type="mouse", x_coordinate=x_coordinate, y_coordinate=y_coordinate, representation=representation)

        @property
        def growth_value(self) -> int:
            """ Defines by how many nodes the snake grows when it consumes a mouse
            :returns a random number of nodes the snake will grow by if it eats a mouse
            """
            return random.randint(2, 3)

The food collection inherits from the native Python list and acts like a queue. the _refresh method updates the queue
with new food objects from the available types. These will be randomly spawned based on their SPAWN_WEIGHT class
attributes. The generate method will simply pop food objects from the front of the queue until it reaches the end. It
will then call _refresh to repopulate the queue with new food objects. It will act like an endless generator of random
food spawns for as long as the generate method of a FoodCollection instance keeps getting called.

.. code-block:: python

    class FoodCollection(list):
        """ Keeps a collection of different types of food objects to be used as a queue by a Snake game for randomly
        generating food objects on the grid
        Constructor arguments:
        :param grid_width - the width of the grid used by the snake game to generate food objects in
        :param grid_length - the length of the grid used by the snake game to generate food objects in
        """

        def __init__(self, grid_width: int, grid_length: int) -> None:
            super().__init__()
            self.grid_width = grid_width
            self.grid_length = grid_length
            self.length = 0
            self._refresh()

        @property
        def max_length(self) -> int:
            """ Retrieves the max length of the food collection based on the size of the grid the collection is used
            to support with random food spawns
            :returns an integer with the max number of food objects the collection can have at any time
            """
            return self.grid_width * self.grid_length

        def _reset(self) -> None:
            """ Resets the current collection by emptying it and making room for new food objects up to the max length
            allowed
            """
            # Empty the current food collection
            self[:] = []
            # Create space for populating it with new food items
            self.extend([None] * self.max_length)
            self.length = self.max_length

        def _refresh(self) -> None:
            """ Provides a new bash of food objects in the current food collection based on how often each food
            object should appear when chosen randomly
            """
            # Empty the collection and make room for new food objects
            self._reset()
            # Enumerate the types of food to choose from and their relative weights of appearance frequency
            eligible_types = [Mouse, Cricket]
            weights = [Mouse.SPAWN_WEIGHT, Cricket.SPAWN_WEIGHT]
            assert len(eligible_types) == len(weights)
            # Generate max_length number of food objects randomly in a stratified fashion based on their weights
            random_type_choices = random.choices(eligible_types, weights=weights, k=self.max_length)
            for idx, food_type in enumerate(random_type_choices):
                # Assign random coordinates to each food item for the game to use for grid placement
                random_coordinates = space.get_coordinates_between_limits(self.grid_width, self.grid_length)
                self[idx] = food_type(x_coordinate=random_coordinates[0], y_coordinate=random_coordinates[1])

        def generate(self, count: int = 1) -> list:
            """ Generates the given count of random food objects from the collection and refreshes the collection
            with new objects if the collection is empty
            :param count - the number of food objects to generate
            :returns a list of randomly chosen food objects
            """
            assert count > 0
            return_foods = []
            for _ in range(count):
                # Refresh the current collection with new food objects if the collection is empty
                if self.length == 0:
                    self._refresh()
                # Get last object from the food collection and remove it from the collection
                return_foods.append(self.pop())
                self.length -= 1
            return return_foods

The utility function, get_coordinates_between_limits, just returns random coordinates that lie within the limits of a
2D grid. This is called in the _refresh method when instantiating new food objects and assigning them random coordinates
on the grid.

.. code-block:: python

    def get_coordinates_between_limits(grid_width: int, grid_length: int) -> tuple:
        """ Provides random coordinates between the specified limits on a 2D grid
        :param grid_width - the width of the grid in number of squares
        :param grid_length - the length of the grid in number of squares
        :returns a tuple with (x-coordinate, y-coordinate)
        """
        random_x_coordinate = random.randint(0, grid_length - 1)
        random_y_coordinate = random.randint(0, grid_width - 1)
        return random_x_coordinate, random_y_coordinate


Board Implementation
####################
Now we implement the board where all the action will take place. The snake will move around the board eating snacks until
it bumps into one of the walls and new food objects will randomly spawn. The board's job is just to accept coordinates
and representations of objects at those coordinates and print itself for the user.

.. code-block:: python

    from pygme.utils.display import clear_console
    from pygme.utils.validation import validate_grid_index


    class GameBoard(object):
        """ Represents a base board to play a game on which may be extended by more specific types of boards
        Constructor arguments:
        :param length - the length of the board to create
        :param width - the width of the board to create
        :param empty_square - how to represent empty squares on the board
        """
        def __init__(self, length: int, width: int, empty_square="_") -> None:
            assert length > 0 and width > 0
            self.length = length
            self.width = width
            self.empty_square = empty_square
            self.board = []
            self._create_board()

        def is_square_clear(self, coordinate: tuple) -> bool:
            if self.board[coordinate[0]][coordinate[1]] == self.empty_square:
                return True
            return False

        def _create_board(self) -> None:
            """ Creates an empty 2D list with the given board dimensions"""
            for i in range(self.length):
                self.board.append([self.empty_square for _ in range(self.width)])

        def print(self) -> None:
            """ Prints out the board to stdout """
            # Clear the terminal
            clear_console()
            # Print the current board
            for i in range(self.width):
                print(' '.join([self.empty_square if not self.board[square][i]
                                else self.board[square][i] for square in range(self.length)]))

        def clear(self) -> None:
            """ Clears the current board by replacing every square with the given empty square character """
            for i in range(self.width):
                for j in range(self.length):
                    self.board[j][i] = self.empty_square

        def refresh(self,
                    coordinates: list, representation: str, clear_board: bool = True) -> None:
            """ Refreshes the board by adding the given representation character to the given coordinates
            Example: representation = '*' at coordinates [(0, 1), (2, 1)] on a 3x3 board will result in the following:
            _ _ _
            * _ *
            _ _ _
            :param coordinates - a list of coordinate tuples to update
            :param representation - the character to be placed in the given coordinates
            :param clear_board - whether to first clear the current board before placing the new characters or not
            """
            # Clear the current board first if the provided argument is true
            if clear_board:
                self.clear()
            for coordinate_tuple in coordinates:
                x_coordinate, y_coordinate = coordinate_tuple[0], coordinate_tuple[1]
                # Only refresh the board with the coordinate if the coordinate is valid
                if validate_grid_index(self.length, self.width, x_coordinate, y_coordinate):
                    # Refresh the board
                    self.board[x_coordinate][y_coordinate] = representation

        def __repr__(self):
            return "GameBoard ({0} by {1})".format(self.length, self.width)

        def __str__(self):
            return self.__repr__()

The core method here is refresh. This will take an input of coordinate tuples and add the given character representation
to each one of the squares defined by the coordinates on the board. It will clear itself each time the refresh method
is called unless told otherwise. Each time there is an update to the snake's location or a new food object spawns, the
refresh method will be called to print it in the terminal.

There are also a couple of utility functions being used here. The clear_console function will simply clear the contents
displayed on the user's terminal. This will be called each time the board is refreshed so that the game appears static
in the shell window.

.. code-block:: python

    def clear_console():
        import os
        os.system('cls' if os.name == 'nt' else 'clear')

The validate_grid_index function is just used to ensure that updates only happen to coordinates that are within the
board.

.. code-block:: python

   def validate_grid_index(grid_length: int, grid_width: int, x_coordinate: int, y_coordinate: int) -> bool:
        if x_coordinate < 0 or x_coordinate >= grid_length or y_coordinate < 0 or y_coordinate >= grid_width:
            return False
        return True

Game Implementation
###################
Finally, the main game loop to tie all of the components above together.

.. code-block:: python

    import random
    import time

    from pygme.game.game import Game
    from pygme.game.player import Player
    from pygme.snake import snake, food
    from pygme.utils.display import clear_console
    from pygme.utils.validation import validate_user_input


    class SnakeGame(Game):
        """ Defines the main Snake game loop and initialization functionality """

        def __init__(self,
                     config: dict, name: str = "Snake", number_of_players: int = 1, difficulty: str = "normal") -> None:
            super().__init__(name, config, number_of_players, difficulty)
            self.required_inputs = {"board_width": int, "board_length": int, "difficulty": str}
            self.board = None
            self.snake = None
            self.food_collection = None
            self.current_food = []
            self.player = Player(computer=False)

        def _validate_initialization(self, initialization_object: dict) -> None:
            """ Ensures that the given initialization_object containing parameters to run the Snake game has complete
            and valid parameters
            :param initialization_object - a dictionary containing game parameter names and their values for operation
            """
            # Validate completeness of inputs
            for required_input in self.required_inputs:
                if required_input not in initialization_object:
                    raise RuntimeError("{0} is a required input to begin a Snake game".format(required_input))
            # Validate correct board dimensions
            board_width = initialization_object["board_width"]
            board_length = initialization_object["board_length"]
            difficulty = initialization_object["difficulty"]
            # Required min coordinates for a game of snake
            # TODO should be in config
            required_width = 10
            required_length = 10
            if initialization_object["board_width"] < required_width \
                    or initialization_object["board_length"] < required_length:
                raise ValueError("The Snake board must be at least {0}x{1}".format(required_length, required_width))
            if board_width != board_length:
                raise ValueError("The Snake board must be a square where width == length")
            if difficulty not in self.DIFFICULTY_TYPES:
                raise ValueError("The game difficulty must be one of {0}".format(self.DIFFICULTY_TYPES))

        def _initialize(self, initialization_object: dict = None) -> None:
            """ Initializes a game of Snake from the given object of game parameters or user input if one is not provided
            :param initialization_object - a dictionary containing game parameter names and their values for operation
            """
            # Get input from the user if no initialization_object is provided
            if not initialization_object:
                initialization_object = {}
                pre_prompt = ""
                while True:
                    clear_console()
                    try:
                        print("{0}Provide your inputs to begin your game of Snake. Difficulty levels: easy, normal, hard\n"
                              .format(pre_prompt))
                        for required_input, input_type in self.required_inputs.items():
                            input_val = input("Enter a value for {0}: ".format(required_input))
                            initialization_object[required_input] = validate_user_input(
                                required_input, input_val, input_type)
                        self._validate_initialization(initialization_object)
                        break
                    except Exception as e:
                        pre_prompt = str(e) + "\n\n"
                        pass
            # Validate the input passed through the method arguments
            else:
                self._validate_initialization(initialization_object)
            # Create the board
            board_width = initialization_object["board_width"]
            board_length = initialization_object["board_length"]
            difficulty = initialization_object["difficulty"]
            self.board = self.construct_board(board_length, board_width)
            # Pick a random point to place the snake on and a starting snake length based on chosen difficulty
            starting_x_coordinate = random.randint(2, board_length-3)
            starting_y_coordinate = random.randint(2, board_width-3)
            starting_length = {"easy": 2, "normal": 4, "hard": 8}[difficulty]
            self.snake = snake.Snake(
                x_coordinate=starting_x_coordinate, y_coordinate=starting_y_coordinate, starting_length=starting_length)
            # Start monitoring player key presses
            self.player.monitor_key_presses()
            # Create a snake food collector and generator
            self.food_collection = food.FoodCollection(grid_width=board_width, grid_length=board_length)

        def _is_game_over(self) -> bool:
            """ Checks the board to see if the game is over
            :returns True if the game is over, False otherwise
            """
            game_over = False
            end_game_coordinates = set()
            current_snake_location = self.snake.current_location
            for coordinate in current_snake_location:
                # check if any coordinate is outside of the board
                # TODO: maybe only check if the head is outside for cases when snake grows into edge
                if coordinate[0] < 0 or coordinate[0] > self.board.length - 1:
                    game_over = True
                    break
                elif coordinate[1] < 0 or coordinate[1] > self.board.width - 1:
                    game_over = True
                    break
                '''
                elif coordinate in end_game_coordinates:
                    game_over = True
                    break
                end_game_coordinates.add(coordinate)
                '''
            return game_over

        def _get_food(self) -> None:
            """ Randomly generates food into the current grid """
            # TODO this should be in config
            difficulty_to_frequency_map = {
                "normal": 5, "easy": 10, "hard": 3}
            # If there is any current food on the grid that is not eaten then just return and don't generate new food
            for current_food_obj in self.current_food:
                if not current_food_obj.eaten:
                    return
            # Randomly generate food based on frequency of appearance by difficulty level
            if random.randint(1, difficulty_to_frequency_map[self.difficulty]) == 1:
                generated_food_ok = False
                generated_foods = []
                # Keep generating until the food falls in a spot where it's ok
                while not generated_food_ok:
                    generated_food_ok = True
                    generated_foods = self.food_collection.generate()
                    for generated_food in generated_foods:
                        # Don't place food in same place as Snake's head
                        if (generated_food.x_coordinate == self.snake.current_location[0][0]
                                or generated_food.y_coordinate == self.snake.current_location[0][1]):
                            # Regenerate if food is located at Snake's head
                            generated_food_ok = False
                self.current_food = generated_foods
                return
            self.current_food = []

        def _resolve_food(self, current_snake_location: list) -> None:
            """ Makes the snake eat the food and marks the food as eaten when that happens, which makes the object
            disappear from the grid; otherwise refresh the board with each uneaten piece of food
            :param current_snake_location - a list of current snake coordinates
            """
            # Check each of the current food items on the grid
            for food_obj in self.current_food:
                # If the snake's head is in the same square as the given food, then make the snake eat the food
                if (current_snake_location[0][0] == food_obj.x_coordinate
                        and current_snake_location[0][1] == food_obj.y_coordinate):
                    self.snake.eat(food_obj)
                    # Marking the food object as eaten will make it disappear from the grid
                    food_obj.eaten = True
                # If the food still exists, show it again on the grid
                if not food_obj.eaten:
                    self.board.refresh(
                        [(food_obj.x_coordinate, food_obj.y_coordinate)],
                        representation=food_obj.representation,
                        clear_board=False
                    )

        def _move_snake(self, current_direction: str) -> None:
            """ Moves the snake along the grid and checks for user input entered in separate thread
            :param current_direction - the direction the snake is current traveling in with respect to the grid
            """
            # Get directional input from the user about where to go
            snake_direction = current_direction
            for key in ["left", "right", "up", "down"]:
                # Change direction only if there is a valid directional key event in the key press map
                if self.player.key_pressed_map[key]:
                    snake_direction = key
                    break
            # Move the snake in either the current or new direction depending on whether player pressed a key
            self.snake.move(snake_direction)

        def _finish_game(self) -> None:
            print("Game over! Hit <Enter> to play again or <q> to exit.")
            self.player.finished_game = True
            self.player.wait_for_player_to_finish()

        def run(self, initialization_object: dict = None) -> dict:
            """ Game loop that accepts player events to move the snake around the board and keeps the state of the game
            until the game finishes
            :param initialization_object - a dictionary containing game parameter names and their values for operation
            :returns a dictionary containing various metrics and their values about the game that was played
            """
            self._initialize(initialization_object)
            representation = str(self.snake)[0]
            while True:
                current_snake_location = self.snake.current_location
                self._get_food()
                self.board.refresh(current_snake_location, representation=representation)
                self._resolve_food(current_snake_location)
                self.board.print()
                print("\nHit arrow keys on your keyboard to move the snake")
                # Get the current direction of the snake
                snake_direction = self.snake.current_direction
                self._move_snake(snake_direction)
                game_over = self._is_game_over()
                if game_over:
                    self._finish_game()
                    break
                else:
                    time.sleep(.25)
            return {}


The Final Game
##############
Yup, one step closer to deciphering the secrets of big data.

.. image:: https://media.giphy.com/media/QLR9DHzeoqJgihomeM/giphy.gif
  :width: 75%
  :alt: Final game implementation

This is part of a Python package I'm working on called pygme (Like pygame but I dropped the a). I'm implementing common
games to play on your terminal. Check it out `here <https://github.com/adaros92/pygme>`_ if you're like me and have
nothing better to do with your time!
