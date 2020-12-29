*************************************
Useless but Fun: Command Line Hangman
*************************************

:date: 2020-12-29 00:00
:modified: 2020-12-29 00:00
:tags: Programming
:category: Programming
:authors: Adams Rosales
:summary: Building a Hangman game to play in the terminal
:header_cover: /static/post9/header.jpg

Interesting...Tell Me More
##########################
I'm building a Python package called `pygme <https://github.com/adaros92/pygme>`_ for playing simple games on your
terminal. It's purely because this is how I enjoy spending my time :).

Last time I wrote about implementing `Snake <https://decipheringbigdata.net/useless-but-fun-command-line-snake.html>`_.
That was okay but it was missing some of that edge. Some of that spice that makes a game *really* fun. Well, don't fret
because today I am implementing Hangman!

.. image:: https://media.giphy.com/media/LNE01Z89j9gis/giphy.gif
  :width: 50%
  :alt: Excited elf

Design
######
Just like with any other serious software project, one must always begin with a well thought-out design. Don't worry. I
got you. Behold, the components of the game!

- Game - contains the game loop and manages interactions between the objects involved in the game
- Board - handy dandy interface used for other board-like games used here as a container for the noose pieces
- Noose - implements and manages the various components of the Hangman noose (pole, rope, head, arms, legs, etc)
- Word - supplements the built-in string class with additional functionality specific to a game of Hangman
- Dictionary - a container class for all possible words that can be generated at random

The actual dictionary of words will be stored in a text file and distributed with the pygme Python package. The
Dictionary class will manage this file by reading in all of the words available and converting them into special
word objects. These word objects will alter the way the characters in each word are represented based on individual characters
that have already been guessed. For example, if the word is "sunny" but the player has only guessed the character "n", it
will display the word as __nn_ when either the Python str or repr functions are called on it.

The Noose class here is just a collection of smaller objects that define how to display each of the components of a
Hangman noose to the user. A noose object will consist of the noose holder thing (?) made up by the base, pole,
top piece, and rope in addition to the man that it will hold, which will be made up by the head, arms, body, and legs.

The Board class is just a handy 2D grid that can hold any data needed for a game. In this case I'm just using it to store
the different components of a noose and "draw" the additional pieces whenever the player's guess is wrong.

Finally, the Game class will just manage all the other components and dictate the flow of the game. At a high level, it
will do the following:

1. Instantiate the necessary board, noose, and dictionary objects
2. Get a random word to guess from the dictionary
3. Display the base noose and hidden word that needs to be guessed to the user
4. Ask for the player's guess and validate it
5. Check if the guess is right or wrong and update the noose object accordingly
6. Display the update to the player (either correct characters appear or a new body part is filled in)

It keeps doing 4-6 until a game over condition is reached (the noose is full or all letters have been guessed).

Noose Implementation
####################
Starting out with Noose class we have the following.

