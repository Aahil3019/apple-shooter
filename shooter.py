import os
from random import randint
from time import clock
from keyboard import key

apple = Actor("apple")
lemon = Actor("lemon")

current_actor = apple  # Start with apple
score = 0
game_over = False
time_left = 60  # 60 seconds countdown
top_scores = [0, 0, 0]  # List to hold top 3 scores
new_high_score = False  # Flag for congratulation message
new_rank = 0  # To track the player's rank in the top 3
SCORE_FILE = "scores.txt"  # File to save/load top scores

def start_game():
    global time_left, new_high_score, new_rank
    load_top_scores()  # Load scores from file when the game starts
    time_left = 60  # Reset the time
    new_high_score = False  # Reset congratulation message flag
    new_rank = 0  # Reset rank
    place_actor()
    clock.schedule_interval(update_timer, 1)  # Update timer every second
    clock.schedule_unique(end_game, 60)  # End game after 60 seconds

def place_actor():
    current_actor.x = randint(10, 800)
    current_actor.y = randint(10, 600)

def increase_score():
    global score
    score += 1

def switch_actor():
    global current_actor
    if current_actor == apple:
        current_actor = lemon
    else:
        current_actor = apple

def on_mouse_down(pos):
    if game_over:
        return
    if current_actor.collidepoint(pos):
        print("Good shot!<3")
        place_actor()
        increase_score()
        switch_actor()
    else:
        print("You Missed!HEHE")
        end_game()  # End the game when player misses

def draw():
    screen.clear()
    if game_over:
        if new_high_score:
            screen.draw.text(f"Congratulations! You are ranked #{new_rank}!", center=(400, 200), fontsize=60, color="yellow")
        screen.draw.text(f"Final Score: {score}", (400, 300), color="red")
        screen.draw.text("Top Scores:", (350, 350), color="white")
        for i, top_score in enumerate(top_scores):
            screen.draw.text(f"{i+1}: {top_score}", (400, 380 + i * 20), color="white")
        screen.draw.text("Press R to Replay or Q to Quit", (350, 450), color="white")
    else:
        screen.draw.text(f"Score: {score}", (10, 10), color="white")
        current_actor.draw()

        # Draw translucent countdown in background (centered)
        screen.draw.text(
            f"Time Left: {time_left}s", 
            center=(400, 50), 
            fontsize=60, 
            color=(255, 255, 255, 128)  # Translucent white
        )

def end_game():
    global game_over
    game_over = True
    update_top_scores()
    save_top_scores()  # Save scores to file after the game ends

def update_top_scores():
    global new_high_score, new_rank
    # Add current score and sort the top scores in descending order
    top_scores.append(score)
    top_scores.sort(reverse=True)
    
    # Keep only the top 3 scores
    if len(top_scores) > 3:
        top_scores.pop()

    # Check if the score is in the top 3 and update the rank
    for i in range(3):
        if score == top_scores[i]:
            new_high_score = True
            new_rank = i + 1  # Rank is 1-based

def on_key_down(key):
    if game_over:
        if key == keys.R:  # Replay
            reset_game()
        elif key == keys.Q:  # Quit
            quit()

def reset_game():
    global score, game_over
    score = 0
    game_over = False
    start_game()  # Restart the game

def update_timer():
    global time_left
    if time_left > 0:
        time_left -= 1
    else:
        clock.unschedule(update_timer)  # Stop updating timer when time runs out
        end_game()  # End the game when timer reaches 0

def save_top_scores():
    """Save the top 3 scores to a file."""
    with open(SCORE_FILE, 'w') as f:
        for score in top_scores:
            f.write(f"{score}\n")

def load_top_scores():
    """Load the top 3 scores from the file."""
    global top_scores
    if os.path.exists(SCORE_FILE):
        with open(SCORE_FILE, 'r') as f:
            top_scores = [int(line.strip()) for line in f.readlines()]
            top_scores.sort(reverse=True)
    else:
        top_scores = [0, 0, 0]  # If no file exists, initialize with default

start_game()  # Begin the game
