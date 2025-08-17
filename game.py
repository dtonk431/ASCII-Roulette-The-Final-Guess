import os
import random
import time
from characters import characters

def clear_screen():
    """Clears the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_title_screen():
    """Displays the title screen of the game."""
    clear_screen()
    print("************************************************************")
    print("*                                                          *")
    print("*        Welcome to GUESS THE NUMBER or... ELSE!           *")
    print("*                                                          *")
    print("************************************************************")
    print("\nI'm thinking of a number between 1 and 25.")
    print("Guess correctly, or face the consequences...")
    input("\nPress Enter to start...")

def get_player_guess():
    """Prompts the player for a number guess and handles invalid input."""
    while True:
        try:
            guess = int(input("I'm thinking of a number between 1 and 25. What is it? "))
            if 1 <= guess <= 25:
                return guess
            else:
                print("Invalid input. Please enter a number between 1 and 25.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def russian_roulette_phase():
    """Handles the Russian Roulette phase of the game."""
    character = random.choice(characters)
    clear_screen()
    print(character["art"])
    print(f"\n{character['name']} says: '{character['intro_dialogue']}'")

    print("\nSpinning the chamber...")
    time.sleep(2)

    # To build tension
    print("*click*")
    time.sleep(1)

    outcome = random.randint(1, 6)

    if outcome == 1: # The losing number
        print("\nBANG!")
        time.sleep(2)
        print(f"\n{character['name']} says: '{character['win_dialogue']}'")
        return False  # Player loses
    else:
        print("\n*CLICK*")
        time.sleep(2)
        print(f"\n{character['name']} says: '{character['lose_dialogue']}'")
        input("\nPress Enter to try guessing again...")
        return True  # Player survives

def game_over_screen():
    """Displays the game over screen."""
    clear_screen()
    print("************************************************************")
    print("*                                                          *")
    print("*                        GAME OVER                         *")
    print("*                                                          *")
    print("************************************************************")

def display_win_screen():
    """Displays the win screen with celebratory ASCII art."""
    clear_screen()
    print("""

        ___________
       '._==_==_=_.'
       .-\\:      /-.
      | (|:.     |) |
       '-|:.     |-'
         \\::.    /
          '::. .'
            ) (
          _.' '._
         `-------`

    """)
    print("************************************************************")
    print("*                                                          *")
    print("*            CONGRATULATIONS! YOU GUESSED IT!              *")
    print("*                                                          *")
    print("************************************************************")


def play_again():
    """Asks the player if they want to play again."""
    while True:
        choice = input("\nPlay Again? (yes/no): ").lower()
        if choice in ["yes", "y"]:
            return True
        elif choice in ["no", "n"]:
            return False
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

def main_game_loop():
    """The main game loop that controls the flow of the game."""
    while True:
        secret_number = random.randint(1, 25)
        player_is_alive = True

        while player_is_alive:
            clear_screen()
            guess = get_player_guess()

            if guess == secret_number:
                display_win_screen()
                break
            else:
                print("\nWrong. Now you must face the consequences.")
                input("Press Enter to continue...")
                player_is_alive = russian_roulette_phase()
                if not player_is_alive:
                    game_over_screen()
                    break

        if not play_again():
            break

    print("\nThanks for playing!")


def main():
    """Main function to run the game."""
    display_title_screen()
    main_game_loop()

if __name__ == "__main__":
    main()