.. code-block:: python

    from pygme.game.board import GameBoard


    class Noose(object):
        """ Combines noose and body parts together to make up the Hangman noose that is displayed to the user
        Constructor parameters:
        @param game_board - the board to draw the noose on
        """
        def __init__(self, game_board: GameBoard) -> None:
            self.game_board = game_board
            self.noose_components = [
                # The base of the noose and rope
                {"x_index": 0, "y_index": 5, "part": NoosePart("base"), "displayed": True},
                {"x_index": 1, "y_index": 5, "part": NoosePart("pole"), "displayed": True},
                {"x_index": 2, "y_index": 5, "part": NoosePart("base"), "displayed": True},
                {"x_index": 1, "y_index": 4, "part": NoosePart("pole"), "displayed": True},
                {"x_index": 1, "y_index": 3, "part": NoosePart("pole"), "displayed": True},
                {"x_index": 1, "y_index": 2, "part": NoosePart("pole"), "displayed": True},
                {"x_index": 1, "y_index": 1, "part": NoosePart("pole"), "displayed": True},
                {"x_index": 2, "y_index": 0, "part": NoosePart("top"), "displayed": True},
                {"x_index": 3, "y_index": 0, "part": NoosePart("top"), "displayed": True},
                {"x_index": 4, "y_index": 1, "part": NoosePart("rope"), "displayed": True},
                # The body
                {"x_index": 4, "y_index": 2, "part": BodyPart("head"), "displayed": False},
                {"x_index": 4, "y_index": 3, "part": BodyPart("body"), "displayed": False},
                {"x_index": 3, "y_index": 3, "part": BodyPart("left_arm"), "displayed": False},
                {"x_index": 5, "y_index": 3, "part": BodyPart("right_arm"), "displayed": False},
                {"x_index": 3, "y_index": 4, "part": BodyPart("left_leg"), "displayed": False},
                {"x_index": 5, "y_index": 4, "part": BodyPart("right_leg"), "displayed": False},
            ]
            self.next_piece = self.get_last_displayed() + 1

        def draw(self) -> None:
            """ Refreshes the associated grid with the latest noose representation """
            self.game_board.clear()
            for component in self.noose_components:
                if not component["displayed"]:
                    continue
                part = component["part"]
                coordinate = (component["x_index"], component["y_index"])
                self.game_board.refresh([coordinate], repr(part), clear_board=False)

        def is_complete(self) -> bool:
            """ Checks whether all components have been displayed, meaning the noose is complete
            :returns True if the entire noose has been build during the course of the Hangman game; False otherwise
            """
            complete = True
            for component in self.noose_components:
                if not component["displayed"]:
                    complete = False
            return complete

        def get_last_displayed(self) -> int:
            """ Retrieves the last component of the Hangman noose that is currently displayed to the user
            :returns an index to the last displayed component in the noose_components class attribute
            """
            complete_idx = len(self.noose_components) - 1
            for idx, component in enumerate(self.noose_components):
                if not component["displayed"]:
                    complete_idx = idx - 1
                    break
            return complete_idx

        def update(self) -> None:
            """ Updates the noose by displaying a new component """
            if not self.is_complete():
                component_to_update = self.noose_components[self.next_piece]
                component_to_update["displayed"] = True
                self.next_piece += 1

This contains a collection of different parts in a list of dictionaries. These dictionaries store information about
where on a 2D grid each piece should be stored in to display the little noose + man figure via the UI. It's hard-coded
here because the shape itself remains constant. This would need to be made more dynamic to accommodate different sizes or
determine the number of parts passed on some parameter like the difficulty level.

When the noose is first instantiated, it holds a pointer to the last displayed item. The update method will just increment
this pointer and display the next item in line. This mechanism allows the game to display new parts of the man when
letters are guessed incorrectly.The get_last_displayed method here just helps with finding that last displayed item when
the noose is first instantiated.

The draw method just updates the given 2D grid/board with each of the components' coordinates and how to represent each
of the components. This will be called by the game loop before each turn to display the current status of the noose to the
player.

The is_complete method is used to check whether all of the components have been displayed or not. This will be used by the
game to determine if the man has been hung, which is a game over condition.

The NoosePart and BodyPart classes here are implemented below. All they do is define how to represent each part.

.. code-block:: python

    from abc import ABC


    class Part(ABC):
        """ A base Part interface to be inherited by different types of concrete parts
        Constructor parameters:
        @param part - the name of the part
        @param part_char_map - how the part will be represented to the user on a grid
        """
        def __init__(self, part: str, part_char_map: dict):
            self.part = part
            self.part_char_map = part_char_map

        def __repr__(self):
            return self.part_char_map[self.part]

        def __str__(self):
            return self.__repr__()


    class BodyPart(Part):
        """ Represents part of the man in Hangman
        Constructor parameters:
        @param part - the name of the part
        """

        PART_CHAR_MAP = {
            "head": "O",
            "left_arm": "-",
            "right_arm": "-",
            "left_leg": "/",
            "right_leg": "\\",
            "body": "|"
        }

        def __init__(self, part: str):
            super().__init__(part, self.PART_CHAR_MAP)


    class NoosePart(Part):
        """ Represents part of noose in Hangman
        Constructor parameters:
        @param part - the name of the part
        """

        PART_CHAR_MAP = {
            "base": "_",
            "top": "_",
            "pole": "|",
            "rope": "|"
        }

        def __init__(self, part: str):
            super().__init__(part, self.PART_CHAR_MAP)


Dictionary Implementation
#########################
Alright, alright, alright. The dictionary! So for this, I just found a list of words online and saved them as a text
file in the data directory of the application `here <https://github.com/adaros92/pygme/blob/main/pygme/data/dictionary.txt>`_.
To accompany this I have a Dictionary class that reads the list in, converts the words into special objects of the Word
class I mentioned before, and generates a random word from that list to be used in the game.

