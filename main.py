import random 

treasure = "🏆"
trap = "💣"
clue = "🔎"
empty = " _"
hidden = " X"

def field_config (message): 
    try:
        value = int(input(message))
        return value
    except ValueError:
        print("Invalid input. Please enter an integer.")
    
def create_field(size): 
    field = []
    for i in range (size):
        row = []
        for j in range (size):
            row.append(empty)
        field.append(row)
    field[0][0] = empty
    return field

def distribute_elements(field, size, traps_quantity, clues_quantity): 
    all_positions = []
    for i in range (size):
        for j in range (size):
            if not (i == 0 and j == 0):
                all_positions.append((i,j))
    random.shuffle(all_positions)

    
    x, y = all_positions.pop()
    field[x][y] = treasure
    treasure_position = (x, y)

    
    for i in range (traps_quantity):
        x, y = all_positions.pop()
        field[x][y] = trap

    
    for i in range (clues_quantity):
        x, y = all_positions.pop()
        field[x][y] = clue

    return treasure_position

def show_field(field_size, field, revealed_positions): 
    print("\nCurrent field:")
    print("    " + " ".join(f"{i:2d}" for i in range(1, field_size + 1)))
    print("   " + "———" * field_size)
    for i in range(field_size):
        row = []
        for j in range (field_size):
            if (i, j) in revealed_positions:
                if field[i][j] == empty:
                    row.append(f"{field[i][j]:2s}")
                else:
                    row.append(f"{field[i][j]}")
            else:
                row.append(f"{hidden:2s}")
        print(f"{i + 1} | " + " ".join(row))

def get_move(field_size, revealed_positions): 
    while True:
        x = int(input(f"\nSelect a row (1 a {field_size}): ")) - 1
        y = int(input(f"Select a column (1 a {field_size}): ")) - 1
        if (x, y) in revealed_positions:
            print("This position has already been revealed... Choose another one.")
            continue
        return x, y
    
def clue_content(current_position, treasure_position): 
    x, y = current_position
    X, Y = treasure_position
    tip = []

    if X < x:
        tip.append("UP")
    elif X > x:
        tip.append("DOWN")

    if Y < y:
        tip.append("to the LEFT")
    elif Y > y:
        tip.append("to the RIGHT")

    if len(tip) == 2:
        return f"The treasure is {tip[0]} and {tip[1]}."
    return f"The treasure is {tip[0]}."

def process_move(field, current_position): 
    x, y = current_position
    square_content = field[x][y]
    if square_content == treasure:
        return treasure
    elif square_content == trap:
        return trap
    elif square_content == clue:
        return clue
    else:
        return empty
        

print("======= Mystic Treasure Hunt =======")

field_size = field_config("Select the field size (NxN): ")
field = create_field(field_size)
traps_quantity = random.randint(3, 6)
clues_quantity = random.randint(5, 8)
treasure_position = distribute_elements(field, field_size, traps_quantity, clues_quantity)
revealed_positions = set()
lifes = 3

show_field(field_size, field, revealed_positions)

while True:
    print(f"\nYou have {lifes} remaining lifes.")
    print(f"There is {traps_quantity} traps and {clues_quantity} clues remaining.")
    x, y = get_move(field_size, revealed_positions)
    revealed_positions.add((x, y))
    result = process_move(field,(x, y))

    if result == treasure:
        show_field(field_size, field, revealed_positions)
        print("\nYou've found the MYSTIC TREASURE! CONGRATULATIONS!")
        break
    elif result == trap:
        show_field(field_size, field, revealed_positions)
        print("\nYou've found a TRAP! Just lost one life.")
        traps_quantity -= 1
        lifes -= 1
        if lifes == 0:
            print("No more lifes. GAME OVER!")
            break
    elif result == clue:
        tip = clue_content((x, y), treasure_position)
        print(f"\nYou've found a CLUE: {tip}")
        show_field(field_size, field, revealed_positions)
        clues_quantity -= 1
    elif result == empty:
        print("\nEmpty square... there is nothing here")
        show_field(field_size, field, revealed_positions)