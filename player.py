import pygame

class Player:
    def __init__(self, mass, x, y ):
        self.nom = "player"
        self.mass = mass
        self.position = pygame.Vector2(x, y)
        self.v = pygame.Vector2(0,1)
        self.direction = pygame.Vector2(0.-1)
        self.radius = 4
        self.is_accelerating = False

    def draw(self, map):
        body = self.update_body()
        if self.is_accelerating:
            self.smallburst(body, map)
        pygame.draw.polygon(map, "red", body)
        pygame.draw.circle(map, "white", body[0], 1)
    
    def update_position(self, dt):        
        self.position += self.v * dt

    def rotate(self, left, right):
        if left and right:
            return
        elif left:
            self.direction = self.direction.rotate(-5)            
        else:
            self.direction = self.direction.rotate(5)               

    def accelerate(self):
        self.v += self.direction * 8
            

    def update_body(self):
        pointe =  self.position + self.direction* self.radius
        base1 = self.position + self.direction.rotate(120)* self.radius
        base2 = self.position + self.direction.rotate(-120) * self.radius 
        body = [pointe, base1, base2]
        return body

    def smallburst(self, body, map):
        milieubase = body[1] + (body[2] - body[1])/2
        pointe = milieubase - (self.direction)* 4 
        b1 = milieubase + self.direction.rotate(90)* 2
        b2 = milieubase + self.direction.rotate(-90)* 2
        burst = [pointe, b1, b2]
        pygame.draw.polygon(map, "yellow", burst)
        