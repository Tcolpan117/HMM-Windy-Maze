from collections import defaultdict
import datetime

# Map dimensions
ROWS = 5
COLS = 6

# Obstacles
OBSTACLES = {(1, 1), (1, 2), (1, 3), (1, 4), (2, 1), (2, 4), (3, 1)}

# List containing the open squares
OPEN_CELLS = []

for row in range(ROWS):
    for col in range(COLS):
        if (row, col) not in OBSTACLES:
            OPEN_CELLS.append((row, col))

# Direction order: west, north, east, south
DIRECTIONS = [(0, -1), (-1, 0), (0, 1), (1, 0)]

WEST = 0
NORTH = 1
EAST = 2
SOUTH = 3

# Evidence conditional probabilities
DETECT_OBSTACLE = 0.95
MISS_OBSTACLE = 0.05
FALSE_OBSTACLE = 0.15
DETECT_OPEN = 0.85

# Transitional probabilities
MOVE_FORWARD = 0.70
DRIFT_LEFT = 0.20
DRIFT_RIGHT = 0.10


def is_open(cell):
    """Returns true if the cell is inside the map and is not an obstacle"""
    return (0 <= cell[0] < ROWS) and (0 <= cell[1] < COLS) and (cell not in OBSTACLES)

def get_neighbor(cell, direction):
    """Returns neighboring cell in direction"""
    return (cell[0] + DIRECTIONS[direction][0], cell[1] + DIRECTIONS[direction][1])

def has_obstacle(cell, direction):
    """Checks if it's an obstacle in direction"""
    return not is_open(get_neighbor(cell, direction))

def sensor_probability(actual_obstacle, reading):
    """Returns probability of one sensor reading"""
    if actual_obstacle:
        if reading == 1:
            return DETECT_OBSTACLE

        return MISS_OBSTACLE

    if reading == 1:
        return FALSE_OBSTACLE

    return DETECT_OPEN

def evidence_probability(cell, evidence):
    """Calculates the probability of receiving the complete sensor evidence"""
    probability = 1.0
    for i, reading in enumerate(evidence):
        actual_obstacle = has_obstacle(cell, i)
        probability *= sensor_probability(actual_obstacle, reading)

    return probability

def filter_sensing(prior_belief, evidence):
    """Updates location probabilities using sensor evidence"""
    new_belief = {}

    for cell in prior_belief:
        new_belief[cell] = prior_belief[cell] * evidence_probability(cell, evidence)
    
    # Makes probabilities add up to 1
    total = sum(new_belief.values())
    for cell in new_belief:
        new_belief[cell] /= total
    return new_belief

def move(cell, direction):
    """Moves into the neighboring square if it is open or stays in original square"""
    destination = get_neighbor(cell, direction)
    
    # Returns new or original square if blocked
    if is_open(destination):
        return destination

    return cell

def predict_moving(prior_belief, commanded_direction):
    """Updates probabilities using windy movement"""
    predicted_belief = defaultdict(float)

    left_direction = (commanded_direction - 1) % 4
    right_direction = (commanded_direction + 1) % 4

    movements = [
        (commanded_direction, MOVE_FORWARD),
        (left_direction, DRIFT_LEFT),
        (right_direction, DRIFT_RIGHT)
    ]

    for direction, probability in movements:
        for cell in prior_belief:
            destination = move(cell, direction)

            predicted_belief[destination] += (prior_belief[cell] * probability)
    return predicted_belief

def print_map(belief):
    """Prints map with current location probabilities"""
    for row in range(ROWS):
        
        for col in range(COLS):
            cell = (row, col)

            if cell in OBSTACLES:
                print("##### ", end=" ")
            else:
                print(f"{belief[cell] * 100:5.2f} ", end=" ")

        print(" ")
    print(" ")

def main():

    # Gives open squares same initial probability
    belief = {}
    probability = 1.0 / len(OPEN_CELLS)

    for cell in OPEN_CELLS:
        belief[cell] = probability

    now = datetime.datetime.now()
    
    print("Students:")
    print("Gustavo Abreu")
    print("Taylan Colpan")
    print(now.strftime("Current time: %m-%d-%Y %H:%M:%S"))
    print(" ")

    print("Initial Location Probabilities")
    print_map(belief)

    print("Filtering after Evidence [0, 0, 0, 1]")
    belief = filter_sensing(belief, [0, 0, 0, 1])
    print_map(belief)

    print("Prediction after Action N")
    belief = predict_moving(belief, NORTH)
    print_map(belief)

    print("Filtering after Evidence [1, 0, 0, 0]")
    belief = filter_sensing(belief, [1, 0, 0, 0])
    print_map(belief)

    print("Prediction after Action N")
    belief = predict_moving(belief, NORTH)
    print_map(belief)

    print("Filtering after Evidence [1, 1, 0, 0]")
    belief = filter_sensing(belief, [1, 1, 0, 0])
    print_map(belief)

    print("Prediction after Action E")
    belief = predict_moving(belief, EAST)
    print_map(belief)

    print("Filtering after Evidence [0, 1, 1, 0]")
    belief = filter_sensing(belief, [0, 1, 1, 0])
    print_map(belief)

main()