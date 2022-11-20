import random
import colorama
from colorama import Fore, Back, Style
colorama.init()

menu = """Welcome to battle ships
You will be playing against the computer.

How it works:
Each player has 7 ships to place on the grid.
In turns, each player will guess where the other player has placed their ships.
If a player hits a ship, that player can take another turn until they miss."""

#SHIPS
# 2x1 - 3
# 3x1 - 2
# 4x2 - 2

# SHIP SELECTION

computer_ships = [{"name": "rhib", "identifier": "R", "amount": 3 , "length": 2, "width": 1}, {"name": "destroyer", "identifier": "D", "amount": 2 , "length": 3, "width": 1}, {"name": "carrier", "identifier": "C", "amount": 2 , "length": 4, "width": 2}]
player_ships = [{"name": "rhib", "identifier": "R", "amount": 3 , "length": 2, "width": 1}, {"name": "destroyer", "identifier": "D", "amount": 2 , "length": 3, "width": 1}, {"name": "carrier", "identifier": "C", "amount": 2 , "length": 4, "width": 2}]

computer_grid = []
player_grid = []

# Creates the editble matrix inside a 2D list.
# 10 x 10 Grid
for i in range(100):
    computer_grid.append(" # ")
    player_grid.append(" # ")


# Displays what ships the user / computer can use.
def display_ships(user):
    print("\nAvailable Ships\n")
    if user == "computer":
        for ship in computer_ships:
            print(f"Ship: {ship['name']}")
            length = ship['length']
            width = ship['width']
            for i in range(length):
                print(f"{ship['identifier']}" * width, end="\n")
    elif user == "player":
        for ship in player_ships:
            print(f"Ship: {ship['name']}")
            length = ship['length']
            width = ship['width']
            for i in range(length):
                print(f"{ship['identifier']}" * width, end="\n")
            
        

def generate_computer_ships():
    # The random index this generates should be where the BOTTOM LEFT corner of the ship is (of the ship in default rotation).

    pass




# Outputs the computers grid (Will be hidden from the playing user in the future).
# Generates a 10 x 10 grid using 100 arrays
def display_computer_grid():
    grid_piece = 0
    for y in range(10):
        print("\n", end="")
        for x in range(10):
            print(computer_grid[grid_piece], end="")
            grid_piece += 1
    print("\n")

# Outputs the players grid 
# Generates a 10 x 10 grid using 100 arrays
def display_player_grid():
    grid_piece = 0
    for y in range(10):
        print("\n", end="")
        for x in range(10):
            print(player_grid[grid_piece], end="")
            grid_piece += 1
    print("\n")


# Takes the coordinates the user enters and turns it into the index of the selected grid piece.
# E.g., The user enters X = 3 and Y = 4. This should return index 32.
def coordinates_to_index(x, y): 
    row = (y * 10) -1
    column = (10 - x)
    index = row - column
    return index

# Allows a ships info to be found by name with the option of also printing that formatted info.
def get_ship_info_by_name(ship_name, print_info):
    for ship in computer_ships:
        if ship['name'] == ship_name:
            if print_info == True:
                print(f"Ship Information: \nName: {ship['name']} \nIdentifier: {ship['identifier']} \nLength: {ship['length']} \nWidth: {ship['width']} \nAmount: {ship['amount']}")
            return ship
    # If ship not found.
    return False


# Checks whether a ship collides with another ship during placement.
#! Currently doesnt support rotation.
#! Need to include border detection - URGENT - DONE I THINK
def check_bounds(ship, index, direction):
    ship_info = get_ship_info_by_name(ship, False)
    length = ship_info['length']
    width = ship_info['width']
    # Checks for other ships
    # Implements the checks for north facing ships
    # We are incrementing / decrementing the index by 10 to check above or below the ship by however far it extends.
    if direction == "North":
        for i in range(ship_info['length']):
            print(f"DEBUG: Checking index {index}")
            if index < 0:
                print("DEBUG: SHIP GOES OUT OF BOUNDS")
                return True, "OUT OF BOUNDS"
            if ship_info['width'] > 1:
                if computer_grid[index + (ship_info['width'] -1)] != " # ":
                    print(f"DEBUG (width): FOUND SHIP AT {index}")
                    return True, "A ship is already in this space"
            if computer_grid[index] != " # ":
                print(f"FOUND SHIP AT {index}")
                return True, "A ship is already in this space"
            index -= 10
        return False, "No Error"
        
# Totals up how many ships the user has to place down before the round can start.
def total_ships():
    total_ship_count = 0
    for i in computer_ships:
        total_ship_count += i['amount']
    return total_ship_count


# Allows the user or computer to place a ship at coordinates.
def place_ship():
    ships = total_ships()
    print("TOTAL SHIPS:", ships)
    
    while ships > 0:
        print("\nYou have started placing a ship.")
        ship = input("What ship do you want to place: ").lower()

        ship_info = get_ship_info_by_name(ship, False)

        if ship_info != False and ship_info["amount"] > 0:
            print(f"You selected a {ship}.")
            print(f"{Fore.RED}IMPORTANT: Ships are placed using the bottom left corner.{Style.RESET_ALL}\n")
            x = int(input("Ship cordinate X: "))
            y = int(input("Ship cordinate Y: "))
            index = coordinates_to_index(x, y)

            #Checks whether the ship hits another ship or is too big to fit where placed.
            direction = "North" #? Should be able to be changed / ship rotated in future.
            bounds, error = check_bounds(ship, index, direction)
            if bounds:
                print(error)
            else:
                # If check bounds returns false, that means that there are no collisions and a ship can be placed.
                # loops through the length to place each block after the collisions are checked.
                for i in range(ship_info['length']):
                    computer_grid[index] = f" {ship_info['identifier']} "
                    computer_grid[index + ship_info['width'] -1] = f" {ship_info['identifier']} "
                    index -= 10
                

                print(f"{ship} placed at ({x}, {y})")
                ship_info["amount"] -= 1 # Removes 1 from the placed ship amount.
                ships -= 1
                display_computer_grid()

        elif ship_info == False:
            print("Invalid Ship, please pick a ship listed.")
            
        else:
            print(f"{Fore.RED + 'You dont have any of these ships left!'}{Style.RESET_ALL}")
            

    




# Used to check if a ship or part of a ship is at the selected coordinate.
def check_ship(x, y):
    index = coordinates_to_index(x, y)
    if computer_grid[index] == " X ":
        return False, "Ship already sunk!"
    elif computer_grid[index] != " # ":
        # Ship found
        return True, "Ship found!"
    else:
        return False, "No ship there captin!"


def hunt():
    hunting = True
    while hunting == True:
        print("You are firing a missile.\nPick a grid piece.")
        x = int(input("Type the X coordinate of the grid: "))
        y = int(input("Type the Y coordinate of the grid: "))
        ship, check_ship_msg = check_ship(x, y)
        if ship:
            print("\n", check_ship_msg)
            computer_grid[coordinates_to_index(x,y)] = " X "
            display_computer_grid()
        else:
            print("\n", check_ship_msg)
            print("Computers turn! ")
            hunting = False

display_ships("computer")

display_computer_grid()

print("PLAYER GRID \n\n\n")
display_player_grid()

place_ship()

hunt()

print("END GRID:")
display_computer_grid()
