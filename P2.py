from collections import defaultdict

# Maze dimensions
ROWS = 5
COLS = 6

# Obstacles are stored as (row, column)
OBSTACLES = {
    (1, 1), (1, 2), (1, 3), (1, 4), (2, 1), (2, 4), (3, 1)
    }

# Create a list containing every open square in the maze
OPEN_CELLS = []

for row in range(ROWS):
    for col in range(COLS):
        if (row, col) not in OBSTACLES:
            OPEN_CELLS.append((row, col))

# Direction order matches the assignment: West, North, East, South
DIRECTIONS = [
    (0, -1), (-1, 0), (0, 1), (1, 0)
    ]

WEST = 0
NORTH = 1
EAST = 2
SOUTH = 3

# Sensor probabilities
DETECT_OBSTACLE = 0.95
MISS_OBSTACLE = 0.05
FALSE_OBSTACLE = 0.15
DETECT_OPEN = 0.85

# Movement probabilities
MOVE_STRAIGHT = 0.70
DRIFT_LEFT = 0.20
DRIFT_RIGHT = 0.10


def is_open(cell):
    """Return True if the cell is inside the maze and is not an obstacle."""



def get_neighbor(cell, direction):
    """Return the neighboring cell in the selected direction."""


def has_obstacle(cell, direction):
    """Check whether an obstacle or maze boundary is in a direction."""


def create_initial_belief():
    """Give every open square the same starting probability."""


def sensor_reading_probability(actual_obstacle, reading):
    """Return the probability of one sensor reading."""


def evidence_probability(cell, evidence):
    """Calculate the probability of receiving the complete sensor evidence
    while the robot is in a particular cell."""


def normalize(belief):
    """Adjust probabilities so that they add up to 1."""


def filter_after_sensing(prior_belief, evidence):
    """Update the location probabilities using sensor evidence."""


def move_or_bounce(cell, direction):
    """Move into the neighboring square if it is open.
    Otherwise, stay in the original square."""


def predict_after_moving(prior_belief, commanded_direction):
    """Update probabilities using the windy movement model."""


def print_belief_grid(title, belief):
    """Print one probability grid as percentages."""







def main():
    belief = create_initial_belief()

    print_belief_grid(
        "Initial Location Probabilities",
        belief
    )

    belief = filter_after_sensing(belief, [0, 0, 0, 1])
    print_belief_grid(
        "Filtering after Evidence [0, 0, 0, 1]",
        belief
    )

    belief = predict_after_moving(belief, NORTH)
    print_belief_grid(
        "Prediction after Action N",
        belief
    )

    belief = filter_after_sensing(belief, [1, 0, 0, 0])
    print_belief_grid(
        "Filtering after Evidence [1, 0, 0, 0]",
        belief
    )

    belief = predict_after_moving(belief, NORTH)
    print_belief_grid(
        "Prediction after Action N",
        belief
    )

    belief = filter_after_sensing(belief, [1, 1, 0, 0])
    print_belief_grid(
        "Filtering after Evidence [1, 1, 0, 0]",
        belief
    )

    belief = predict_after_moving(belief, EAST)
    print_belief_grid(
        "Prediction after Action E",
        belief
    )

    belief = filter_after_sensing(belief, [0, 1, 1, 0])
    print_belief_grid(
        "Filtering after Evidence [0, 1, 1, 0]",
        belief
    )