import pygame
import sys
import random
pygame.init()

WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0,0,0)
RED=(255,0,0)
BLA=(50,50,50)
RECT_WIDTH, RECT_HEIGHT = 50, 50
RECT_SPEED = 5
rows, cols = (12, 16) #for it be square use same ratio as rows
head='u'
appleEaten=False
if not (WIDTH/cols+HEIGHT/rows).is_integer():
    raise ValueError("screen dims not dividing right to nums of rows/cols")

class Cell:
    def __init__(self,type,snakeNode,dir):
        self.type=type
        self.snakeNode=snakeNode
        self.dir=dir
        
    def __str__(self):
        return f"{self.type}"
#build the grid

    
grid=[]
for r in range(rows):
    row=[]
    for c in range(cols):
       cell = Cell('b',-1,'u')
       row.append(cell)
    grid.append(row)

grid[5][5].type = 's'
grid[5][5].dir = 'u'
grid[5][5].snakeNode=0
grid[5][4].type = 's'
grid[5][4].snakeNode=1
grid[5][3].snakeNode=2
grid[5][3].type = 's'

grid[6][6].type='a'

def printGrid(grid):
    print("="*20)
    for r in range(rows):
        for c in range(cols):
            print(grid[r][c].snakeNode," ",end="")
        print()
        
#printGrid(grid)
def findHead(grid):
    for r in range(rows):
        for c in range(cols):
            
            if(grid[r][c].snakeNode==0) :
                return r,c
def findTail(grid):
   max =-1
   tr = 1
   tc =1
  
   for r in range(rows):
        for c in range(cols):
            if(grid[r][c].snakeNode>max) :
                max = grid[r][c].snakeNode
                tr =r
                tc = c

   return tr,tc
                

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("game")




    while True:
        handle_events()


        
        update_grid(grid)
        draw(screen,grid)




def getEmpty(grid):
    empty=[]
    for r in range(rows):
        for l in range(cols):
            if(grid[r][l].type=='b'):
                empty.append((r,l))
    return empty
def genApple(grid):
    empty = getEmpty(grid)
    r,l=random.choice(empty)
    grid[r][l].type='a'
    global appleEaten
    appleEaten=False


def ateApple(grid):
    print("ate apple")
    global appleEaten
    appleEaten=True
   
        

def gameOver():
    print("game over you died!")

def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

def update_grid(grid):
    global head
    keys = pygame.key.get_pressed()
    headRow,headCol=findHead(grid)
    tailRow,tailCol=findTail(grid)
    updateSnake(grid)
    if keys[pygame.K_LEFT] and head!='r':
       head='l'
       left(grid,headRow,headCol) 
        
    elif keys[pygame.K_RIGHT] and head!='l':
       head='r'
       right(grid,headRow,headCol) 
        
        
    elif keys[pygame.K_UP] and head!='d':
       up(grid,headRow,headCol) 
       head='u'

    elif keys[pygame.K_DOWN] and head!='u':
       down(grid,headRow,headCol) 
       head='d'

    else:
        if(head=='l'):
            left(grid,headRow,headCol) 
        if(head=='r'):
            right(grid,headRow,headCol) 
        if(head=='u'):
            up(grid,headRow,headCol)
        if(head=='d'):
            down(grid,headRow,headCol)
    
    global appleEaten
    print(appleEaten)
    if(appleEaten):
         genApple(grid)
    else:
        grid[tailRow][tailCol].snakeNode=-1
        grid[tailRow][tailCol].type='b'



def updateSnake(grid):
    tailRow,tailCol=findTail(grid)
    
    for r in range(rows):
        for c in range(cols):
            if(grid[r][c].type=='s'):
                grid[r][c].snakeNode+=1

   

def up(grid,headRow,headCol):
    if(headRow==0 or(grid[headRow-1][headCol].type=='s')):
        gameOver()
        return
    if(grid[headRow-1][headCol].type=='a'):
        ateApple(grid)
    grid[headRow-1][headCol].type='s'
    grid[headRow-1][headCol].snakeNode=0
        


def down(grid,headRow,headCol):
    if(headRow==rows-1 or(grid[headRow+1][headCol].type=='s')) :
        gameOver()
        return
    if(grid[headRow+1][headCol].type=='a'):
        ateApple(grid)
    grid[headRow+1][headCol].type='s'
    grid[headRow+1][headCol].snakeNode=0
   
def right(grid,headRow,headCol):
    if(headCol==cols-1 or(grid[headRow][headCol+1].type=='s')):
        gameOver()
        return
    if(grid[headRow][headCol+1].type=='a'):
        ateApple(grid)
    grid[headRow][headCol+1].type='s'
    grid[headRow][headCol+1].snakeNode=0


def left(grid,headRow,headCol):
    if(headCol==0 or(grid[headRow][headCol-1].type=='s')):
        gameOver()
        return
    if(grid[headRow][headCol-1].type=='a'):
        ateApple(grid)
    grid[headRow][headCol-1].type='s'
    grid[headRow][headCol-1].snakeNode=0





def draw(screen, grid):
    
    screen.fill(BLACK)  
   # pygame.draw.rect(screen, BLUE, (rect_x, rect_y, RECT_WIDTH, RECT_HEIGHT))  # Draw rectangle
    for r in range(rows):
        for c in range(cols):
            cell = grid[r][c]
            color =BLA
            if(cell.type=='b'): color  =BLACK
            if(cell.type=='s') : color =BLUE
            if(cell.type=='a') : color =RED 

            pygame.draw.rect(screen,color,(c*(WIDTH//cols),r*(HEIGHT//rows),RECT_WIDTH,RECT_HEIGHT))

    drawLines(screen)
    pygame.display.flip() 
    pygame.time.Clock().tick(7)  


def drawLines(screen):
   for c in range(1,cols):
    pygame.draw.line(screen,WHITE, (c*(WIDTH//cols), 0), (c*(WIDTH//cols),HEIGHT))

   for r in range(1,rows):
    pygame.draw.line(screen,WHITE,(0,r*(HEIGHT//rows)),(WIDTH,r*(HEIGHT//rows)))

       


    
    
if __name__ == "__main__":
    main()
