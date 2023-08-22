import os

def choose_game_type():
    """ Allows the player to choose whether to play against the computer or against another player. """
    game_type = input("You want to play against another player or computer? [Player/Computer]: ").lower()

    while game_type not in ['computer', 'c', 'player', 'p']:
        game_type = input('Type "Player" if you want to play with another person or "Computer" if you want '
                          'to play against computer: ').lower()

    if game_type == 'computer' or game_type == 'c':
        players = ["Player", "Computer"]
    else:
        players = ["Player 1", "Player 2"]
    return players


CENTER = ['b2']
CORNERS = ['a1', 'a3', 'c1', 'c3']
SIDES = ['a2', 'b1', 'b3', 'c2']
WINNING_SEQUENCES = [
    ['a1', 'a2', 'a3'],
    ['b1', 'b2', 'b3'],
    ['c1', 'c2', 'c3'],
    ['a1', 'b1', 'c1'],
    ['a2', 'b2', 'c2'],
    ['a3', 'b3', 'c3'],
    ['a1', 'b2', 'c3'],
    ['a3', 'b2', 'c1']
]
board = {
    'row0': '    1   2   3',
    'mid_row': '   -----------',
    'a1': ' A    ',
    'a2': '|   |',
    'a3': '   ',
    'b1': ' B    ',
    'b2': '|   |',
    'b3': '   ',
    'c1': ' C    ',
    'c2': '|   |',
    'c3': '   '
}

players_names = choose_game_type()
player_moves = {players_names[0]: [], players_names[1]: []}
marks = {players_names[0]: {'a1': ' A  X ',
                            'a2': '| X |',
                            'a3': ' X ',
                            'b1': ' B  X ',
                            'b2': '| X |',
                            'b3': ' X ',
                            'c1': ' C  X ',
                            'c2': '| X |',
                            'c3': ' X '
                            },

         players_names[1]: {'a1': ' A  O ',
                            'a2': '| O |',
                            'a3': ' O ',
                            'b1': ' B  O ',
                            'b2': '| O |',
                            'b3': ' O ',
                            'c1': ' C  O ',
                            'c2': '| O |',
                            'c3': ' O '
                            }
         }

def draw_board():
    """ Function draws a game board """
    print(board['row0']+'\n',
          board['a1'] + board['a2'] + board['a3']+'\n',
          board['mid_row']+'\n',
          board['b1'] + board['b2'] + board['b3']+'\n',
          board['mid_row'] + '\n',
          board['c1'] + board['c2'] + board['c3'] + '\n'
          )

def move(player_no: str):
    """ It is responsible for the user's movement. It allows the user to select a field and check if it is free."""

    if player_no == 'Computer':
        player_move = computer_algorithm()
    else:
        player_move = input(player_no + ': ').lower()

    # Checks if the user entered the correct field
    if player_move not in CENTER + CORNERS + SIDES:
        print("Wrong place")
        move(player_no)
    else:
        # Checks if the space is already taken
        if player_move in player_moves[players_names[0]]+player_moves[players_names[1]]:
            print("Place already taken")
            move(player_no)
        else:  # Updates the game board and saves the player's choice
            board[player_move] = marks[player_no][player_move]
            player_moves[player_no].append(player_move)

def result(player_no: str):
    """ Checks the score of the game. Returns string indicating which player won or information about a tie"""
    for sequence in WINNING_SEQUENCES:
        if all(item in player_moves[player_no] for item in sequence):
            return f"{player_no} wins!"
    if sum(len(values) for values in player_moves.values()) == 9:
        return "Tie!"

def another_game():
    """ Allows the player to decide if he wants to play again. If so, it resets the board and the player_moves """

    end_game_choice = input("Do you want to play again? [Y/N]: ").lower()

    while end_game_choice != "y" and end_game_choice != 'n':
        print("Please type Y if you want to play again or N if you want to end game.")
        end_game_choice = input("Do you want to play again? [Y/N]: ").lower()

    if end_game_choice == "n":
        global is_on
        is_on = False
    elif end_game_choice == 'y':
        print("New Game")
        global board, player_moves
        board = {
            'row0': '    1   2   3',
            'mid_row': '   -----------',
            'a1': ' A    ',
            'a2': '|   |',
            'a3': '   ',
            'b1': ' B    ',
            'b2': '|   |',
            'b3': '   ',
            'c1': ' C    ',
            'c2': '|   |',
            'c3': '   '
        }
        player_moves = {players_names[0]: [], players_names[1]: []}

def computer_algorithm():
    """ The function responsible for the plays of the computer.
    Returns a string as the place the computer wants to play. """

    # Checks if two out of three places in winning_sequences for Computer are occupied and takes the last place to win.
    for seq in WINNING_SEQUENCES:
        field_taken = [n for n in seq if n in player_moves['Computer'] and n not in player_moves["Player"]]
        field_missing = [n for n in seq if n not in player_moves['Computer'] + player_moves["Player"]]
        if len(field_taken) == 2 and len(field_missing) == 1:
            return field_missing[0]

    # Blocks an opponent if he can win in the next turn
    for seq in WINNING_SEQUENCES:
        field_taken = [n for n in seq if n in player_moves['Player'] and n not in player_moves["Computer"]]
        field_missing = [n for n in seq if n not in player_moves['Computer'] + player_moves["Player"]]
        if len(field_taken) == 2 and len(field_missing) == 1:
            return field_missing[0]

    # Moves to middle, if free
    if CENTER[0] not in player_moves["Player"] + player_moves['Computer']:
        return CENTER[0]

    # Plays the opposite corner to the opponent
    for n in range(4):
        if CORNERS[n] in player_moves["Player"] and \
                CORNERS[(n + 1) * -1] not in player_moves["Player"] + player_moves['Computer']:
            return CORNERS[(n + 1) * -1]

    # If two opposite corners are occupied by the opponent, plays the side
    for n in range(4):
        if CORNERS[n] in player_moves["Player"] and CORNERS[(n + 1) * -1] in player_moves["Player"] and \
                SIDES[n] not in player_moves["Player"] + player_moves['Computer']:
            return SIDES[n]

    # Plays the corner
    for n in CORNERS:
        if n not in player_moves["Player"] + player_moves["Computer"]:
            return n

    # Plays the side
    for n in SIDES:
        if n not in player_moves["Player"] + player_moves["Computer"]:
            return n

# Main loop of the game. It draws the game board, makes the players' moves and checks the result.
is_on = True
while is_on:
    for player in player_moves:
        os.system('cls')
        draw_board()
        move(player)
        if result(player) is not None:
            os.system('cls')
            draw_board()
            print(result(player))
            another_game()
            break
