import random
import colorama
from colorama import Fore, Back, Style
colorama.init()

menu = """Welcome to battle ships!
You will be playing against the computer.

How it works:
Each player has 5 ships to place on the grid.
In turns, each player will guess where the other player has placed their ships.
If a player hits a ship, that player can take another turn until they miss."""

#SHIPS
# 2x1 - 3
# 3x1 - 2
# 4x2 - 2

# SHIP SELECTION

computer_ships = [{"name": "rhib", "identifier": "R", "amount": 2 , "length": 2, "width": 1}, {"name": "destroyer", "identifier": "D", "amount": 2 , "length": 3, "width": 1}, {"name": "carrier", "identifier": "C", "amount": 1 , "length": 4, "width": 2}]
player_ships = [{"name": "rhib", "identifier": "R", "amount": 2 , "length": 2, "width": 1}, {"name": "destroyer", "identifier": "D", "amount": 2 , "length": 3, "width": 1}, {"name": "carrier", "identifier": "C", "amount": 1 , "length": 4, "width": 2}]

computer_grid = []
player_grid = []

# ship_groups is meant to group together each index of every ship, so that it can be used to detect fully sunk ships later on.
computer_ship_groups = {}
player_ship_groups = {}

# Creates the editble matrix inside a 2D list.
# 10 x 10 Grid
for i in range(100):
    computer_grid.append(" # ")
    player_grid.append(" # ")

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


# Displays what ships the user / computer can use.
def display_ships():
    print("\nAvailable Ships\n")
    for ship in player_ships:
        print(f"Ship: {ship['name']}\n" + f"Amount: {ship['amount']}")
        length = ship['length']
        width = ship['width']
        # Prints the ships identifier out with its length * width.
        for i in range(length):
            print(f"{ship['identifier']}" * width, end="\n")


# Takes the coordinates the user enters and turns it into the index of the selected grid piece.
# E.g., The user enters X = 3 and Y = 4. This should return index 32.
def coordinates_to_index(x, y): 
    row = (y * 10) -1
    column = (10 - x)
    index = row - column
    return index

# Allows a ships info to be found by name with the option of also printing that formatted info.
def get_ship_info_by_name(ship_name, print_info, user):
    if user == "player":
        user_ships = player_ships
    else:
        user_ships = computer_ships

    for ship in user_ships:
        if ship['name'] == ship_name:
            if print_info == True:
                print(f"Ship Information: \nName: {ship['name']} \nIdentifier: {ship['identifier']} \nLength: {ship['length']} \nWidth: {ship['width']} \nAmount: {ship['amount']}")
            return ship
    # If ship not found.
    return False

# Totals up how many ships the user has to place down before the round can start.
def total_ships():
    total_ship_count = 0
    for i in player_ships:
        total_ship_count += i['amount']
    return total_ship_count


# Checks whether a ship collides with another ship during placement.
#! Currently doesnt support rotation.
def check_bounds(ship, index, direction, user):
    ship_info = get_ship_info_by_name(ship, False, user)
    # Checks for other ships
    # Implements the checks for north facing ships
    # We are incrementing / decrementing the index by 10 to check above or below the ship by however far it extends.
    if user == "player":
        user = player_grid
    else:
        user = computer_grid
    if direction == "North":
        for i in range(ship_info['length']):
            if index < 0:
                return True, "SHIP OUT OF BOUNDS"
            if ship_info['width'] > 1:
                if user[index + (ship_info['width'] -1)] != " # ":
                    print(f"DEBUG (width): FOUND SHIP AT {index}")
                    return True, "THIS SPACE IS ALRADY TAKEN."
                # Check if ships with a width greater than 1 are placed in the 10th column.
                # (Ship would go out of bounds if a ship with a width greater than 1 was placed here.)
                if index % 10 == 9:
                    print("TRIED INDEX: ", index)
                    return True, "SHIP EXTENDS OUT OF BOUNDS" 
            if user[index] != " # ":
                print(f"DEBUG: FOUND SHIP AT {index}")
                return True, "THIS SPACE IS ALRADY TAKEN."
            index -= 10
        return False, "No Error"
    




