# Format Code Later: black.now.sh

from GameEngine import Engine as Game  # lol doesn't do anything
from GameEngine import Screen
import sys, time, os, random

screenSize = (850, 800)

screen = Screen(screenSize, (100, 100), "Snake Game")

# Screen can do
# screen.fillbg((R,G,B))
# screen.drawrect((X1,Y1),(X2,Y2),(R,G,B))
# screen.drawline((X1,Y1),(X2,Y2),(R,G,B))
# screen.write(TEXT,(X,Y),(R,G,B),(FONTNAME,FONTSIZE,BOLD,ITALIC,UNDERLINE))
# screen.bindkey(KEY,FUNCTION)
## screen.unbindkey(BINDID) BINDID is returned by the bind function.

# Eventloop Processing Snake Draw Code and Win Detection Design:
# https://stackoverflow.com/questions/459083/how-do-you-run-your-own-code-alongside-tkinters-event-loop


class Apple:
    def __init__(self):
        self.pos = [random.randint(0, 24), random.randint(0, 24)]

    def regenerate(self):
        self.pos = [random.randint(0, 24), random.randint(0, 24)]
        random.seed(random.randint(1,1000)%100)

    def setPos(self, x, y):
        self.pos = [x, y]

    def position(self):
        return self.pos


class Snake:
    def __init__(self, screen):  # Board is 25x25 in size
        self.screen = screen
        self.headpos = [12, 12]
        self.bodypos = [[12, 12], [11, 12], [10, 12], [9, 12], [8, 12]]
        self.length = len(self.bodypos)
        self.direction = [1,0]  # [xMove,yMove] ([1,0] = right, [-1,0] = left, [0,1] = up, [0,-1] = down)
        self.apple = Apple()
        self.expand = 0
        self.apple.setPos(16, 12)  # So it always spawns in a valid location
        self.bugfixed = False # Fix a render bug that idk how to fix otherwise

    def newApple(self):
        self.apple.regenerate()
        while self.apple.position() in self.bodypos:
            self.apple.regenerate()

    def changeDirection(self, d):
        self.direction = d

    def nextStep(self):
        self.headpos = [
            self.headpos[0] + self.direction[0],
            self.headpos[1] + self.direction[1],
        ]
        if self.headpos == self.apple.position(): # Check if the snake ate the Apple
            self.newApple()
            self.bodypos = [self.headpos[:]] + self.bodypos[:]
            self.expand += 1
        else:
            self.bodypos = [self.headpos[:]] + self.bodypos[:-1]
        self.length = len(self.bodypos)

    def validpos(self):
        if self.headpos in self.bodypos[1:]:
            return False
        elif not 0 <= self.headpos[0] < 25 or not 0 <= self.headpos[1] < 25:
            return False
        else:
            return True

    def draw(self):
        snakebodysize = 25
        # Small bugfix that is applied at the start of the program
        if not self.bugfixed:
            self.screen.drawrect(
                ((snakebodysize * (9)), (snakebodysize * (13))),
                ((snakebodysize * (10)), (snakebodysize * (14))),
                BLACK,
            )
            self.bugfixed = not self.bugfixed
        # Remove the last piece of the snake body if it isn't expanding
        if not self.expand:
            pos = self.bodypos[-1]
            self.screen.drawrect(
                ((snakebodysize * (pos[0] + 1)), (snakebodysize * (pos[1] + 1))),
                ((snakebodysize * (pos[0] + 2)), (snakebodysize * (pos[1] + 2))),
                BLACK,
            )
        else:
            self.expand += -1
        # Change the color of the body that *was* the head
        pos = self.bodypos[1]
        self.screen.drawrect(
            ((snakebodysize * (pos[0] + 1)), (snakebodysize * (pos[1] + 1))),
            ((snakebodysize * (pos[0] + 2)), (snakebodysize * (pos[1] + 2))),
            GREEN,
        )
        # Draw the Head using a different color
        pos = self.headpos
        self.screen.drawrect(
            ((snakebodysize * (pos[0] + 1)), (snakebodysize * (pos[1] + 1))),
            ((snakebodysize * (pos[0] + 2)), (snakebodysize * (pos[1] + 2))),
            BLUE,
        )
        # Draw the Apple
        pos = self.apple.position()
        self.screen.drawrect(
            ((snakebodysize * (pos[0] + 1)), (snakebodysize * (pos[1] + 1))),
            ((snakebodysize * (pos[0] + 2)), (snakebodysize * (pos[1] + 2))),
            RED,
        )
        self.screen.drawline([snakebodysize,snakebodysize],[snakebodysize*26,snakebodysize],RED)
        self.screen.drawline([snakebodysize,snakebodysize],[snakebodysize,snakebodysize*26],RED)
        self.screen.drawline([snakebodysize*26,snakebodysize],[snakebodysize*26,snakebodysize*26],RED)
        self.screen.drawline([snakebodysize,snakebodysize*26],[snakebodysize*26,snakebodysize*26],RED)

    def drawAll(self):
        snakebodysize = 25
        # Draw the snake body
        for pos in self.bodypos:
            self.screen.drawrect(
                ((snakebodysize * (pos[0] + 1)), (snakebodysize * (pos[1] + 1))),
                ((snakebodysize * (pos[0] + 2)), (snakebodysize * (pos[1] + 2))),
                GREEN,
            )
        # Draw the Head using a different color
        pos = self.headpos
        self.screen.drawrect(
            ((snakebodysize * (pos[0] + 1)), (snakebodysize * (pos[1] + 1))),
            ((snakebodysize * (pos[0] + 2)), (snakebodysize * (pos[1] + 2))),
            BLUE,
        )
        # Draw the Apple # Need to move to front before the snake
        pos = self.apple.position()
        self.screen.drawrect(
            ((snakebodysize * (pos[0] + 1)), (snakebodysize * (pos[1] + 1))),
            ((snakebodysize * (pos[0] + 2)), (snakebodysize * (pos[1] + 2))),
            RED,
        )
        # Draw the outside borders
        self.screen.drawline([snakebodysize,snakebodysize],[snakebodysize*26,snakebodysize],RED)
        self.screen.drawline([snakebodysize,snakebodysize],[snakebodysize,snakebodysize*26],RED)
        self.screen.drawline([snakebodysize*26,snakebodysize],[snakebodysize*26,snakebodysize*26],RED)
        self.screen.drawline([snakebodysize,snakebodysize*26],[snakebodysize*26,snakebodysize*26],RED)


