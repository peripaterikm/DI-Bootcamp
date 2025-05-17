two_D_list = [['-', '-', '-'],
             ['-', '-', '-'],
             ['-', '-', '-']]

def display_board(field):
    for row in field:
        print(' '.join(row))

display_board(two_D_list)

def player_input(player, board):
    while True:
        row = int(input(f"{player}, enter row (0-2): "))
        col = int(input(f"{player}, enter column (0-2): "))

        if row not in range(3) or col not in range(3):
            print("Invalid position. Please enter numbers from 0 to 2.")
            continue

        # Проверка, что ячейка пуста
        if board[row][col] != '-':
            print("That cell is already taken. Choose another one.")
            continue

        return row, col  # Возвращаем координаты, если всё в порядке

#two_D_list[0][0] = 'x'
row, col = player_input(1, two_D_list)

display_board(two_D_list)