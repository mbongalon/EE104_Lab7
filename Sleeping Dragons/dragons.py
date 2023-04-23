# import the necessary modules
import math
import random

# define constants
WIDTH = 800
HEIGHT = 600
CENTER_X = WIDTH / 2
CENTER_Y = HEIGHT / 2
CENTER = (CENTER_X, CENTER_Y)
FONT_COLOR = (0, 0, 0)
EGG_TARGET = 50
HERO1_START = (200, 200)
HERO2_START = (200, 400)
ATTACK_DISTANCE = 250
DRAGON_WAKE_TIME = 2
EGG_HIDE_TIME = 2
MOVE_DISTANCE = 5

# define global variables
lives = 3
eggs_collected = 0
game_over = False
game_complete = False
reset_required1 = False
reset_required2 = False

# create a dictionary for the easy lair (dragons, eggs, timers)
easy_lair = {
    "dragon": Actor("dragon-asleep", pos=(600, 100)),
    "eggs": Actor("one-egg", pos=(400, 100)),
    "egg_count": 1,
    "egg_hidden": False,
    "egg_hide_counter": 0,
    "sleep_length": 9,
    "sleep_counter": 0,
    "wake_counter": 0
}

# create a dictionary for the medium lair (dragons, eggs, timers)
medium_lair = {
    "dragon": Actor("dragon-asleep", pos=(600, 300)),
    "eggs": Actor("two-eggs", pos=(400, 300)),
    "egg_count": 2,
    "egg_hidden": False,
    "egg_hide_counter": 0,
    "sleep_length": 6,
    "sleep_counter": 0,
    "wake_counter": 0
}

# create a dictionary for the hard lair (dragons, eggs, timers)
hard_lair = {
    "dragon": Actor("dragon-asleep", pos=(600, 500)),
    "eggs": Actor("three-eggs", pos=(400, 500)),
    "egg_count": 3,
    "egg_hidden": False,
    "egg_hide_counter": 0,
    "sleep_length": 3,
    "sleep_counter": 0,
    "wake_counter": 0
}

# bring in the lairs and heroes
lairs = [easy_lair, medium_lair, hard_lair]
hero1 = Actor("hero", pos=HERO1_START)
hero2 = Actor("hero2", pos=HERO2_START)

# draw the background, lairs, and heroes
# write different text to screen depending on whether the game is won or loss
def draw():
    global lairs, eggs_collected, lives, game_complete
    screen.clear()
    screen.blit("dungeon", (0, 0))
    if game_over:
        screen.draw.text("GAME OVER!", fontsize=60, center=CENTER, color=FONT_COLOR)
    elif game_complete:
        screen.draw.text("YOU WON!", fontsize=60, center=CENTER, color=FONT_COLOR)
    else:
        hero1.draw()
        hero2.draw()
        draw_lairs(lairs)
        draw_counters(eggs_collected, lives)

# draw the easy, medium, and hard lairs
# hide the eggs depending on timer conditions
def draw_lairs(lairs_to_draw):
    for lair in lairs_to_draw:
        lair["dragon"].draw()
        if lair["egg_hidden"] is False:
            lair["eggs"].draw()

# create an interface to show eggs collected and player lives
def draw_counters(eggs_collected, lives):
    screen.blit("egg-count", (0, HEIGHT - 30))
    screen.draw.text(str(eggs_collected), fontsize=40, pos=(30, HEIGHT - 30), color=FONT_COLOR)
    screen.blit("life-count", (60, HEIGHT - 30))
    screen.draw.text(str(lives), fontsize=40, pos=(90, HEIGHT - 30), color=FONT_COLOR)
    
# enable player movement and perform collision checks
def update():
    global reset_required1, reset_required2
    if reset_required1 is False:
        if keyboard.right:
            hero1.x += MOVE_DISTANCE
            if hero1.x > WIDTH:
                hero1.x = WIDTH
        elif keyboard.left:
            hero1.x -= MOVE_DISTANCE
            if hero1.x < 0:
                hero1.x = 0
        elif keyboard.down:
            hero1.y += MOVE_DISTANCE
            if hero1.y > HEIGHT:
                hero1.y = HEIGHT
        elif keyboard.up:
            hero1.y -= MOVE_DISTANCE
            if hero1.y < 0:
                hero1.y = 0
    if reset_required2 is False:
        if keyboard.d:
            hero2.x += MOVE_DISTANCE
            if hero2.x > WIDTH:
                hero2.x = WIDTH
        elif keyboard.a:
            hero2.x -= MOVE_DISTANCE
            if hero2.x < 0:
                hero2.x = 0
        elif keyboard.s:
            hero2.y += MOVE_DISTANCE
            if hero2.y > HEIGHT:
                hero2.y = HEIGHT
        elif keyboard.w:
            hero2.y -= MOVE_DISTANCE
            if hero2.y < 0:
                hero2.y = 0
    check_for_collisions()
    