.. code-block:: python

    import os
    import pkg_resources
    import random
    import sys


    class Dictionary(object):
        """ Represents a dictionary to get words from for word games
        Constructor arguments:
        :param config - a configuration dictionary containing the file packaged up with pygme containing all words
        """
        def __init__(self, config: dict) -> None:
            self.dictionary_filename = config["dictionary_filename"]
            self.words = []
            self._load_dictionary()

        def _load_dictionary(self):
            """ Reads the dictionary file specified in the config assumed to be stored in data subdirectory """
            directory_path = pkg_resources.resource_filename('pygme', 'data/')
            full_path = os.path.join(directory_path, self.dictionary_filename)
            with open(full_path, "r") as f:
                words = f.readlines()
            self.words = [Word(word.strip("\n")) for word in words]

        def get_random_word(self, min_length: int = 1, max_length: int = sys.maxsize) -> str:
            """ Retrieves a random word with length between the given minimum and max length arguments
            :param min_length - the minimum length that the word should have
            :param max_length - the maximum length that the word should have
            :returns a random word from the dictionary matching the given length criteria
            """
            eligible_words = [word for word in self.words if min_length <= len(word) <= max_length]
            return random.choice(eligible_words)

This takes a config dictionary with the name of the dictionary file as it's stored in the data directory within the
application. It will then read this file with the _load_dictionary method and store each word in a words list. The
get_random_word method just returns a random word from the current list matching the required min and max length limits.

You'll notice that each word is stored as a Word object. This class is defined next.

.. code-block:: python

    class Word(object):
        """ Represents a word in a dictionary. Used to provide supplements to existing str class by not taking into
        account capitalization when comparing words and hiding certain characters when returning the word to a caller.
        Constructor parameters:
        @param word - a regular string word
        @param show_only - an optional set containing characters to exclude from the word when repr or str are called
        """

        def __init__(self, word: str, show_only: set = None):
            super().__init__()
            if " " in word:
                raise ValueError("The given word {0} contains whitespace".format(word))
            self.word = word.lower()
            self.show_only = show_only
            self.hide_all = False
            if not show_only:
                self.show_only = set()

        def __len__(self):
            return len(self.word)

        def __contains__(self, letter: str) -> bool:
            """ Checks whether the given letter is within the word without taking capitalization into account
            For example:
            "a" in action == True
            "A" in action == True
            "p" in action == False
            :param letter - the letter to check
            :returns True if the letter is in the word, False otherwise
            """
            return letter.lower() in self.word

        def __repr__(self) -> str:
            """ When repr() is called on the string, exclude characters not in the self.show_only set if it's nonempty
            :returns either the string as is or the string with excluded
            """
            return_str = self.word
            if self.show_only or self.hide_all:
                return_str = ""
                # Only show characters that are in the given show_only set
                for char in self.word:
                    if char.lower() in self.show_only or char.upper() in self.show_only:
                        return_str += char
                    else:
                        return_str += "_"
            return return_str

        def __str__(self) -> str:
            return self.__repr__()

        def __setattr__(self, key: str, value: any) -> None:
            """ Overrides the set attribute functionality to always take the lowercase of a word
            For example:
            my_word = Word("hello")
            my_word.word = "Hi"
            my_word.word == "hi" # True
            :param key - the object attribute to set
            :param value - the value to assign to the attribute
            """
            # Any attribute other than word will be set normally and word will always be taken as lowercase
            self.__dict__[key] = value
            if key == "word":
                self.__dict__[key] = value.lower()

        def __iter__(self):
            yield from self.word

This pretty much acts like a string but implements some specific functionality we need for Hangman. First when a word is
stored, it's immediately converted to lowercase to ensure consistency. Second, the __contains__ magic method ensures that
when we check for presence of a character in the word string (like 'a' in abacus), it will convert the letter being checked
to lowercase. Third, when we call either str() or repr() on the string, only the characters present in the provided show_only
set will be displayed.

The __iter__ method here defines what behavior each word string should exhibit when the program iterates over it. For example,
if we define word my_word = Word("someword"), this will define what happens when we do for char in my_word. The yield from
self.word will just provide each character in the word stored with the object so : s, o, m, e, w, ... ,d.

Board Implementation
####################
Now for the class to record each of the noose's components and print it out to the screen.

