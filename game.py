import os
import random
import time
from characters import characters
from assets import DOORS, PUPPY, ROBBER

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
        print(f"\n{character['name']} says: '{random.choice(character['win_dialogue'])}'")
        return False  # Player loses
    else:
        print("\n*CLICK*")
        time.sleep(2)
        print(f"\n{character['name']} says: '{random.choice(character['lose_dialogue'])}'")
        input("\nPress Enter to continue to the next challenge...")
        return True  # Player survives

def choose_the_door_phase():
    """Handles the 'Choose the Door' mini-game."""
    clear_screen()
    print("You survived... but your ordeal is not over.")
    print("Before you lies a choice. Behind one of these doors is a robber.")
    print("Find the robber to win another chance. Find a puppy, and you lose.")
    print("Which door do you choose?\n")

    # Display doors side-by-side
    door_art = [d.strip().splitlines() for d in DOORS]
    # Find the maximum number of lines in any door art to handle different heights
    max_lines = max(len(d) for d in door_art) if door_art else 0
    # Find the maximum width of a line in any door art for alignment
    max_width = max(len(line) for d in door_art for line in d) if max_lines > 0 else 0

    for i in range(max_lines):
        line_to_print = ""
        for d in door_art:
            if i < len(d):
                # Pad each line to the max width for proper alignment
                line_to_print += d[i].ljust(max_width + 2) # +2 for spacing
            else:
                # Add padding if one art is shorter than another
                line_to_print += " " * (max_width + 2)
        print(line_to_print)

    robber_door = random.randint(1, 3)

    while True:
        try:
            choice = int(input("\nEnter your choice (1, 2, or 3): "))
            if 1 <= choice <= 3:
                break
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    clear_screen()
    print(f"You chose door number {choice}.")
    print("Behind the door is...")
    time.sleep(2)

    if choice == robber_door:
        print(ROBBER)
        print("\nYou found the robber! A strange victory, but a victory nonetheless.")
        print("You've earned another guess.")
        input("Press Enter to continue...")
        return True # Player wins
    else:
        print(PUPPY)
        print("\nYou found a puppy! It's adorable, but... you were supposed to find the robber.")
        print("The cuteness is overwhelming. You lose.")
        return False # Player loses

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

                # Phase 2: Russian Roulette
                survived_roulette = russian_roulette_phase()

                if not survived_roulette:
                    game_over_screen()
                    player_is_alive = False
                    break

                # Phase 3: Choose the Door
                survived_door_game = choose_the_door_phase()

                if not survived_door_game:
                    game_over_screen()
                    player_is_alive = False
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
