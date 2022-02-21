# code by youtuber: Engineer Man and modified to work in pycharm as well as commented
# I also added in the scoring at the end... :)
# Need to modify speed in y direction/line spacing in y direction and also
# need to change size of window
# want to add a border but how with screen refresh?

# to run type "main.py" in terminal (not console) below.
# ensure that emulate terminal in console is turned on in run configuration

import random
import curses  # imports library of windows keyboard input stuff
import time


def snake_game():
    game_speed = 100
    s = curses.initscr()  # initialize the screen using curses
    curses.curs_set(0)  # set cursor to 0 so it doesnt show up on the screen
    sh, sw = s.getmaxyx()  # set width and height of the frame
    w = curses.newwin(sh, sw, 0, 0)  # make a window based on the width and height starting at top left of the screen
    w.keypad(1)  # set so it accepts keypad input
    w.timeout(game_speed)  # refresh the screen every 100 ms. OVERALL SPEED

    # creating the snakes initial position
    snk_x = int(sw/4)
    snk_y = int(sh/2)

    # creating initial snake body parts
    snake = [
        [snk_y, snk_x],
        [snk_y, int(snk_x-2)],
        [snk_y, int(snk_x-4)],
        [snk_y, int(snk_x-6)],
        [snk_y, int(snk_x-8)]
    ]

    # creating food
    food = [int(sh/2), int(sw/2)+1]  # starting place of the food
    w.addch(food[0], food[1], curses.ACS_DIAMOND)  # adding the food to the screen in the shape of ACS diamond

    # initial snake direction
    key = curses.KEY_RIGHT

    score = 0  # define a variable to count the amount of food eaten

    # Infinite Loop for snake
    while True:

        next_key = w.getch()  # see what the next key is
        key = key if next_key == -1 else next_key  # gives no value or next key value

        # checks to see losing conditions. (hiting edges or itself)
        if snake[0][0] in [0, sh] or snake[0][1] in [0, sw-1] or snake[0] in snake[1:]:
            curses.endwin()
            print("\nGAME OVER...\nYOUR SCORE IS: " + str(score * 100))
            n = input("Play Again? (y/n): ")
            while n in "Yy":
                snake_game()
            print("Good Bye!")
            quit()

        # determine what new head of the snake will be when it eats food
        new_head = [snake[0][0], snake[0][1]]  # Start by taking the old head of the snake

        # determine which key is being pressed and add the head in that direction
        if key == curses.KEY_DOWN:
            new_head[0] += 1
            time.sleep(0.04)  # to adjust for y direction speed
        if key == curses.KEY_UP:
            new_head[0] -= 1
            time.sleep(0.04)  # to adjust for y direction speed
        if key == curses.KEY_LEFT:
            new_head[1] -= 2  # skip every other x space to make the game a more uniform grid
        if key == curses.KEY_RIGHT:
            new_head[1] += 2  # skip every other x space to make the game a more uniform grid
        # insert new head of snake
        snake.insert(0, new_head)

        # if snake gets food need to generate new food
        if snake[0] == food:
            score = score + 1  # if a piece of food is eaten score increases by 1
            food = None

            while food is None:

                nf = [random.randint(1, sh - 1),
                      random.randrange(2, sw - 1, 2)   # generate at a random integer location
                     ]
                food = nf if nf not in snake else None  # if the food is generated in the body of the snake redo food generation
                w.addch(food[0], food[1], curses.ACS_DIAMOND)
        else:
            tail = snake.pop()  # add head of snake to show motion and remove tail. snake is acs DIAMOND character
            w.addch(tail[0], tail[1], ' ')

        w.addch(snake[0][0], snake[0][1], curses.ACS_DIAMOND)




        # Increase game speed if a certain score is reached (feature currently not included -> remove comment to use feature)
    '''    if score > 5:
            w.timeout(game_speed - 25)
            if score > 10:
                w.timeout(game_speed - 50)
                if score > 15:
                    w.timeout(game_speed)
    '''  # open code with + on left of this line


snake_game()
