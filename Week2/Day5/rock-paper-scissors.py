# rock-paper-scissors.py
from game import Game

def get_user_menu_choice():
    print("\nMenu:")
    print("1. Play a new game")
    print("2. Show scores")
    print("3. Quit")
    choice = input("Enter your choice (1/2/3): ").strip()
    while choice not in ['1', '2', '3']:
        print("Invalid choice. Please try again.")
        choice = input("Enter your choice (1/2/3): ").strip()
    return choice

def print_results(results):
    print("\nGame Summary:")
    print(f"Wins: {results['win']}, Losses: {results['loss']}, Draws: {results['draw']}")
    print("Thank you for playing!")

def main():
    results = {"win": 0, "loss": 0, "draw": 0}
    while True:
        user_choice = get_user_menu_choice()
        if user_choice == '1':
            game = Game()
            result = game.play()
            results[result] += 1
        elif user_choice == '2':
            print_results(results)
        elif user_choice == '3':
            print_results(results)
            break

if __name__ == "__main__":
    main()