# Generates the computers ship placement.
# The random index this generates should be where the BOTTOM LEFT corner of the ship is (of the ship in default rotation).
def generate_computer_ships():
    ships = total_ships()
    direction = "North"
    while ships > 0:
        for ship in computer_ships:
            if ship['amount'] > 0:
                ship = ship['name']

                ship_info = get_ship_info_by_name(ship, False, "computer")

                index = random.randint(0, 98)
                bounds, error = check_bounds(ship, index, direction, "computer")
                if bounds:
                    print("COMPUTER (BOUNDS ERROR) - While placing ship")
                    print("COMPUTER (Placement)", error)
                else:
                    ship_indexes = []
                    print("Computer is placing", ship)
                    for i in range(ship_info['length']):
                        computer_grid[index] = f" {ship_info['identifier']} "
                        computer_grid[index + ship_info['width'] -1] = f" {ship_info['identifier']} "
                        # Stores the ships indexes into a array to be stored as a group later.
                        ship_indexes.append(index)
                        if ship_info['width'] > 1:
                            ship_indexes.append((index + ship_info['width'] -1))
                        index -= 10

                    print(f"{ship} placed at ({index})")
                    ship_info["amount"] -= 1 # Removes 1 from the selected ship amount.
                    ships -= 1 #Removes 1 from total ships
                    # The code below creates a dictionary with the shipp name & amount as an identifier and stores which indexes it has taken up.
                    # This will be used to check if a ship has been fully sunk or not.
                    # the name and the amount left of the ship have been added to create a unique id.
                    computer_ship_groups[ship_info['name'] + str(ship_info['amount'])] = ship_indexes
                    print("DEBUG: REMAINING SHIPS --> ", {ships})

    return computer_ship_groups

# Allows the user to place a ship at selected coordinates.
def place_ship():
    ships = total_ships()
    display_player_grid()
    while ships > 0:
        print("- " * 10 + "\nSHIP PLACEMENT\n" + "- " * 10)

        # Outputs type & amount of ship the user can place.
        print("Ships to place:")
        for ship in player_ships:
            print(f"{ship['amount']}x", f"{ship['name']}")

        ship = input("Select a ship to place: ").lower()

        ship_info = get_ship_info_by_name(ship, False, "player")

        # ship exists & user has ships left to place.
        if ship_info != False and ship_info["amount"] > 0:
            print(f"You selected a {ship}.")
            print(f"{Fore.RED}IMPORTANT: Ships are placed using the bottom left corner.{Style.RESET_ALL}\n")
            x = int(input("Ship cordinate X: "))
            y = int(input("Ship cordinate Y: "))
            index = coordinates_to_index(x, y)

            #Checks whether the ship hits another ship or is too large to fit where placed.
            direction = "North" #? Should be able to be changed / ship rotated in future.
            bounds, error = check_bounds(ship, index, direction, "player")
            if bounds:
                print(error)
            else:
                # If check bounds returns false, that means that there are no collisions and a ship can be placed.
                # loops through the length to place each block after the collisions are checked.
                ship_indexes = []
                for i in range(ship_info['length']):
                    player_grid[index] = f" {ship_info['identifier']} "
                    player_grid[index + ship_info['width'] -1] = f" {ship_info['identifier']} "
                    # Stores the ships indexes into a array to be stored as a group later.
                    ship_indexes.append(index)
                    if ship_info['width'] > 1:
                        ship_indexes.append((index + ship_info['width'] -1))
                    index -= 10
                

                print(f"{ship} placed at ({x}, {y})")
                ship_info["amount"] -= 1 # Removes 1 from the selected ship amount.
                ships -= 1 
                # The code below creates a dictionary with the shipp name & amount as an identifier and stores which indexes it has taken up.
                # This will be used to check if a ship has been fully sunk or not.
                # the name and the amount left of the ship have been added to create a unique id.
                player_ship_groups[ship_info['name'] + str(ship_info['amount'])] = ship_indexes
                display_player_grid()
                
                

        elif ship_info == False:
            print("Invalid Ship, please pick a ship listed.")      
        else:
            print(f"{Fore.RED + 'You dont have any of these ships left!'}{Style.RESET_ALL}")
    
    return player_ship_groups   

