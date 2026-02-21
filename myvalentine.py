from typing import Self
import sys
import time
import os

class _State:
    def __init__(self):
        self.current_website = None
        self.remaining_tasks = []
        self.completed_tasks = []

    def set_current_task(self, task):
        self.current_website = task

state = _State()

def show_menu(options: list[str]) -> str:
    """
     Prints a list of options to the console and waits for the
    player to select one.

    Parameters:
        options (list[str]): A list of options to present to the player.

    Returns:
        str: The option selected by the player
    """

    while True:
        for i in range(0, len(options)):
            print(str(i+1) + ". " + options[i])
        command = input().lower()
        try:
            num = int(command)
            if num > 0 and num <= len(options):
                print ("")
                return options[num-1]
            else:
                print("" + str(num) + " is not a valid option. Please try again.")
                continue
        except:
            pass
        try:
            index = [x.lower() for x in options].index(command)
            print("")
            return options[index]
        except:
            print("Try again. '" + command + "' is not a valid choice.\n")

def show_options(*options: list[str]) -> str:
    """
    Prints a list of options to the console and waits for the
    user to select one.

    Returns:
        str: The option selected by the player
    """
    return show_menu(options)

class Website:
    """
    A class representing a website that the player need to complete its task.

    Setting one of the direction properties (north, south, east, or west) will
    also update the Website being set in the corresponding direction. For example,
    setting the north of a Website will also set the south of the target Website.

    Attributes:
        name (str): The name of the Website
        description (str): A description of the Website
        north (Website): The Website to the North of this Website or None if there is no Website
        east (Website): The Website to the East of this Website or None if there is no Website
        south (Website): The Website to the South of this Website or None if there is no Website
        west (Website): The Website to the West of this Website or None if there is no Website
        locked (bool): True if this Website cannot be entered or False otherwise
        keys (list[Website]): A list of Websites that this Website contains keys for
        friends (list[str]): A list of friends in this Website
    """
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self._north = None
        self._south = None
        self._east = None
        self._west = None
        self.locked = False
        self.keys = []
        self.tasks = []

    def set_locked(self, locked: bool) -> None:
        """
        Sets whether this Website is locked or not. If you wish to lock
        the Website with a key, use add_key_for instead.

        Parameters:
            locked (bool): True to lock the Website or False to unlock it
        """
        self.locked = locked
    
    def is_locked(self) -> bool:
        """
        Returns True if this Website is locked and requires
        a key to enter.

        Returns:
            bool: True if the Website is locked or False otherwise.
        """
        return self.locked == True
    
    def _get_north(self):
        return self._north
    def _set_north(self, Website: Self):
        if self._north != None:
            self._north._south = None

        if Website._south != None:
            Website._south._north = None
        
        self._north = Website
        Website._south = self
    def _del_north(self):
        if self._north != None:
            self._north._south = None
        del self._north

    def _get_south(self):
        return self._south
    def _set_south(self, Website: Self):
        if self._south != None:
            self._south._north = None

        if Website._north != None:
            Website._north._south = None
        
        self._south = Website
        Website._north = self
    def _del_south(self):
        if self._south != None:
            self._south._north = None
        del self._south

    def _get_east(self):
        return self._east
    def _set_east(self, Website: Self):
        if self._east != None:
            self._east._west = None

        if Website._west != None:
            Website._west._east = None
        
        self._east = Website
        Website._west = self
    def _del_east(self):
        if self._east != None:
            self._east._west = None
        del self._east

    def _get_west(self):
        return self._west
    def _set_west(self, Website: Self):
        if self._west != None:
            self._west._east = None

        if Website._east != None:
            Website._east._west = None
        
        self._west = Website
        Website._east = self
    def _del_west(self):
        if self._west != None:
            self._west._east = None
        del self._west

    north = property(_get_north, _set_north, _del_north)
    south = property(_get_south, _set_south, _del_south)
    east = property(_get_east, _set_east, _del_east)
    west = property(_get_west, _set_west, _del_west)
    
    def move(self, direction: str) -> None:
        """
        Moves the player character to the Website in the given direction.
        Direction must be one of "North", "East", "South", or "West".
        If there is no Website in the given direction or the Website in that
        direction is locked, this will print a message and do nothing.

        Parameters:
            direction (str): One of either "North", "East", "South", or "West"
        """
        Website = None
        match direction.lower():
            case "north":
                Website = self._north
            case "east":
                Website = self._east
            case "west":
                Website = self._west
            case "south":
                Website = self._south

        if Website == None:
            print("You can't move there")
            return

        if Website.is_locked():
            found_key = False
            for key in state.keys:
                if key == Website:
                    print("\U0001F5DD " +  green_text(" You unlocked the door with the " + key.name + " key."))
                    found_key = True
                    break
            if not found_key:
                print("\U0001F512 You turn the handle, but the door is " + red_text("locked") + "! You need a key to enter this Website.")
                return

        print("You walk into the " + Website.name + ". " + red_text("The door slams shut behind you.") + "\n" + Website.description)
        set_current_Website(Website)
        
    def show_move_options(self) -> None:
        """
        Prints a list of valid move directions to the console and
        waits for the player to make a choice. After choosing, the
        player will be moved to the Website in the given direction.
        """
        options = []
        if self._north != None:
            options.append("North")
        if self._south != None:
            options.append("South")
        if self._east != None:
            options.append("East")
        if self._west != None:
            options.append("West")
        
        print(underline_text("Where will you move next?"))
        choice = show_menu(options)
        print("")
        self.move(choice)
        print("")
    
    def where_am_i(self) -> None:
        print(self.description)

    def look_around(self) -> None:
        """
        Prints out the description of the website as well as any connected
        websites. If there is a key in this website, the player will also pick
        it up.
        """
        print(self.description)

        if self._north != None:
            print("The " + self._north.name + " is to the North.")
        if self._south != None:
            print("The " + self._south.name + " is to the South.")
        if self._east != None:
            print("The " + self._east.name + " is to the East.")
        if self._west != None:
            print("The " + self._west.name + " is to the West.")

        if len(self.keys) > 0:
            print("")
            for key in self.keys:
                print("\U0001F389 " + yellow_text("Congratulations! As you look around, you find the " + key.name + " key!"))
                state.keys.append(key)
            self.keys = []

        if len(self.tasks) > 0:
            print("")
            for friend in self.tasks:
                print("\U0001F388 " + yellow_text("You found your friend, " + friend + "!"))
                print(friend + " is now following you.")
                state.found_friends.append(friend)
                state.remaining_friends.remove(friend)
            self.tasks = []
        
        print("")
    
    def add_key_for(self, Website: Self) -> None:
        """
        Places a key for the given Website in this Website. That Website will be locked
        to the player unless they first use the look_around function in this Website
        to find the key.

        Parameters:
            Website (Website): The Website to lock and add a key for
        """
        self.keys.append(Website)
        Website.set_locked(True)
    
    def add_friend(self, name: str) -> None:
        """
        Places a friend in this Website. The player will find the friend
        if they use the look_around function in this Website.

        Parameters:
            name (str): The name of the friend
        """
        self.tasks.append(name)
        state.remaining_tasks.append(name)
    
