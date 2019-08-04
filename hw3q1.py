P1_TOKEN = 'X'
P2_TOKEN = 'O'
EMPTY_SPOT = '_'
MS_INVALID_MOVE = -1
MS_VALID_MOVE = 0
MS_OUT_OF_RANGE = 1
MS_OCCUPIED = 2
GS_FULL_BOARD = 0
GS_WIN = 1
GS_ONGOING = 2


def scan_dimensions():
    '''asks dimensions of the board
    if input is valid returns brd_input
    if input is not valid asks again until valid
    :return:brd_input: the size of the board
    '''
    brd_input = input('Please enter the dimensions of the board:')
    while (not brd_input.isdigit()) or (int(brd_input) < 2) \
        or (int(brd_input) > 9):
        print('\nBad input.')
        brd_input = input('Please enter the dimensions of the board:')
    return brd_input


def init_board(brd_sz):
    '''initialize board to EMPTY_SPOT
    :param brd_sz: the side of the board
    :return: the board'''
    board = [[EMPTY_SPOT for i in range(brd_sz)] for j in range(brd_sz)]
    return board


def print_board(board):
    '''print Tic-tac-toe board
    :param board: the game board'''
    board_size = len(board)
    print("\n")
    for i, row in enumerate(board[::-1]):
        print(str(board_size-i) + ' ' + ''
              .join(['|'+cell for cell in row]) + '|')
    print('  '+''.join([' {}'.format(i) for i in range(1, board_size+1)]))


def is_board_full(board):
    '''checks if the board is full
    :param:board: the board of the game
    :return: true if full, false if not full'''
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == '_':
                return False
    return True


def scan_move(curr_token):
    '''ask for and get current move from the player
    that uses specified input token
    :param curr_token: the char that represents the added token
    :return: ask_move: the move that the player wants to do: 'row col' '''
    ask_move = input('Player {}, Enter next move:'.format(curr_token))
    return ask_move


def check_move(board, move):
    '''check current move and return the result code
       MS_VALID_MOVE if the move can be executed
       MS_INVALID_MOVE if the move can't be executed
       MS_OUT_OF_RANGE if the input move is not a possible input
       MS_OCCUPIED if the move is of an already assigned square

       :param board: the game board
       :param move: the current move
       :return: the result code
       '''
    if (move.find(' ') == int(len(board))) or (move.find(' ') == 0) \
        or (move.count(' ') != 1):
        return MS_INVALID_MOVE
    else:
        move = move.split(' ')
    if (not move[0].isdigit()) or (not move[1].isdigit()):
        return MS_INVALID_MOVE
    if (int(move[0]) < 0) or (int(move[1]) < 0):
        return MS_INVALID_MOVE
    if (len(move[0]) > 1) or (len(move[1]) > 1):
        return MS_OUT_OF_RANGE
    if (int(move[0]) > len(board)) or (int(move[1]) > len(board))\
        or (int(move[0]) < 1) or (int(move[1]) < 1):
        return MS_OUT_OF_RANGE
    if board[int(move[0])-1][int(move[1])-1] != '_':
        return MS_OCCUPIED
    return MS_VALID_MOVE


def print_move_error(move, move_status):
    '''
    print a relevant error message for invalid move
    and asks for new input in case it is not MS_INVALID_MOVE
    :param move: the current move 'row col'
    :param move_status: integer describing the move status
    '''
    print("\n")
    print('Invalid move.', end=' ')
    if move_status == MS_OUT_OF_RANGE:
        print('Input move is out of range.')
    elif move_status == MS_OCCUPIED:
        print('Cell {},{} is not empty.'.format(move[0], move[2]))
    elif move_status == MS_INVALID_MOVE:
        print('Enter TWO proper coordinates! It\'s all over...')
    else:
        # SHOULDN'T GET HERE
        print('Error in print_move_error:Invalid move_status.')
    if move_status != MS_INVALID_MOVE:
        print('Please try again:')


def make_move(board, move, curr_token):
    '''
    assign token to square (ASSUME ALL VALID).
    :param board: the game board
    :param move: the square we want to assign
    the token to, move = [row,col]
    :param curr_token: the char that represents the added current token
    :return:
    '''
    board[move[0]][move[1]] = curr_token


def get_opposite_token(curr_token):
    ''' switches the tokens between turns
    :param curr_token: the current token
    :return: the opposite token
    '''
    if curr_token == P1_TOKEN:
        curr_token = P2_TOKEN
        return curr_token
    if curr_token == P2_TOKEN:
        curr_token = P1_TOKEN
        return curr_token