def check_game():
    for values in computer_ship_groups.values():
        for v in values:
            if computer_grid[v] != " S ":
                return False
    return True
                

# Used to check if a ship or part of a ship is at the selected coordinate.
def check_ship(index, user):
    if user == "player":
        user = computer_grid
    else:
        user = player_grid

    if user[index] == " X ":
        return False, "Ship already hit!"
    elif user[index] == " S ":
        return False, "Ship already sunk!"

    elif user[index] != " # ":
        # Ship found
        user[index] = " X " # Sets the index to be marked as hit.

        for values in computer_ship_groups.values():
            # Check if the ship has been fully sunk- Can be improved?
            if index in values: # Reduces checks
                for v in values:
                    if user[v] != " X ":
                        all_ship_values_hit = False
                        break
                    else:
                        all_ship_values_hit = True

                if all_ship_values_hit == True:
                    for v in values:
                        user[v] = " S "
                    return True, "Ship Sunk!"
                    

        return True, "Ship found!"
    else:
        computer_grid[index] = " O "
        return False, "No ship there captin!"



def player_hunt():
    hunting = True
    while hunting == True:
        print("You are firing a missile.\nPick a grid piece.")
        x = int(input("Type the X coordinate of the grid: "))
        y = int(input("Type the Y coordinate of the grid: "))
        check_index = coordinates_to_index(x, y)
        ship_found, check_ship_msg = check_ship(check_index, "player")
        if ship_found:
            display_computer_grid()
            print("\n" + check_ship_msg)
            if check_game(): #! OR HERE?
                print("\nGame Over! All ships sunk. Player Wins!\n")
                hunting = False
                return False
        else:
            display_computer_grid()
            print("\n" + check_ship_msg)
            hunting = False

comp_stats = {
    "guesses": [],
    "sunken": 0,
    "hits": []
}

def computer_hunt(stats):
    guesses = comp_stats["guesses"]
    sunken = comp_stats["sunken"]
    hits = comp_stats["hits"]
    a = True
    if len(guesses) < 1 or a == True:
        fire_index = random.randint(0, 100) # Picks a random index to hit to start off.
        result_bool, result_info = check_ship(fire_index, "computer")
        if result_info == "Ship already hit!":
            print("Computer - already hit ship -- SHOULDNT HAPPEN")

        elif result_info == "Ship already sunk!":
            print("Computer - ship already sunk")
        
        elif result_info == "Ship sunk!":
            print("Computer - sunk a ship")
            stats['sunken'] += 1

        elif result_info == "Ship found!":
            print("Computer - hit a ship")
            stats['guesses'].append(fire_index)
            stats['hits'].append(fire_index)

            
        elif result_info == "No ship there captin!":
            comp_stats['guesses'].append(fire_index)
    
        else:
            print(result_bool, result_info)


def game_master():
    # randomly generate the computers ships.
    generate_computer_ships()
    # allows the player to place their ships.
    place_ship()

    #? Could remove this. All this is useful for is the size of the ships...
    print("Players ships:")
    display_ships()

    #! DEBUG CODE V
    print("COMPUTER GRID \n\n")
    display_computer_grid()
    #! DEBUG CODE ^

    print("PLAYER GRID \n\n")
    display_player_grid()

    game_started = True
    while game_started:
        print("Players Turn!\n")
        if player_hunt() == False:
            game_started = False
            break
        print("Computers turn! ")
        computer_hunt(comp_stats)

game_master()



print("END GRID:")
display_computer_grid()
display_player_grid()