.. code-block:: python

    from pygme.utils.display import clear_console
    from pygme.utils.validation import validate_grid_index
    from pygme.utils.space import


    class GameBoard(object):
        """ Represents a base board to play a game on which may be extended by more specific types of boards
        Constructor arguments:
        :param length - the length of the board to create
        :param width - the width of the board to create
        :param empty_square - how to represent empty squares on the board
        """
        def __init__(self, length: int, width: int, empty_square: str = "_") -> None:
            assert length > 0 and width > 0
            self.length = length
            self.width = width
            self.empty_square = empty_square
            self.board = []
            self._create_board()

        def is_square_clear(self, coordinate: tuple) -> bool:
            """ Returns True if the square at a given coordinate is empty; False if it's not empty
            :param coordinate - an x,y coordinate to check
            :returns whether the given coordinate is empty in the board
            """
            assert are_coordinates_between_limits(coordinate, self.width, self.length)
            if self.board[coordinate[0]][coordinate[1]] == self.empty_square:
                return True
            return False

        def _create_board(self) -> None:
            """ Creates an empty 2D list with the given board dimensions"""
            for i in range(self.length):
                self.board.append([self.empty_square for _ in range(self.width)])

        def print(self, include_reference: bool = False, ignore_characters: set = None, join_char: str = " ") -> None:
            """ Prints out the board to stdout
            :param include_reference - whether to include grid references when printing the board out in the console
            :param ignore_characters - a collection of characters to replace with empty characters
            :param join_char - how to join a row list together to produce a row on the terminl screen
            """
            # Clear the terminal
            clear_console()
            if not ignore_characters:
                ignore_characters = set()
            # Add an index before each column if applicable
            if include_reference:
                header_items = [str(x) for x in range(self.length)]
                header = "    "
                for item in header_items:
                    if len(item) == 1:
                        header += item + "   "
                    else:
                        header += item + "  "
                print(header)
            # Print the board
            for i in range(self.width):
                # Print an index before each row if applicable
                header = ""
                space = ""
                if include_reference:
                    header = "{0}".format(i)
                    if len(header) == 1:
                        space = " " * 3
                    else:
                        space = " " * 2
                    row_string = ""
                    for square in range(self.length):
                        column_spacing = "   "
                        if self.board[square][i] and self.board[square][i] not in ignore_characters:
                            row_string += self.board[square][i]
                        else:
                            row_string += self.empty_square
                        row_string += column_spacing
                    print(header + space + row_string + "\n")
                else:
                    row_string = join_char.join([self.empty_square if (not self.board[square][i]
                                                                       or self.board[square][i] in ignore_characters)
                                                 else self.board[square][i] for square in range(self.length)])
                    print(row_string)

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

This is fairly self-explanatory so moving on. Also, if someone wants to work on that horrendous print method the code
is `on GitHub <https://github.com/adaros92/pygme/blob/main/pygme/game/board.py>`_.

Game Implementation
###################
Finally we have the class to glue all of the different components together and run the main game loop.

