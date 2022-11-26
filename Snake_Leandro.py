import pygame
import random
from enum import Enum
from collections import namedtuple
pygame.init()
zoneText= pygame.font.SysFont("arial",25)

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point= namedtuple("Point","x, y")

#RGB COLORS

Blanc=(255,255,255)
Rouge=(200,0,0)
Bleu1=(0,0,255)
Bleu2=(0,100,255)
Noir=(0,0,0)

Taille= 20
Speed=50
class Snake:

    def __init__(self,longueur=640,largeur=480):
        self.longueur=longueur
        self.largeur=largeur

        #init display
        self.display=pygame.display.set_mode((self.longueur,self.largeur))
        pygame.display.set_caption("Snake leandro")
        self.clock=pygame.time.Clock()
        #init game state

        self.direction= Direction.RIGHT
        self.tete= Point(self.longueur/2, self.largeur/2)
        self.snake= [self.tete,Point(self.tete.x-Taille,self.tete.y), Point(self.tete.x-(2*Taille),self.tete.y)]
        self.score=0
        self.food=None
        self._spawn_food()
    def _spawn_food(self):
        x = random.randint(0,(self.longueur-Taille)//Taille)* Taille
        y = random.randint(0,(self.largeur-Taille)//Taille)*Taille
        self.food= Point(x,y)
        if self.food in self.snake:
            self._spawn_food()
    def etapeDuJeu(self):
        #Collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.direction= Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    self.direction= Direction.RIGHT
                elif event.key == pygame.K_UP:
                    self.direction= Direction.UP
                elif event.key == pygame.K_DOWN:
                    self.direction= Direction.DOWN

        #move
        self.move(self.direction) #met a jour la tete
        self.snake.insert(0,self.tete)

        gameOver=False
        if self.isCollision():
            gameOver=True
            return gameOver,self.score

        #place new food or just move

        if self.tete == self.food:
            self.score += 1
            self._spawn_food()
        else:
            self.snake.pop()

        #update ui and clock

        self.updateUi()
        self.clock.tick(Speed)

        #return game over and score

        gameOver=False
        return gameOver,self.score
    def isCollision(self):

        if self.tete.x > self.longueur - Taille or self.tete.x < 0 or self.tete.y > self.largeur -Taille or self.tete.y < 0:
            return True

        if self.tete in self.snake[1:]:
            return True

        return False

    def updateUi(self):
        self.display.fill(Noir)
        for pt in self.snake:
            pygame.draw.rect(self.display,Bleu1,pygame.Rect(pt.x,pt.y,Taille,Taille))
            pygame.draw.rect(self.display, Bleu2, pygame.Rect(pt.x+4, pt.y+4, Taille-8, Taille-8))

        pygame.draw.rect(self.display,Rouge,pygame.Rect(self.food.x,self.food.y,Taille,Taille))

        text= zoneText.render("Score: "+ str(self.score),True,Blanc)
        self.display.blit(text,[0,0])
        pygame.display.flip()

    def move(self,direction):
        x = self.tete.x
        y = self.tete.y
        if direction == Direction.RIGHT:
            x+=Taille
        elif direction == Direction.LEFT:
            x -= Taille
        elif direction == Direction.DOWN:
            y += Taille
        elif direction == Direction.UP:
            y -= Taille

        self.tete= Point(x,y)





if __name__ == '__main__':
    game = Snake()

    while True:
        gameOver,score = game.etapeDuJeu()

        if gameOver==True:
            break
    print("Score : ", score)

    pygame.quit()