# call helper functions to wake/sleep dragons
def update_lairs():
    global lairs, hero1, hero2, lives
    for lair in lairs:
        if lair["dragon"].image == "dragon-asleep":
            update_sleeping_dragon(lair)
        elif lair["dragon"].image == "dragon-awake":
            update_waking_dragon(lair)
        update_egg(lair)

clock.schedule_interval(update_lairs, 1)

# create timer conditions to wake up dragons
def update_sleeping_dragon(lair):
    if lair["sleep_counter"] >= lair["sleep_length"]:
        # Less Predictable Dragons
        if random.choice([True, False]):
            lair["dragon"].image = "dragon-awake"
        lair["sleep_counter"] = 0
    else:
        lair["sleep_counter"] += 1
        
# create timer conditions to put dragons asleep
def update_waking_dragon(lair):
    if lair["wake_counter"] >= DRAGON_WAKE_TIME:
        lair["dragon"].image = "dragon-asleep"
        lair["wake_counter"] = 0
    else:
        lair["wake_counter"] += 1
        
# hide the eggs upon collision
def update_egg(lair):
    if lair["egg_hidden"] is True:
        if lair["egg_hide_counter"] >= EGG_HIDE_TIME:
            lair["egg_hidden"] = False
            lair["egg_hide_counter"] = 0
        else:
            lair["egg_hide_counter"] += 1
    
# check for player collisions with eggs or dragons
def check_for_collisions():
    global lairs, eggs_collected, lives, reset_required1, reset_required2, game_complete
    for lair in lairs:
        if lair["egg_hidden"] is False:
            check_for_egg_collision(lair)
        if lair["dragon"].image == "dragon-awake" and reset_required1 is False:
            check_for_dragon_collision(lair)
        if lair["dragon"].image == "dragon-awake" and reset_required2 is False:
            check_for_dragon_collision(lair)

# perform math operations to check player distance relative to dragons
def check_for_dragon_collision(lair):
    x_distance1 = hero1.x - lair["dragon"].x
    y_distance1 = hero1.y - lair["dragon"].y
    x_distance2 = hero2.x - lair["dragon"].x
    y_distance2 = hero2.y - lair["dragon"].y
    distance1 = math.hypot(x_distance1, y_distance1)
    distance2 = math.hypot(x_distance2, y_distance2)
    if distance1 < ATTACK_DISTANCE and abs(y_distance1) < 100:
        handle_dragon_collision1()
    if distance2 < ATTACK_DISTANCE and abs(y_distance2) < 100:
        handle_dragon_collision2()

# reset Hero 1 position upon collision with dragons
def handle_dragon_collision1():
    global reset_required1
    reset_required1 = True
    animate(hero1, pos=HERO1_START, on_finished=subtract_life1)
    
# reset Hero 2 position upon collision with dragons
def handle_dragon_collision2():
    global reset_required2
    reset_required2 = True
    animate(hero2, pos=HERO2_START, on_finished=subtract_life2)

# hide eggs and increase eggs collected upon player collision
# win the game after collecting enough eggs
def check_for_egg_collision(lair):
    global eggs_collected, game_complete
    if hero1.colliderect(lair["eggs"]) or hero2.colliderect(lair["eggs"]):
        lair["egg_hidden"] = True
        eggs_collected += lair["egg_count"]
        if eggs_collected >= EGG_TARGET:
            game_complete = True

# disable Hero 1 movement upon collision with dragons
# reduce player lives by 1
def subtract_life1():
    global lives, reset_required1, game_over
    lives -= 1
    if lives == 0:
        game_over = True
    reset_required1 = False

# disable Hero 2 movement upon collision with dragons
# reduce player lives by 1
def subtract_life2():
    global lives, reset_required2, game_over
    lives -= 1
    if lives == 0:
        game_over = True
    reset_required2 = False