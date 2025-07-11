import pygame as pg
from random import randrange

#Setting Window Params
WINDOW = 1000
TILE_SIZE = 50
RANGE = (TILE_SIZE // 2, WINDOW - TILE_SIZE//2, TILE_SIZE)
screen = pg.display.set_mode([WINDOW] * 2)

#random position function
get_random_position = lambda: [randrange(*RANGE), randrange(*RANGE)]

#setting up pygame clock
clock = pg.time.Clock()

#setting up snake and food
snake = pg.rect.Rect([0,0, TILE_SIZE - 2, TILE_SIZE -2 ])
snake.center = get_random_position()
snake_dir = (0,0)
food = snake.copy()
food.center = get_random_position() 

#speed control
time, time_step = 0, 110

#score initialize
score = 0
pg.display.set_caption("Snake by Maymun Rahman     SCORE: " + str(score) )


#initial snake settings
length = 1
segments = [snake.copy()]

#music/sfx
pg.mixer.init()
pg.mixer.music.load("game_theme.mp3")
crash_sound = pg.mixer.Sound("crash.mp3")
crash_sound.set_volume(0.5)
game_start_sound = pg.mixer.Sound("game_start.mp3")
food_eat_sound = pg.mixer.Sound("food_eat.mp3")
pg.mixer.Sound.play(game_start_sound)
pg.mixer.music.play(-1)

#direction dictionary; makes sure the snake can't move into itself
dirs = {pg.K_w: 1, pg.K_s:1, pg.K_a: 1, pg.K_d: 1}

#crashing
def crash():
    pg.mixer.music.stop()
    pg.mixer.Sound.play(crash_sound)
    pg.mixer.music.stop()

    
#main game loop
while True:
    pg.display.set_caption("Snake by Maymun Rahman     SCORE: " + str(score) )
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_w and dirs[pg.K_w]:
                snake_dir = (0, -TILE_SIZE)
                dirs = {pg.K_w: 1, pg.K_s:0, pg.K_a: 1, pg.K_d: 1}
            if event.key == pg.K_s and dirs[pg.K_s] :
                snake_dir = (0, TILE_SIZE)
                dirs = {pg.K_w: 0, pg.K_s:1, pg.K_a: 1, pg.K_d: 1}
            if event.key == pg.K_a and dirs[pg.K_a]:
                snake_dir = (-TILE_SIZE,0)
                dirs = {pg.K_w: 1, pg.K_s:1, pg.K_a: 1, pg.K_d: 0}
            if event.key == pg.K_d and dirs[pg.K_d]:
                snake_dir = (TILE_SIZE, 0)
                dirs = {pg.K_w: 1, pg.K_s:1, pg.K_a: 0, pg.K_d: 1}
    screen.fill('black')
    #check boundaries and self eating
    self_eating = pg.Rect.collidelist(snake, segments[:-1]) != -1
    if snake.left < 0 or snake.right > WINDOW or snake.top < 0 or snake.bottom > WINDOW or self_eating:
        crash()
        score = 0
        pg.time.wait(1000)
        pg.mixer.Sound.play(game_start_sound)
        pg.time.wait(500)
        pg.mixer.music.play(-1) 
       
        snake.center, food.center = get_random_position(), get_random_position()
        length, snake_dir = 1, (0,0)
        segments = [snake.copy()]
        

    #check food
    if snake.center == food.center:
        pg.mixer.Sound.play(food_eat_sound)
        food.center = get_random_position()
        length +=1
        score += 1

    #draw snake
    [pg.draw.rect(screen, 'green', segment) for segment in segments]
    #draw food
    pg.draw.rect(screen, 'red', food)
    #move snake
    time_now = pg.time.get_ticks()
    if time_now -   time > time_step:
        time = time_now
        snake.move_ip(snake_dir)
        segments.append(snake.copy())
        segments = segments[-length:]
    pg.display.flip()
    clock.tick(60)
