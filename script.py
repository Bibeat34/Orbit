import pygame, constant, copy
from affichagetext import affichetext_milieutrait, affiche_vitesse_besoin
from colider import *
from camera import *


def calculate_gravitational_force(p1, p2):
    direction_vect = p2.position - p1.position
    direction_vect = direction_vect.normalize()

    distance = p1.position.distance_to(p2.position)
    if distance == 0:
        return pygame.Vector2(0, 0)
    
    force = constant.G * (p1.mass * p2.mass) / ((distance*500)**2)
    vforce = direction_vect * force
    return vforce

def update_velocities(objects, big_planets, dt):
    for p1 in objects:
        attract_general = pygame.Vector2(0, 0)
        for p2 in big_planets:
            if p1 != p2:
                if constant.RAYON_ACTION != 0: 
                    if p1.position.distance_to(p2.position) <= constant.RAYON_ACTION:
                        v_attract = calculate_gravitational_force(p1, p2)
                        attract_general += v_attract
                else:
                    v_attract = calculate_gravitational_force(p1, p2)
                    attract_general += v_attract        

        p1.v += attract_general / p1.mass * dt       

def repose(screen, planet_list):
    for planet in planet_list:
        if planet.position.x > screen.get_width():
            planet.position.x = 0
        elif planet.position.x < 0:
            planet.position.x = screen.get_width()
        if planet.position.y > screen.get_height():
            planet.position.y = 0
        elif planet.position.y < 0:
            planet.position.y = screen.get_height() 

def wall_bounce(surface, planet_list):
    for planet in planet_list:
        if planet.position.x + planet.radius > surface.get_width():
            planet.v = planet.v.reflect((1,0))
        elif planet.position.x - planet.radius < 0:
            planet.v = planet.v.reflect((1,0))
        if planet.position.y + planet.radius > surface.get_height():
            planet.v = planet.v.reflect((0,1))
        elif planet.position.y - planet.radius < 0:
            planet.v = planet.v.reflect((0,1))           
       

def switch_color(nb_clic):
    color = "brown"
    match nb_clic:
        case 0:
            color = "purple"
        case 1:
            color = "green"                        
        case 2:
            color = "blue"
        case 3:
            color = "grey"
        case 4:
            color = "white"
        case 5:
            color = "orange"
        case _:
            color = "pink"
            nb_clic = -1

    nb_clic += 1
    return nb_clic, color

def switch_size(nb):
    match nb:
        case 1: return 20
        case 2: return 18
        case 3: return 22
        case _: return 20 

def delete_planet(last, planets, big_planets):
    del planets[last-1]
    last = len(big_planets)
    del big_planets[last-1]
    last = len(planets)
    return last

def strength_direction(vector, more, less, right, left, shiftD):
    mult = 1
    if shiftD:
        mult = 0.01
    if more:
        vector.scale_to_length(vector.length() + mult)
    if less:
        if vector.length() < 2:
            vector.scale_to_length(1)
        else:     
            vector.scale_to_length(vector.length() - mult) 
    if left:
        vector = vector.rotate( -mult)            
    if right:                       
        vector = vector.rotate(mult)
    return vector
 
def affiche_distance(map, new_planet, near_planet, dt):
    dist = new_planet.position.distance_to(near_planet.position)
    dist = round(dist, 2) * 100
    text = f'{dist}km'
    pygame.draw.line(map, "white", new_planet.position, near_planet.position)
    affichetext_milieutrait(map, text, new_planet.position, near_planet.position)
    affiche_vitesse_besoin(map, new_planet, near_planet, dt)

#A REFAIRE
def miseOrbit(p1, p2):
    direction_vect = p2.position - p1.position
    direction_vect = direction_vect.normalize()
    direction_vect = direction_vect.rotate(90)

    distance = p1.position.distance_to(p2.position) 
    force = constant.G * p1.mass * p2.mass / (distance*1000)**2
    vectForce = direction_vect * force
    vectForce = vectForce / p1.mass
    return vectForce

def predictPos(map, p1, planets, dt):      #dt = 0.02
     
    planet = copy.deepcopy(p1)
    for _ in range(5000):
        attract_general = pygame.Vector2(0, 0)                
        for p2 in planets:
            if p2 == p1:
                pass
            else:    
                v_force = calculate_gravitational_force(planet, p2)
                attract_general += v_force

                if planet.position.distance_to(p2.position) <= p2.radius:
                    return

        planet.v += attract_general / planet.mass * 0.02        
        planet.update_position(0.02)
        pygame.draw.line(map, "blue", planet.position, planet.position + (planet.v * 0.02))
        
       # pygame.draw.circle(map, "blue", planet.position, 2)
        if _%100 == 0:
            pygame.draw.circle(map, "red", planet.position, planet.radius, 1)
       
  