def is_col_win(board, move):
    ''' checks if the column in the board is full by a specific token
    :param board: the game board
    :param move: the last move that took place
    :return: true if the specific column in the board is full by a
    specific token
        '''
    num_col = int(move[1])
    num_row = int(move[0])
    n = 0
    for i in range(len(board)):
        if board[i][num_col] == board[num_row][num_col]:
            n += 1
        if n == len(board):
            return True


def is_row_win(board, move):
        ''' checks if the row in the board is full by a specific token
    :param board: the game board
    :param move: the last move that took place
    :return: true if the specific row in the board is full by a
    specific token
        '''
        n = 0
        num_col = int(move[1])
        num_row = int(move[0])
        for j in range(len(board)):
            if board[num_row][j] == board[num_row][num_col]:
                n += 1
            if n == len(board):
                return True


def is_slant_l2r_win(board, move):
    ''' checks if the left to right slant in the board is
    full by a specific token
        :param board: the game board
        :param move: the last move that took place
        :return: true if the specific slant in the board is full by a
        specific token
            '''
    n = 0
    num_col = int(move[1])
    num_row = int(move[0])
    for i in range(len(board)):
        for j in range(len(board)):
            if i+j ==len(board)-1:
                if board[i][j] == board[num_row][num_col]:
                    n += 1
                if n == len(board):
                    return True


def is_slant_r2l_win(board, move):
    ''' checks if the right to left slant in the board is
        full by a specific token
            :param board: the game board
            :param move: the last move that took place
            :return: true if the specific slant in the board is full by a
            specific token
                '''
    n = 0
    num_col = int(move[1])
    num_row = int(move[0])
    for i in range(len(board)):
        for j in range(len(board)):
            if i == j - (len(board)-1):
                if board[i][j] == board[num_row][num_col]:
                    n += 1
                    if n == len(board):
                        return True


def is_win(board, move):
    '''checks if there is a possibility for a win
    :param board: the board of the game
    :param move: the current move
    :return: true if there is a win, false otherwise'''
    if is_row_win(board, move) or is_col_win(board, move)\
    or is_slant_l2r_win(board,move) or is_slant_r2l_win(board, move):
        return True
    else:
        return False


def game_status(board, move):
    '''
    returns the status of the game based on the last move.
    :param board: the game board
    :param move: last move, move = [row,col]
    :return: current game status
    '''
    if is_win(board, move):
        return GS_WIN
    if is_board_full(board):
        return GS_FULL_BOARD
    return GS_ONGOING


def print_end_message(status, curr_token):
    '''
    prints a message that indicates game results
    :param status: the status of the game
    :param curr_token: the char that represents the added token
    :return:
    '''
    print('The game has ended!', end=' ')
    if status == GS_FULL_BOARD:
        print('It\'s a tie.')
    elif status == GS_WIN:
        print('Player {} has won!!!!!'
              .format(get_opposite_token(curr_token)))
    else:
        print('Error in print_end_message:'
                        'game has not ended')


def move_corrections(move):
    '''changes the content of move and transforms him to a list
    :param: move: the current move
    :return: move: the transformed move'''
    move = move.split(' ')
    move[0] = int(move[0]) - 1
    move[1] = int(move[1]) - 1
    return move


def play_turn(board, curr_token):
    '''
    play one turn of the game.
    :param board: the game board
    :param curr_token: the char that represents the added current token
    :return: false if the game is over. otherwise true
    '''
    move = scan_move(curr_token)
    move_status = check_move(board, move)
    if move_status == MS_INVALID_MOVE:
        print_move_error(move, move_status)
        return False
    while move_status != MS_VALID_MOVE:
        print_move_error(move, move_status)
        move = scan_move(curr_token)
        move_status = check_move(board, move)
        if move_status == MS_INVALID_MOVE:
            print_move_error(move, move_status)
            return False
    move = move_corrections(move)
    make_move(board, move, curr_token)
    print_board(board)
    return move

# Implenet here the main body of the game


def main():
    print('Welcome to Toe-Tac-Tic!')
    brd_sz = scan_dimensions()
    board = init_board(int(brd_sz))
    print_board(board)
    curr_token = P1_TOKEN
    move = play_turn(board, curr_token)
    while (move is not False) and game_status(board, move) == GS_ONGOING:
        curr_token = get_opposite_token(curr_token)
        move = play_turn(board, curr_token)
    if move is not False:
        status = game_status(board, move)
        print_end_message(status, curr_token)


if __name__ == "__main__":
    main()