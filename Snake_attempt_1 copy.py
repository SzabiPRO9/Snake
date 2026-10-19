import tkinter #for the graphic
import random

ROWS = 25
COLS = 25
TILE_SIZE = 25

WINDOW_WIDTH = TILE_SIZE * COLS
WINDOW_HEIGHT = TILE_SIZE * ROWS

class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y

#game window
window = tkinter.Tk()
window.title("Snake")
window.resizable(False, False)

canvas = tkinter.Canvas(window, bg = "white", width = WINDOW_WIDTH, height = WINDOW_HEIGHT, borderwidth = 0, highlightthickness = 0)
canvas.pack()
window.update()

#center the location of the window (it's appearence)
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

window_x = int((screen_width/2)-(window_width/2))
window_y = int ((screen_height/2)-(window_height/2))
# format "(w)x(h)+(x)+(y)"
window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

# initialize the game
snake = Tile(5*TILE_SIZE, 5*TILE_SIZE) # single tile or snake's head
food = Tile(10*TILE_SIZE, 10*TILE_SIZE)
bomb = Tile(15*TILE_SIZE, 15*TILE_SIZE)
snake_body = [] # multiple snake tiles
velocityX = 0
velocityY = 0
game_over = False
score = 0
h_score = 0

def restart_game():
    global snake, food, bomb, snake_body, velocityX, velocityY, game_over, score
    snake = Tile(5*TILE_SIZE, 5*TILE_SIZE)
    food = Tile(10*TILE_SIZE, 10*TILE_SIZE)
    bomb = Tile(15*TILE_SIZE, 15*TILE_SIZE)
    snake_body = []
    velocityX = 0
    velocityY = 0
    game_over = False
    score = 0
    button.place_forget()

button = tkinter.Button(canvas, text = "Restart", command = restart_game)

def change_direction(e): # e = event
    # print(e) - it shows the code of the keys, we need only the function
    # print(e.keysym) - it just shows the function
    global velocityX, velocityY, game_over
    if (game_over):
        return

    if (e.keysym == "Up" and velocityY != 1):
        velocityX = 0
        velocityY = -1
    elif (e.keysym == "Down" and velocityY != -1):
        velocityX = 0
        velocityY = 1
    elif (e.keysym == "Left" and velocityX != 1):
        velocityX = -1
        velocityY = 0
    elif (e.keysym == "Right" and velocityX != -1):
        velocityX = 1
        velocityY = 0
    # elif (e.keysym == "Space" and game_over == True):
    

def move():
    global snake, food, bomb, snake_body, game_over, score
    if (game_over):
        return

    if (snake.x < 0 or snake.x >=  WINDOW_WIDTH or snake.y < 0 or snake.y >= WINDOW_HEIGHT):
        game_over = True
        return
    
    for tile in snake_body:
        if (snake.x == tile.x and snake.y == tile.y):
            game_over = True
            return

    # collision
    if (snake.x == food.x and snake.y == food.y):
        snake_body.append(Tile(food.x, food.y))
        food.x = random.randint(0, COLS-1) * TILE_SIZE
        food.y = random.randint(0, ROWS-1) * TILE_SIZE
        score += 1    
    elif (snake.x == bomb.x and snake.y == bomb.y):
        if (len(snake_body) > 0):
            snake_body.pop()
            bomb.x = random.randint(0, COLS-1) * TILE_SIZE
            bomb.y = random.randint(0, ROWS-1) * TILE_SIZE
            score -= 1
        else:
            game_over = True
            return

    # update snake's body, its movement
    for i in range(len(snake_body)-1, -1, -1):
        tile = snake_body[i]
        if (i == 0):
            tile.x = snake.x
            tile.y = snake.y
        else:
            prev_tile = snake_body[i-1]
            tile.x = prev_tile.x
            tile.y = prev_tile.y

    snake.x += velocityX * TILE_SIZE
    snake.y += velocityY * TILE_SIZE

def move_bomb():
    n = random.randint(1, 50) 
    if (n == 1):
        bomb.x = random.randint(0, COLS-1) * TILE_SIZE
        bomb.y = random.randint(0, ROWS-1) * TILE_SIZE 

def high_score():
    global h_score
    if (game_over == True):
        if (h_score <= score):
            h_score = score


def draw():
    global snake, food, bomb, snake_body, game_over, score
    move()
    if (game_over == False):
        move_bomb()
    high_score()

    canvas.delete("all")

    # draw food
    canvas.create_rectangle(food.x, food.y, food.x + TILE_SIZE, food.y + TILE_SIZE, fill = "red")

    # draw bomb
    canvas.create_rectangle(bomb.x, bomb.y, bomb.x + TILE_SIZE, bomb.y + TILE_SIZE, fill = "black")

    # draw snake
    canvas.create_rectangle(snake.x, snake.y, snake.x + TILE_SIZE, snake.y + TILE_SIZE, fill = "green")

    for tile in snake_body:
        canvas.create_rectangle(tile.x, tile.y, tile.x + TILE_SIZE, tile.y + TILE_SIZE, fill = "green")

    if (game_over):
        canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, font = "Arial 20", text = f"Game over: {score}", fill = "black")
        canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2+30, font = "Arial 20", text = f"High score: {h_score}", fill = "black")
        button.place(relx = 0.5, rely = 0.5, y = 70, anchor = "center")
    else:
        button.place_forget()
        canvas.create_text(30, 20, font = "Arial 12", text = f"Score: {score}", fill = "black")
        canvas.create_text(50, 40, font = "Arial 12", text = f"High score: {h_score}", fill = "black")
        

    window.after(100, draw)

draw()

window.bind("<KeyRelease>", change_direction)
window.mainloop()
