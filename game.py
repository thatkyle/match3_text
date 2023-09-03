import random

# Initialize the grid
rows, cols = 12, 8
grid = [[{'block_type': random.choice('abcd')} for _ in range(cols)] for _ in range(rows)]
checked_grid = [[False for _ in range(cols)] for _ in range(rows)]
unique_cells = {}

# Initialize shapes
# Os represent matching block types
# Xs represent non-matching block types, or matching block types in cells that are not part of the shape
#TODO remove checked if not used
shape_dicts = [
    {'shape': ['OXX', 'OOO', 'OXX'], 'score': 5},
    {'shape': ['XOX', 'XOX', 'OOO'], 'score': 5},
    {'shape': ['XXO', 'OOO', 'XXO'], 'score': 5},
    {'shape': ['OOO', 'OXX', 'OXX'], 'score': 5},
    {'shape': ['OOO', 'XXO', 'XXO'], 'score': 5},
    {'shape': ['XXO', 'XXO', 'OOO'], 'score': 5},
    {'shape': ['OOO', 'XOX', 'XOX'], 'score': 5},
    {'shape': ['OXX', 'OXX', 'OOO'], 'score': 5},
    {'shape': ['XOX', 'OOO', 'XOX'], 'score': 5},
    {'shape': ['O', 'O', 'O', 'O', 'O'], 'score': 5},
    {'shape': ['OOOOO'], 'score': 5},
    {'shape': ['O', 'O', 'O', 'O'], 'score': 4},
    {'shape': ['OOOO'], 'score': 4},
    {'shape': ['OO', 'OO'], 'score': 4},
    {'shape': ['O', 'O', 'O'], 'score': 3},
    {'shape': ['OOO'], 'score': 3}
]

# Sort shapes by score in descending order
# Shapes with higher scores should always be above shapes with lower scores for
# shape matching logic to work properly. (i.e matches of 5 should always be above
# matches of 4, above matches of 3, etc.) This sort ensures the correct order.
shape_dicts = sorted(shape_dicts, key=lambda x: x['score'], reverse=True)

# Helper function to check for a match
def is_match(grid, shape, row, col):
    shape_rows, shape_cols = len(shape), len(shape[0])
    block_to_match = None
    matching_positions = []

    for r in range(shape_rows):
        for c in range(shape_cols):
            if shape[r][c] == 'O':
                if block_to_match is None:
                    block_to_match = grid[row + r][col + c]
                elif grid[row + r][col + c] != block_to_match:
                    return False, []
                matching_positions.append((row + r, col + c))
            elif shape[r][c] == 'X':
                if grid[row + r][col + c] == block_to_match:
                    continue
    return True if block_to_match is not None else False, matching_positions

# Function to find matches
def find_matches(grid, shape_dicts):
    matches = []
    
    for shape_dict in shape_dicts:
        shape = shape_dict['shape']
        score = shape_dict['score']
        shape_rows, shape_cols = len(shape), len(shape[0])
        
        for row in range(rows - shape_rows + 1):
            for col in range(cols - shape_cols + 1):
                # Skip this cell if it's already checked
                if checked_grid[row][col]:
                    continue
                
                match, positions = is_match(grid, shape, row, col)
                
                if match:
                    # Add to matches
                    matches.append((shape, positions, score))
                    
                    # Update the 'checked' grid
                    for r, c in positions:
                        checked_grid[r][c] = True

    # Sort matches by score (number of cells)
    # matches.sort(key=lambda x: len(x[1]), reverse=True)
    
    # Remove duplicates and partail matches
    unique_cells = set()
    unique_matches = []
    
    for shape, positions, score in matches:
        new_positions = [pos for pos in positions if pos not in unique_cells]
        
        if new_positions and len(new_positions) == score:
            unique_matches.append((shape, new_positions))
            unique_cells.update(new_positions)
    
    return unique_matches


# Function to update the grid
def update_grid(grid, matches):
    for _, positions in matches:
        for row, col in positions:
            grid[row][col] = None  # Mark as empty

    # Let the letters above fall down
    rows, cols = len(grid), len(grid[0])
    for col in range(cols):
        empty_row = rows - 1
        for row in reversed(range(rows)):
            if grid[row][col] is None:
                continue
            else:
                grid[empty_row][col] = grid[row][col]
                if empty_row != row:
                    grid[row][col] = None
                empty_row -= 1

    # Fill in the empty spots at the top with new random letters
    for row in range(rows):
        for col in range(cols):
            if grid[row][col] is None:
                grid[row][col] = random.choice('ABCD')

    return grid


# Main loop
score = 0
while True:
    # Print the grid for debugging
    for row in grid:
        print(' '.join(cell['block_type'] if cell['block_type'] else '.' for cell in row))
    print()

    matches = find_matches(grid, shape_dicts)
    
    if matches:
        print("Found matches:")
        for match in matches:
            print(f"{match}\n")
        score += sum(len(positions) for _, positions in matches)
        for _, positions in matches:
            for position in positions:
                grid[position[0]][position[1]]['block_type'] = grid[position[0]][position[1]]['block_type'].upper()
        for row in grid:
            print(' '.join(cell['block_type'] if cell['block_type'] else '.' for cell in row))
        print()
        print(f"Score: {score}")
        # update_grid(grid, matches)
    else:
        print("No matches found.")

    user_input = input("Press 'q' to quit or any other key to continue: ")
    if user_input == 'q':
        break