from config import get_config

BOARD_MAX_SQUARE_SIZE = get_config("board_max_square_size", "cw")

prompts = {
    "greet_1": "====Welcome to Cell War!====",
    "require_size": f"Input Board's Square Size! Max size is {BOARD_MAX_SQUARE_SIZE}, Format's like this: `!size7`",
    "require_size_!valid": "Square Size (a number) not valid",
    "waiting_for_start_instruction": "Start the game once you're ready! Notice: A game must have at least 1 player and 2 characters to start.",
    "wait_for_first_player": "The game must have at least 1 player to start!",
    "wait_for_first_char": "The game must have at least 2 characters to start!",
    "still_waiting_to_start": "The game is still running, prepare to start or use `!exit` to end the session!",
    "still_waiting_for_input": "The game is still running, proceed or use `!exit` to end the session!",
    "require_move": "Input Your Character's Move! Format's like this: `!move2,3`",
    "require_move_!valid": "Character move not valid!",
    "require_move_!valid::out_of_bounds": "Your move is out of bounds!",
    "require_move_!valid::beyond_mv": "Your move is beyond the character's MV!",
    "require_move_!valid::tile_occupied": "At your move's destination already has another character!",
    "require_skill": "Input the skill (and its arguments)!"
    
}

def get(key):
    try:
        return prompts[key]
    except KeyError:
        return f'[prompts.{key} not found]'