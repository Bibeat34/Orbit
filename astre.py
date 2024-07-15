import pygame, constant
from affichagetext import affichetext_milieutrait


class Astre():
    def __init__(self, nom, x, y , mass, color):        
        self.nom = nom
        self.mass = mass
        self.position = pygame.Vector2(x, y)
        self.radius = 20 * (mass / constant.MAX_MASS) ** (1/3)
        self.color = color
        self.v = pygame.Vector2(1,1)

        count = 1     
        while mass > 10:
            mass = mass/10
            count += 1
        if self.nom == "Soleil":
            self.radius = 40
        elif count < 8:
           # print('plus petit que ^8')
            self.radius = 2 
        else:
            self.radius = 2*(2*count-30)
            print(self.radius)     
        

    def draw(self, screen):
        if self.radius <= 2:
            pygame.draw.circle(screen, self.color, self.position, 2)
        else:    
            pygame.draw.circle(screen, self.color, self.position, self.radius)
        

    def update_position(self, dt):
        if self.nom == "Soleil":
            self.v = pygame.Vector2(0,0)
        else:
            self.position += self.v * dt        

    def affiche_direction(self, screen):
        if self.v.length() < 10 and self.v.length() > 0:
           longueur = self.v.normalize()
           longueur = longueur * 10 
           pygame.draw.line(screen, "yellow", self.position, self.position +longueur) 
        else:    pygame.draw.line(screen, "yellow", self.position, self.position + self.v)

    def affiche_vitesse(self, screen):
        affichetext_milieutrait(screen, self.v.length(), self.position)

    def affiche_rayon(self, screen):
        if constant.RAYON_ACTION != 0:
            pygame.draw.circle(screen, "red", self.position, constant.RAYON_ACTION, 1)

    def copy(self):
        mass, pos, v = self.mass, self.position, self.v
        return mass, pos, v

    def update_mass(self, new_mass):
        count = 1
        self.mass = new_mass      
        while new_mass > 10:
            new_mass = new_mass/10
            count += 1                             
        self.radius = 2*(2*count-30)
        print(self.radius)
    