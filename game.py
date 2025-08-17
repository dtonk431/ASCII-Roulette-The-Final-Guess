import kivy
kivy.require('2.3.1')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty, ObjectProperty, NumericProperty
from kivy.clock import Clock
import random

from characters import characters
from assets import DOORS, PUPPY, ROBBER

class GameManager(ScreenManager):
    secret_number = NumericProperty(0)
    current_character = ObjectProperty(None)
    robber_door = NumericProperty(0)

    def start_new_game(self):
        """Resets game state for a new round."""
        self.secret_number = random.randint(1, 25)
        # Reset guessing screen message
        guessing_screen = self.get_screen('guessing')
        guessing_screen.update_message("I'm thinking of a number between 1 and 25...")
        guessing_screen.ids.guess_input.text = ""
        self.current = 'guessing'

    def check_guess(self, guess_text):
        """Checks the player's number guess."""
        guessing_screen = self.get_screen('guessing')
        try:
            guess = int(guess_text)
            if not (1 <= guess <= 25):
                guessing_screen.update_message("Number must be between 1 and 25.")
                return

            if guess == self.secret_number:
                self.get_screen('result').show_win()
                self.current = 'result'
            else:
                guessing_screen.update_message(f"'{guess}' is wrong. Face the consequences.")
                self.current_character = random.choice(characters)
                # Use a short delay before transitioning to roulette
                Clock.schedule_once(lambda dt: self.transition_to_screen('roulette'), 1.5)
        except ValueError:
            guessing_screen.update_message("Please enter a valid number.")

    def play_roulette(self):
        """Simulates the Russian Roulette event."""
        roulette_screen = self.get_screen('roulette')
        roulette_screen.show_outcome_text("*click*")

        # Schedule the actual outcome reveal
        Clock.schedule_once(self.reveal_roulette_outcome, 2)

    def reveal_roulette_outcome(self, dt):
        """Reveals the roulette outcome and transitions."""
        outcome = random.randint(1, 6)
        roulette_screen = self.get_screen('roulette')

        if outcome == 1: # Player loses
            roulette_screen.show_outcome_text("BANG!")
            message = f"{self.current_character['name']} says: '{random.choice(self.current_character['win_dialogue'])}'"
            self.get_screen('result').show_game_over(message)
            Clock.schedule_once(lambda dt: self.transition_to_screen('result'), 2)
        else: # Player survives
            roulette_screen.show_outcome_text("*CLICK*... you survive. For now.")
            self.robber_door = random.randint(1, 3)
            Clock.schedule_once(lambda dt: self.transition_to_screen('door'), 2)

    def play_door_game(self, door_number):
        """Handles the 'Choose the Door' mini-game logic."""
        door_screen = self.get_screen('door')
        door_screen.reveal_door(door_number, self.robber_door)

        if door_number == self.robber_door:
            # Player wins, schedule transition back to guessing
            Clock.schedule_once(lambda dt: self.start_new_game(), 3)
        else:
            # Player loses, schedule game over
            self.get_screen('result').show_game_over("You found a puppy! Adorable... but you lose.")
            Clock.schedule_once(lambda dt: self.transition_to_screen('result'), 3)

    def transition_to_screen(self, screen_name):
        self.current = screen_name

class TitleScreen(Screen):
    pass

class GuessingScreen(Screen):
    message = StringProperty("I'm thinking of a number between 1 and 25...")
    def update_message(self, new_message):
        self.message = new_message

class RouletteScreen(Screen):
    outcome_text = StringProperty('')
    def show_outcome_text(self, text):
        self.outcome_text = text

class DoorScreen(Screen):
    feedback_text = StringProperty('Choose a door... Find the robber to survive.')
    def reveal_door(self, choice, correct_door):
        if choice == correct_door:
            self.feedback_text = f"Door {choice}... You found the robber! You live!"
        else:
            self.feedback_text = f"Door {choice}... It's a puppy! You lose!"

class ResultScreen(Screen):
    result_text = StringProperty('')
    art_text = StringProperty('')
    def show_win(self):
        self.result_text = "CONGRATULATIONS! YOU GUESSED IT!"
        self.art_text = """
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
        """
    def show_game_over(self, message="GAME OVER"):
        self.result_text = message
        self.art_text = ""

class GuessOrDieApp(App):
    def build(self):
        return GameManager()

if __name__ == '__main__':
    GuessOrDieApp().run()
