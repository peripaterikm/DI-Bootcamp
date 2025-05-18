# two_D_list = [['-', '-', '-'],
#              ['-', '-', '-'],
#              ['-', '-', '-']]

# def display_board(field):
#     for row in field:
#         print(' '.join(row))

# display_board(two_D_list)

# def player_input(player, board):
#     while True:
#         row = int(input(f"{player}, enter row (0-2): "))
#         col = int(input(f"{player}, enter column (0-2): "))

#         if row not in range(3) or col not in range(3):
#             print("Invalid position. Please enter numbers from 0 to 2.")
#             continue

#         # Проверка, что ячейка пуста
#         if board[row][col] != '-':
#             print("That cell is already taken. Choose another one.")
#             continue

#         return row, col  # Возвращаем координаты, если всё в порядке

# #two_D_list[0][0] = 'x'
# row, col = player_input(1, two_D_list)

# display_board(two_D_list)

# Step 1: Representing the Game Board
def create_board():
    return [[" " for _ in range(3)] for _ in range(3)]

# Step 2: Displaying the Game Board
def display_board(board):
    print("\n")
    for row in board:
        print(" | ".join(row))
        print("-" * 9)
    print("\n")

# Step 3: Getting Player Input
def player_input(player, board):
    while True:
        try:
            row = int(input(f"{player}, enter row (0-2): "))
            col = int(input(f"{player}, enter column (0-2): "))
            if row in range(3) and col in range(3):
                if board[row][col] == " ":
                    return row, col
                else:
                    print("That cell is already taken.")
            else:
                print("Row and column must be between 0 and 2.")
        except ValueError:
            print("Please enter valid numbers.")

# Step 4: Checking for a Winner
def check_win(board, player):
    # Check rows
    for row in board:
        if all(cell == player for cell in row):
            return True
    # Check columns
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True
    # Check diagonals
    if all(board[i][i] == player for i in range(3)):
        return True
    if all(board[i][2 - i] == player for i in range(3)):
        return True
    return False

# Step 5: Checking for a draw
def check_draw(board):
    return all(cell != " " for row in board for cell in row)

# Step 6: Main Game Loop
def play():
    board = create_board()
    current_player = "X"

    while True:
        display_board(board)
        row, col = player_input(current_player, board)
        board[row][col] = current_player

        if check_win(board, current_player):
            display_board(board)
            print(f"{current_player} wins! 🎉")
            break
        elif check_draw(board):
            display_board(board)
            print("It's a draw! 🤝")
            break
        else:
            # Switch players
            current_player = "O" if current_player == "X" else "X"

# Run the game
play()
