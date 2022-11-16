import random

menu = """Welcome to battle ships
You will be playing against the computer.

How it works:
Each player has 7 ships to place on the grid.
In turns, each player will guess where the other player has placed their ships.
If a player hits a ship, that player can take another turn until they miss."""

#SHIPS
# 1x 2
# 2x 3
# 2x 4
# 1x 5

# SHIP SELECTION

computer_ships = [{"name": "rhib", "identifier": "R", "amount": 2 , "length": 1, "width": 1}, {"name": "destroyer", "identifier": "D", "amount": 1 , "length": 4, "width": 2}]

# Displays what ships the user / computer can use.
def display_ships():
    print("\nAvailable Ships\n")
    for ship in computer_ships:
        print(f"Ship: {ship['name']}")
        length = ship['length']
        width = ship['width']
        for i in range(length):
            print("D" * width, end="\n")
            
        

def generate_computer_ships():
    # The random index this generates should be where the BOTTOM LEFT corner of the ship is (of the ship in default rotation).
    random = random.randint(0, 99)
    for ship in computer_ships:
        if ship['amount'] > 0:
            place_ship()
    pass


computer_grid = []

# Creates the editble matrix inside a 2D list.
# 10 x 10 Grid
for i in range(100):
    computer_grid.append(" # ")

# Generates the computers grid (Will be hidden from the playing user in the future).
# Generates a 10 x 10 grid using 100 arrays
def display_computer_grid():
    grid_piece = 0
    for y in range(10):
        print("\n", end="")
        for x in range(10):
            print(computer_grid[grid_piece], end="")
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
            # print(f"Index of {ship_name} is {ship}")
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
        


# Allows the user or computer to place a ship at coordinates.
def place_ship():
    ships = 4
    while ships > 0:
        print("You have started placing a ship.")
        ship = input("What ship do you want to place: ").lower()

        ship_info = get_ship_info_by_name(ship, True)

        if ship_info != False and ship_info["amount"] > 0:
            print(f"You selected a {ship}.")
            print("IMPORTANT:\nShips are placed using the bottom left corner.\n")
            x = int(input("Ship cordinate X: "))
            y = int(input("Ship cordinate Y: "))
            index = coordinates_to_index(x, y)

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
                    # if computer_grid[index + (ship_info['width'] -1)] != " # ":
                    index -= 10
                    ships -= 1

                print(f"{ship} placed at ({x}, {y})")
                display_computer_grid()

        elif ship_info == False:
            print("Invalid Ship, please pick a ship listed.")
            place_ship()
        else:
            print("You dont have any of these ships left!")
            place_ship()

    




# Used to check if a ship or part of a ship is at the selected coordinate.
def check_ship(x, y):
    index = coordinates_to_index(x, y)
    if computer_grid[index] != " # ":
        print("Ship found!") #! Debug statement
        return True
    else:
        return False

def hunt():
    print("You are firing a missile.\nPick a grid piece.")
    x = int(input("Type the X coordinate of the grid: "))
    y = int(input("Type the Y coordinate of the grid: "))
    if check_ship(x, y):
        print("\nBang! Ship Sunk.")
        computer_grid[coordinates_to_index(x,y)] != " X "
    else:
        print("\nNo ship there captin!")

display_ships()

display_computer_grid()

place_ship()

hunt()
display_computer_grid()
hunt()
