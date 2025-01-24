import pygame
import random
from numpy import matmul
import pandas as pd

data = pd.read_csv("IRIS.csv")
X = data.drop('species',axis=1)
y = data['species']
# Generate a list of 10 random 4-element tuples with integers from 1 to 100
random.seed(10)
random_tuples = [[random.randint(-5, 5) for _ in range(4)]+[1] for _ in range(10)]
random_colors = {label:tuple(random.randint(0, 255) for _ in range(3)) for label in y.unique()}


wheel_pos = 0

def proj_matrix(alpha,beta) :
    return [
    [1,0,alpha/50.,beta/50.,0],
    [0,1,beta/50.,alpha/50.,0],
    [0,0,0,0,1]]
center_0_matrix= [
    [1,0,350],
    [0,1,250],
    [0,0,1]]   
def scale_matrix(alpha):
    return[
    [alpha+50,0,0],
    [0,alpha+50,0],
    [0,0,1]
]


def normalize(point):
    return [float(coord)/point[-1] for coord in point[:-1]]

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# initialize pygame
pygame.init()
screen_size = (700, 500)

pygame.font.init() # you have to call this at the start, 
                   # if you want to use this module.
font = pygame.font.SysFont('Arial', 30)

# create a window
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("pygame Test")
 
# clock is used to set a max fps
clock = pygame.time.Clock()

alpha = 0
beta = 0


running = True
dragging = False
start_pos = end_pos = pos = prev_pos = [0,0]
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEWHEEL:
            wheel_pos += event.y
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if not dragging:
                    start_pos = event.pos 
                dragging = True
        elif event.type == pygame.MOUSEMOTION:
            if dragging:
                pos[0]+= event.pos[0]-prev_pos[0]
                pos[1]+= event.pos[1]-prev_pos[1]
            prev_pos = event.pos
                

        # Detect mouse button release
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                dragging = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                pos= [0,0]
            if event.key == pygame.K_m:
                print(proj_matrix(pos[0],pos[1]))
    #clear the screen
    screen.fill(BLACK)
    
    def pipeline(point):
        point = matmul(proj_matrix(pos[0],pos[1]),point)
        point = matmul(scale_matrix(wheel_pos),point)
        point = matmul(center_0_matrix,point)
        point = normalize(point)
        return point
    
    for point,label in zip(X.values,y.values):
        point = point.tolist() + [1]
        point = pipeline(point)
        pygame.draw.circle(screen,random_colors[label],(point[0],point[1]),5)


    origin = pipeline([0,0,0,0,1])
    x = pipeline([10000,0,0,0,1])
    y_ = pipeline([0,10000,0,0,1])
    z = pipeline([0,0,10000,0,1])
    w = pipeline([0,0,0,10000,1])
    pygame.draw.line(screen,'white',origin,x)
    pygame.draw.line(screen,'white',origin,y_)
    pygame.draw.line(screen,'white',origin,z)
    pygame.draw.line(screen,'white',origin,w)
    # pygame.draw.circle(screen,"blue",start_pos,5)
    # pygame.draw.circle(screen,"yellow",(pos[0]+350,pos[1]+250),5)

    text_surface = font.render(str(wheel_pos), False, 'red')
    screen.blit(text_surface, (0,0))
    # flip() updates the screen to make our changes visible
    pygame.display.flip()
     
    # how many updates per second
    clock.tick(60)

pygame.quit()
