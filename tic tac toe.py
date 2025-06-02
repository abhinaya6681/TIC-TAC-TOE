from colorama import Fore, Style, init
import math

init(autoreset=True)

PLAYER = "X"
AI = "O"

def print_board(board):
    print()
    for i, row in enumerate(board):
        print("   " + "   |   ".join(
            f"{Fore.RED + cell + Style.RESET_ALL}" if cell == PLAYER else
            f"{Fore.CYAN + cell + Style.RESET_ALL}" if cell == AI else
            str(i * 3 + j + 1)
            for j, cell in enumerate(row)))
        if i < 2:
            print("  " + "-" * 33)
    print()

def check_winner(board, player):
    for row in board:
        if all(cell == player for cell in row):
            return True
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True
    return False

def is_full(board):
    return all(cell != " " for row in board for cell in row)

def get_available_moves(board):
    return [(i, j) for i in range(3) for j in range(3) if board[i][j] == " "]

def minimax(board, depth, is_maximizing):
    if check_winner(board, AI):
        return 1
    if check_winner(board, PLAYER):
        return -1
    if is_full(board):
        return 0

    if is_maximizing:
        best_score = -math.inf
        for i, j in get_available_moves(board):
            board[i][j] = AI
            score = minimax(board, depth + 1, False)
            board[i][j] = " "
            best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for i, j in get_available_moves(board):
            board[i][j] = PLAYER
            score = minimax(board, depth + 1, True)
            board[i][j] = " "
            best_score = min(score, best_score)
        return best_score

def best_move(board):
    best_score = -math.inf
    move = None
    for i, j in get_available_moves(board):
        board[i][j] = AI
        score = minimax(board, 0, False)
        board[i][j] = " "
        if score > best_score:
            best_score = score
            move = (i, j)
    return move

def get_player_move(board):
    while True:
        try:
            move = int(input(f"{Fore.GREEN}Your move (1-9): ")) - 1
            row, col = divmod(move, 3)
            if board[row][col] == " ":
                return row, col
            else:
                print(f"{Fore.YELLOW}That cell is already taken.")
        except (ValueError, IndexError):
            print(f"{Fore.YELLOW}Invalid input. Enter a number between 1 and 9.")

def play_game():
    board = [[" " for _ in range(3)] for _ in range(3)]
    print(f"{Fore.MAGENTA}Welcome to Tic Tac Toe vs AI!\n")
    print("You are X, AI is O.")
    print("Board positions:")
    print_board([["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"]])

    while True:
        print_board(board)
        row, col = get_player_move(board)
        board[row][col] = PLAYER

        if check_winner(board, PLAYER):
            print_board(board)
            print(f"{Fore.GREEN}🎉 You win! Well played.")
            break
        if is_full(board):
            print_board(board)
            print(f"{Fore.CYAN}🤝 It's a draw!")
            break

        ai_row, ai_col = best_move(board)
        board[ai_row][ai_col] = AI
        print(f"{Fore.CYAN}AI chose position {(ai_row * 3 + ai_col + 1)}.")

        if check_winner(board, AI):
            print_board(board)
            print(f"{Fore.RED}💀 AI wins! Better luck next time.")
            break
        if is_full(board):
            print_board(board)
            print(f"{Fore.CYAN}🤝 It's a draw!")
            break

play_game()