def set_current_Website(Website: Self) -> None:
    """
    Sets the current Website the player is in to the given Website.

    Parameters:
        Website (Website): The Website to place the player in.
    """
    state.set_current_Website(Website)

def get_current_Website() -> Website:
    """
    Gets the Website the player is currently occupying.

    Returns:
        Website: The Website the player is currently occupying.
    """
    return state.current_Website

def remaining_tasks() -> int:
    """
    Gets the number of friends that have not yet been found

    Returns:
        int: The number of friends reamining to find.
    """
    return len(state.remaining_task)

def print_slow(str):
    """
    Slows down the return of text to appear like a typewriter.
    """
    for letter in str:
        sys.stdout.write(letter)
        sys.stdout.flush()
        time.sleep(0.005)

def enter_the_manor():
    # clear the screen
    print('\x1b[2J\x1b[3J\x1b[H')
    print_slow("While walking home from the movie theater with your three friends, you stop in front of an old house \nthat you don't remember seeing before. You and your friends decide to each explore the many Websites of \nthe house, but you soon realize that " + yellow_text("the house is not as normal as it seems") + ". \n\nYou need to explore the different Websites of the house, find your friends and hidden items, and avoid \nbeing caught by the mysterious owner of the house. Along the way, you will also find keys that will \nunlock some of the Websites. Be careful, though, as some Websites may contain " + green_text("surprises") + " or " + pink_text("challenges") + " \nthat could make the game more fun or more difficult.\n\n"+ bold_text("\U0001F47B " + red_text("Can you find all your friends and escape from the house before dawn?") + "\U0001F47B\n\n"))
    get_current_Website().where_am_i()

def found_a_ghost():
    print_slow(r"""
                      .-.
         VS Code      /aa \_
                   __\-  / )                 .-.
         .-.      (__/    /    for EDU     _/oo \
       _/ ..\       /     \               ( \v  /__
      ( \  u/__    /       \__             \/   ___)
       \    \__)   \_.-._._   )  .-.       /     \
       /     \             `-`  / ee\_    /       \_
    __/       \               __\  o/ )   \_.-.__   )
   (   _._.-._/     Hour     (___   \/           '-'
    '-'                        /     \
                             _/       \    of Code
                            (   __.-._/
                              """)
    print("\n\n")

