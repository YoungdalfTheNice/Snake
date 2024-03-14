from tkinter import *
import random
import logging

logging.basicConfig(level='DEBUG', format='%(levelname)s - %(message)s')

GAME_WIDTH  = 1200
GAME_HEIGHT = 700
SPEED = 100
SPACE_SIZE = 50
SNAKE_COLOR = "#00FF00"

BG_COLOR    = "#000000"

UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4


def new_game():
    
    global end_screen

    if end_screen:
        logging.info("Neues Spiel gestartet!")
        end_screen = FALSE

        canvas.delete(ALL)

        snake = Snake()
        food = Food(canvas)
        
        window.bind('<w>', lambda event: change_direction(snake, UP))
        window.bind('<a>', lambda event: change_direction(snake, LEFT))
        window.bind('<s>', lambda event: change_direction(snake, DOWN))
        window.bind('<d>', lambda event: change_direction(snake, RIGHT))
        next_turn(snake, food)


# Wo erscheint die Schlange? - oben links
# Wie groß ist die Schlange? - 3x Space size
# In welche Richtung bewegt sich die Schlange? - down
# Welche Farbe hat die Schlange?
# Welche Farbe hat der Apfel?

class Snake:
    
    def __init__(self):
        self.coordinates = [(0,0),(0,0),(0,0)]
        self.squares = []
        self.direction = DOWN
        for x, y in self.coordinates:
            square = canvas.create_rectangle(x,y,x + SPACE_SIZE, y + SPACE_SIZE, fill = SNAKE_COLOR, tag = "snake")
            self.squares.append(square)


class Food:
    FOOD_COLOR = "#FF0000"
    def __init__(self,canvas):
        
        x = random.randint(0,(GAME_WIDTH/SPACE_SIZE)-1)*SPACE_SIZE
        y = random.randint(0,(GAME_HEIGHT/SPACE_SIZE)-1)*SPACE_SIZE
        self.coordinates = (x,y)
        self.draw(canvas)

    
    def draw(self,canvas):
        x = self.coordinates[0]
        y = self.coordinates[1]
        canvas.create_oval(x,y,x + SPACE_SIZE, y + SPACE_SIZE, fill = Food.FOOD_COLOR, tag = "food")


def change_direction(snake, new_direction):
    
    if new_direction == LEFT:
        if snake.direction != RIGHT:
            snake.direction = new_direction
    
    elif new_direction == RIGHT:
        if snake.direction != LEFT:
            snake.direction = new_direction
            
    elif new_direction == DOWN:
        if snake.direction != UP:
            snake.direction = new_direction
            
    elif new_direction == UP:
        if snake.direction != DOWN:
            snake.direction = new_direction
    
def game_over():
    global end_screen
    end_screen = TRUE
    canvas.delete(ALL)

    def blink_game_over():
        canvas.itemconfig(game_over_text, state="hidden" if canvas.itemcget(game_over_text, "state") == "normal" else "normal")
        canvas.after(300, blink_game_over)
    
    game_over_text = canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2 - 100, text="GAME OVER", fill="red", font=("terminal", 90), tag="gameover")
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2 + 50, text="Leertaste drücken für neues Spiel.", fill="red", font=("terminal", 30), tag="gameover")

    blink_game_over()


# Restlicher Code bleibt unverändert


def check_collision(snake):
     
    x,y = snake.coordinates[0] # Kopf
    if x < 0 or y < 0 or x >= GAME_WIDTH or y >= GAME_HEIGHT:
        return True
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return TRUE
    return FALSE
  
def next_turn(snake, food):
    
    # Koordinaten des Kopfes der Schlange
    x,y = snake.coordinates[0]
    

    if snake.direction == DOWN:
        y += SPACE_SIZE
    if snake.direction == UP:
        y -= SPACE_SIZE
    if snake.direction == RIGHT:
        x += SPACE_SIZE
    if snake.direction == LEFT:
        x -= SPACE_SIZE
       
    
    snake.coordinates.insert(0,(x,y))
    square = canvas.create_rectangle(x,y,x + SPACE_SIZE, y + SPACE_SIZE, fill = SNAKE_COLOR, tag = "snake")
    snake.squares.insert(0, square)


    if x == food.coordinates[0] and y == food.coordinates[1]:
        score = len(snake.coordinates) - 3
        label.config(text="Score:{}".format(score), font=('terminal', 40))
        canvas.delete("food")
        food = Food(canvas)

    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collision(snake):
        game_over()
    else:
        window.after(SPEED,next_turn,snake, food)



window = Tk()
window.title("Snake Game")
window.resizable(False, False)

end_screen = True

label = Label(window, text="Score:{}".format(0), font=('terminal', 40))
label.pack()

canvas = Canvas(window, bg=BG_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.bind('<space>', lambda event: new_game())    

window.mainloop()