.. code-block:: python

    import string

    from pygme.game.board import GameBoard
    from pygme.game.game import Game
    from pygme.hangman import noose
    from pygme.utils import dictionary


    class HangmanGame(Game):
        """ Contains the necessary logic to run a game of Hangman
        Constructor parameters:
        @param config - the configuration dictionary to use for the game (should be defined in data packaged with pygme)
        @param name - the name of the game to feed to parent class
        @param difficulty - a difficulty to assume (provided by user during initialization)
        """

        def __init__(self, config: dict, name: str = "hangman", difficulty: str = "normal") -> None:
            super().__init__(name, config, difficulty)
            self.dictionary = None
            self.noose = None
            self.min_word_length = None
            self.max_word_length = None
            self.guessed_characters = set()
            self.board = None
            self.noose = None
            self.word = None

        def _validate_initialization(self, initialization_object: dict) -> None:
            """ Validates the initialization object to ensure a Hangman game can occur
            :param initialization_object - required game parameters to follow
            """
            self._validate_base(initialization_object)

        def _initialize(self, initialization_object: dict = None) -> None:
            """ Initializes the game of Hangman
            :param initialization_object - an optional dictionary containing the required game parameters to use
            """
            initialization_object = self._get_user_input(initialization_object)
            self.difficulty = initialization_object["difficulty"]
            self.dictionary = dictionary.Dictionary(self.config)
            word_sizes_by_difficulty = self.config["word_sizes_by_difficulty"][self.difficulty]
            self.min_word_length = word_sizes_by_difficulty["min_word_length"]
            self.max_word_length = word_sizes_by_difficulty["max_word_length"]
            self.board = GameBoard(self.config["board_length"], self.config["board_width"], " ")
            self.noose = noose.Noose(self.board)
            self.noose.draw()

        def _has_won(self) -> bool:
            """ Checks whether the player has won the game by checking if all the letters in the word have been guessed
            :returns True if the game has been won; False otherwise
            """
            for letter in self.word:
                if letter not in self.guessed_characters:
                    return False
            return True

        def _man_died(self) -> bool:
            """ Checks whether the man has died by checking if the noose is complete
            :returns True if the man is dead; False otherwise
            """
            return self.noose.is_complete()

        def _is_game_over(self) -> bool:
            """ Checks whether the game has finished from two possible options - the player has won (guessed all letters) or
            the man has died
            :returns True if the game is over; False otherwise
            """
            if self._has_won() or self._man_died():
                return True
            return False

        def _display_word(self) -> None:
            """ Prints the current word to be guessed by hiding characters that have not been guessed yet when displaying
            the word to the user """
            if not self.guessed_characters:
                self.word.hide_all = True
            else:
                self.word.hide_all = False
                self.word.show_only = self.guessed_characters
            print("Word to guess:\n{0}\n".format(repr(self.word)))
            print("Guessed character: {0}\n".format(self.guessed_characters))

        def _display_final_status(self) -> None:
            """ Displays a message to let the user know how they did after the game finishes """
            self.word.show_only = set()
            self.word.hide_all = False
            print("\nThe word was: {0}\n".format(repr(self.word)))
            if self._has_won():
                print("Congratulations, you won!")
            else:
                print("Better luck next time!")

        def _get_guess_input(self) -> str:
            """ Accepts string input from the user to be the next guess (for monkeypatching instead of built-in input func)
            :returns the string input received from the user
            """
            return input("Enter a character to guess next:")

        def _get_guess(self) -> str:
            """ Retrieves a letter guess from the user and validates it before returning it to be used in the game
            :returns a single ASCII character to be the next letter guess in the game
            """
            guess_valid = False
            guess = None
            while not guess_valid:
                guess = self._get_guess_input()
                # Ensure the guess has not been already provided
                if guess in self.guessed_characters:
                    print("You already guessed that character. Try again.")
                # There must be a guess
                elif len(guess) > 1:
                    print("You can only enter one character at a time")
                # The guess must be either a lowercase or upper case letter
                elif guess not in string.ascii_letters:
                    print("Guesses must be one of {0}".format(string.ascii_letters))
                else:
                    guess_valid = True
            self.guessed_characters.add(guess)
            return guess

        def run(self, initialization_object: dict = None) -> dict:
            """ Runs the game of Hangman
            :param initialization_object - an optional dictionary containing the required game parameters to use
            """
            self._initialize(initialization_object)
            self.word = self.dictionary.get_random_word(min_length=self.min_word_length, max_length=self.max_word_length)
            assert len(self.word) > 1
            while not self._is_game_over():
                # Display noose and word on board
                self.board.print(join_char="")
                self._display_word()
                guess = self._get_guess()
                # Get the noose to display a new piece if the guess is wrong
                if guess not in self.word:
                    self.noose.update()
                # Update the current noose on the board to be displayed to the user
                self.noose.draw()
            self.board.print(join_char="")
            self._display_final_status()
            return {}

The game logic is found within the run method. All others are utility methods used by this run method. This is also pretty
straightforward. We start out by initializing everything with the _initialize method. Then when generate a new random
word for the player to guess. Next we begin iterating for as long as the game has not finished  and do the following:

1. Print the board, which has been drawn on by the noose object, to the user
2. Display the word with all characters that have yet to be guessed displayed as underscores
3. Ask for the player's next guess
4. Check if the guessed letter is in the word and if not, update the noose with the next body part
5. Draw the latest noose on the board


Once the game finishes, the final board will be printed out along with a status message that tells the player whether
they won or not.

The Final Game
##############
Check out this sweet play!

.. image:: https://media.giphy.com/media/y4x68SYqJg2b9PdRF5/giphy.gif
  :width: 60%
  :alt: A game of Hangman in the terminal

I'm going to tell my grand kids this was God of War.