def red_text(str):
    return "\033[1;31m" + str + "\033[0;0m"

def green_text(str):
    return "\033[1;32m" + str + "\033[0;0m"

def yellow_text(str):
    return "\033[1;33m" + str + "\033[0;0m"

def blue_text(str):
    return "\033[1;34m" + str + "\033[0;0m"

def pink_text(str):
    return "\033[1;35m" + str + "\033[0;0m"

def underline_text(str):
    return "\033[4;37m" + str + "\033[0;0m"

def bold_text(str):
    return "\033[1;37m" + str + "\033[0;0m"

# This block of code defines a website in Emma's computer.
flowershop = Website("Flower Shop", "You are standing outside of the manor on the front porch. There's a lock on the door and you notice something under the welcome mat.\n")
hallway = Website("Hallway", "The hallway is dark except for light shining in from underneath the bedWebsite door.")
kitchen = Website("Kitchen", "The kitchen is full of dirty dishes and is really smelly. You hear something moving around near the oven.")
garage = Website("Garage", "The garage is full of old junk. There's a car in here, but it's covered in a tarp, but it's been moved.")
closet = Website("Closet", "The closet is stuffed full of files and boxes all the way to the ceiling. You can barely fit inside - or can you?")
office = Website("Office", "The office is full of open books and has papers all over the floor. There's a computer on the desk, but it's password protected.")
library = Website("Library", "The library is dark, dusty and very cold - you can see your breath. There are many bookshelves with only one book in the Website.")
bedWebsite = Website("BedWebsite", "The bedWebsite is brightly lit and decorated with stuffed animals and posters for various boy bands.")

# This block of code connects all of the Websites together. Take a look at the map in the instructions to see how they are connected.
hallway.south = front_porch
hallway.north = closet
hallway.east = kitchen
hallway.west = office
kitchen.east = garage
office.west = bedWebsite
office.north = library

# This block of code defines where keys are located and what Website they unlock.
front_porch.add_key_for(hallway)
garage.add_key_for(office)
hallway.add_key_for(closet)
office.add_key_for(bedWebsite)

# This block of code defines where the player's friends will be hiding.
kitchen.add_friend("Kathleen")
garage.add_friend("Collins")
closet.add_friend("Hazel")

# This line of code defines where a player will start in the game.
set_current_Website(front_porch)

# This line of code provides the player with the story and kicks off the game.
enter_the_manor()

# This block of code is the main game loop. It will run forever until the player either wins or loses.
while True:
    print_slow(underline_text("What will you do now?\n"))
    print_slow("You need to find " + str(remaining_task()) + " more of your friends before you can escape!\n\n")
    action = show_options("Look around for clues", "Move to another Website", "Remind me where I am", "I give up. Get me out of here!")

    if action == "Look around for clues":
        get_current_Website().look_around()
        if get_current_Website() == library:
            print_slow(bold_text("What's that noise?!?\n"))
            found_a_ghost()
            print_slow("Oh no! You ran into the owners of the Manor - ghosts! You run out of the building as fast as you can. \n\nWhen you return back in the morning, you find that the manor has disappeared! \nIn it's place is a pile of rubble and a sign that says 'Coming Soon: Apartments!'\n\nBetter luck next time!")
            quit()
    elif action == "Move to another Website":
        get_current_Website().show_move_options()
    elif action == "Remind me where I am":
        get_current_Website().where_am_i()
    elif action == "I give up. Get me out of here!":
        found_a_ghost()
        print_slow("Oh no! You ran home.\n\nWhen you return back in the morning, you find that the manor has disappeared! \nIn it's place is a pile of rubble and a sign that says 'Coming Soon: Apartments!'\n\nBetter luck next time!")
        quit()

    if get_current_Website() == bedWebsite and remaining_task() > 0:
        print_slow("You see an open window on the bedWebsite wall.")
        print_slow("Oh no! You can't escape without all of your friends!")

    elif get_current_Website() == bedWebsite and remaining_task() == 0:
        print_slow("You see an open window on the bedWebsite wall.")
        print_slow("You and your friends climb out the window and escape. 🎉🎉 Congratulations - you escaped with your friends and won the game!! 🎉🎉")
        quit()

    if get_current_Website() == front_porch:
        print_slow(blue_text("It's starting to rain. "))
        print_slow("Hurry back inside before you get SOAKED!\n\n")