def gameOver(screen, win=False):
    screen.fillbg(BLACK)
    snake.drawAll()
    screen.drawrect((225, 115), (625, 185), GRAY)
    screen.write("Game Over!", (425, 150), RED, ("Consolas", 50, True, False, False))
    if win:
        screen.write(
            "You Win!", (425, 450), WHITE, ("Consolas", 50, True, False, False)
        )
    else:
        screen.write(
            "You Lose!", (425, 450), WHITE, ("Consolas", 50, True, False, False)
        )


def startGame():
    screen.drawrect((325, 115), (525, 185), BLACK)
    snakeTick()
    
def snakeTick():
    if snake.validpos():
        if snake.length != 25:
            snake.nextStep()
            snake.draw()
            snake.screen.root.after(
                tickSpeed, snakeTick
            )  # Reschedules Event to run in tickSpeed seconds
        else:
            gameOver(snake.screen,True)
    else:
        gameOver(snake.screen)

def up(event):  # Just so I can properly bind there keys
    if snake.direction != [0,1]:
        snake.changeDirection([0, -1])


def down(event):
    if snake.direction != [0,-1]:
        snake.changeDirection([0, 1])


def right(event):
    if snake.direction != [-1,0]:
        snake.changeDirection([1, 0])


def left(event):
    if snake.direction != [1,0]:
        snake.changeDirection([-1, 0])


# Constants
BLACK = (0, 0, 0)
GRAY = (127, 127, 127)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
DARK_RED = (125, 100, 100)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

tickSpeed = 200

# Start Menu Drawing Code
screen.fillbg(BLACK)
screen.drawrect((325, 115), (525, 185), GRAY)
screen.write("Snake", (425, 150), RED, ("Consolas", 50, True, False, False))

snake = Snake(screen)
snake.drawAll()

screen.bindkey("<Up>", up)
screen.bindkey("<Down>", down)
screen.bindkey("<Right>", right)
screen.bindkey("<Left>", left)

# screen.drawline((100,100),(250,150),GREEN,10)

# def enter():
#    screen.fillbg(BLACK)
#    screen.write("you pressed enter",(400,300),RED,("Consolas",15,True,False,False))
# enterKeybindId = screen.bindkey("<Return>",lambda x: enter())
screen.root.after(1000, startGame)
screen.mainloop()
