import pygame
import random

colors = [
    (0,0,0),
    (0,240,240), # I block ( 4 in einer reihe block )
    (0,0,240), # J block
    (240,160,0), # L block 
    (240,240,0), # O block 
    (0,240,0), # S block 
    (160,0,240), # T block
    (240,0,0), # Z block
]

class Figure:
    x = 0
    y = 0
    
    Figures = [
       [[1,5,9,13],[4,5,6,7]], # I Block
       [[1,2,5,9],[0,4,5,6],[1,5,9,8],[4,5,6,7]], # J Block
       [[1,2,6,10],[5,6,7,9],[2,6,10,11],[3,5,6,7]], # L Block
       [[1,2,5,6]], # O Block
       [[6,7,9,10],[1,5,6,10]], # S Block
       [[1,4,5,6],[1,4,5,9],[4,5,6,9],[1,5,6,9]], # T Block
       [[4,5,9,10],[2,6,5,9]] # Z Block
    ]
    
    def __init__(self,x_coord,y_coord):
        self.x = x_coord
        self.y = y_coord
        self.type = random.randint(0,len(self.Figures)-1)
        self.color = colors[self.type + 1]
        self.rotation = 0
    
    def image(self):
        return self.Figures[self.type][self.rotation]
    
    
    def rotate(self):
        self.rotation = (self.rotation + 1) % (len(self.Figures[self.type]))

class Tetris():
    height = 0
    width = 0
    field = []
    score = 0
    state = "start"
    Figure = None
    
    def __init__(self,_height,_width):
        self.height = _height
        self.width = _width
        self.field = []
        self.score = 0
        self.state = "start"
        for i in range(_height):
            new_line = []
            for j in range(_width):
                new_line.append(0)
            self.field.append(new_line)
        self.new_figure()
            
    def new_figure(self):
        self.Figure = Figure(3,0)
        
    def go_down(self):
        self.Figure.y += 1
        if self.intersects():
            self.Figure.y -= 1
            self.freeze()
        
    def side(self, dx):
        old_x = self.Figure.x
        edge = False
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in self.Figure.image():
                    if j + self.Figure.x + dx < 0 or \
                       j + self.Figure.x + dx >= self.width or \
                       i + self.Figure.y >= self.height:
                        edge = True
        if not edge:
            self.Figure.x += dx
        if self.intersects():
            self.Figure.x = old_x

        
    
    def left(self):
        self.side(-1)
    
    def right(self):
        self.side(1)
    
    def down(self):
        while not self.intersects():
            self.Figure.y += 1
        self.Figure.y -= 1
        self.freeze()
    
    def rotate(self):
        old_rotation = self.Figure.rotation
        self.Figure.rotate()
        if self.intersects():
            self.Figure.rotation = old_rotation
        
    def intersects(self):
        intersection = False
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in self.Figure.image():
                    if i + self.Figure.y > self.height - 1 or \
                       i + self.Figure.y < 0 or \
                       self.field[i + self.Figure.y][j + self.Figure.x] > 0:
                        intersection = True
        return intersection
        
    def freeze(self):
        for i in range(4):
            for j in range(4):
                p = i*4 + j
                if p in self.Figure.image():
                    self.field[i + self.Figure.y][j + self.Figure.x] = self.Figure.type
        self.break_lines()
        self.new_figure()
        if self.intersects():
            self.state = "gameover"
            
    def break_lines(self):
        lines_cleared = 0
        for i in range(self.height - 1, 0, -1):
            if all(self.field[i]):
                lines_cleared += 1
                del self.field[i]
                self.field.insert(0, [0] * self.width)
        
        self.score += lines_cleared ** 2






pygame.init()
screen = pygame.display.set_mode((400,750))
pygame.display.set_caption("Tetris")
done = False
fps = 2
clock = pygame.time.Clock()
counter = 0
game = Tetris(20,10)
pressing_down = False
pressing_left = False
pressing_right = False
zoom = 30
BLACK = (0,0,0)
RED = (255,0,0)
WHITE = (255,255,255)
GRAY = (128,128,128)
while not done:
    if game.state == "start":
        game.go_down()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                game.rotate()
            if event.key == pygame.K_DOWN:
                pressing_down = True
            if event.key == pygame.K_LEFT:
                pressing_left = True
            if event.key == pygame.K_RIGHT:
                pressing_right = True
                
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                pressing_down = False
            if event.key == pygame.K_LEFT:
                pressing_left = False
            if event.key == pygame.K_RIGHT:
                pressing_right = False
        
        if pressing_down == True:
            game.down()
        if pressing_left == True:
            game.left()
        if pressing_right == True:
            game.right()
            
    screen.fill(color = WHITE)
    for i in range(game.height):
        for j in range(game.width):
            if game.field[i][j] == 0:
                color = GRAY
                just_border = 1
            else:
                just_border = 0
                color = colors[game.field[i][j]]
                
            pygame.draw.rect(screen,color,[30+j*zoom,30+i*zoom,zoom,zoom],just_border)
    if game.Figure is not None:
        for i in range(4):
            for j in range(4):
                p = i*4 + j
                if p in game.Figure.image():
                    pygame.draw.rect(screen,game.Figure.color,
                                     [30+(j+game.Figure.x)*zoom,30+(i+game.Figure.y)*zoom,zoom,zoom])
                
    gameover_font = pygame.font.SysFont("Calibri",65,True,False)
    text_gameover = gameover_font.render("Game Over !",True,(255,215,0))
    
    if game.state == "gameover":
        screen.blit(text_gameover, [30,250])
        
    score_font = pygame.font.SysFont("Calibri",15,True,False)
    text_score = score_font.render("Score: " + str(game.score),True,(255,215,0))
    screen.blit(text_score, [0,0])
    
    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
