import utime
import picoexplorer as display
from constants import *
from actor import Actor
from enemies import Enemies
from shot import Shot
from player import Player

# positions relative to pos where crash would be hit
spacecraft_hit_pos = [
    (-15,5),
    (-10,0),
    (-5,-5),
    (-3,-10),
    (0,-15),
    (-3,-10),
    (-5,-5),
    (10,0),
    (15,5)
    ]

SKY_COLOR = (0, 0, 0)
TEXT_COLOR = (255,255,255)

width = display.get_width()
height = display.get_height()

display_buffer = bytearray(width * height * 2)  # 2-bytes per pixel (RGB565)
display.init(display_buffer)

spaceship = Actor(display, "spacecraftimg.spr", (120, 200))

enemies = Enemies(display)

# List to track shots
shots = []
# Prevent continuous shots
shot_last_time = utime.time()
# min time between shots
shot_delay = 2

player1 = Player(display)

game_status = GAME_READY


# similar to pgzero draw
def draw():
    display.set_pen(*SKY_COLOR)
    display.clear()
    # Display game  over message
    if (game_status == GAME_READY):
        display.set_pen(*TEXT_COLOR)
        display.text("Space Game", 40, 90, 220, 3)
        display.text("Click to start", 50, 160, 220, 2)
    elif (game_status == GAME_OVER):
        display.set_pen(*TEXT_COLOR)
        display.text("Game Over", 45, 90, 220, 3)
        display.text("Score "+str(player1.score), 75, 160, 220, 2)
    elif (game_status == GAME_PLAY):
        spaceship.draw(display_buffer)
        enemies.draw(display_buffer)
        for this_shot in shots:
            this_shot.draw(display_buffer)
        # Display score and number of lives
        display.set_pen(*TEXT_COLOR)
        display.text(str(player1.score), 10, 10, 120, 1)
        display.text(player1.get_score_string(), 200, 10, 40, 1)
        
    # Update display for any state
    display.update()
    
# similar to pgzero update
def update():
    global game_status, shot_last_time, timer
    
    if (game_status == GAME_READY):
        # wait for button press then start game  
        if (display.is_pressed(display.BUTTON_A) or display.is_pressed(display.BUTTON_B) or display.is_pressed(display.BUTTON_X) or display.is_pressed(display.BUTTON_Y)) :
            game_status = GAME_PLAY
            player1.reset()
    elif game_status == GAME_OVER:
        if ((utime.time() > timer + 4) and (display.is_pressed(display.BUTTON_A) or display.is_pressed(display.BUTTON_B) or display.is_pressed(display.BUTTON_X) or display.is_pressed(display.BUTTON_Y))) :
            game_status = GAME_PLAY
            player1.reset()
    elif (game_status == GAME_PLAY):
        enemies.update()
        # check for end of level
        if (enemies.check_crash((spaceship.x,spaceship.y), spacecraft_hit_pos)):
            timer = utime.time()
            player1.lives -= 1
            if (player1.lives <= 0):
                game_status = GAME_OVER
        if (display.is_pressed(display.BUTTON_Y)) :
            spaceship.x += 2
        if (display.is_pressed(display.BUTTON_B)) :
            spaceship.x -= 2
        if (display.is_pressed(display.BUTTON_A) or display.is_pressed(display.BUTTON_X)) :
            if ((shot_last_time + shot_delay) < utime.time()): 
                shots.append(Shot(display,(spaceship.x,spaceship.y-25)))
                shot_last_time = utime.time()        
        # Update existing shots
        for this_shot in shots:
            # Update position of shot
            this_shot.update()
            if this_shot.y <= 0:
                shots.remove(this_shot)
            # Check if hit asteroid or enemy
            elif enemies.check_shot(this_shot.x, this_shot.y):
                player1.score += 10
                # remove shot (otherwise it continues to hit others)
                shots.remove(this_shot)    

# This is based on a binary image file (RGB565) with the same dimensions as the screen
# updates the global display_buffer directly
def blit_image_file (filename):
    global display_buffer
    with open (filename, "rb") as file:
        position = 0
        while position < (width * height * 2):
            current_byte = file.read(1)
            # if eof
            if len(current_byte) == 0:
                break
            # copy to buffer
            display_buffer[position] = ord(current_byte)
            position += 1
    file.close()
    

# Do nothing - but continue to display the image
while True:
    draw()
    update()

