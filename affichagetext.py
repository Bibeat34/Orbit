import pygame
import constant

pygame.init()
font1 = pygame.font.SysFont("Cambria", 12, True)
font2 = pygame.font.SysFont("Arial", 15, True)


def  affichetext_milieutrait(screen, text, start_position, end_position = None):
    if type(text) == float:
        new_text = round(text, 2)
    else: new_text = text     

    new_text = font1.render(f'{new_text}', True, "black", "white")
    if type(start_position) == pygame.Vector2 and type(end_position) == pygame.Vector2:
        position = (start_position + end_position) /2

        if start_position.x > end_position.x:
            text_rect = new_text.get_rect(bottomleft = position)
        else:
            text_rect = new_text.get_rect(bottomright = position)    
        screen.blit(new_text, text_rect)
        return        
    
    elif end_position == None:
        position = start_position
        text_rect = new_text.get_rect(midbottom = position)
        text_rect.y -= 25
        screen.blit(new_text, text_rect)
        return 

def affiche_vitesse_besoin(map, p1, p2, dt):
    distance = p1.position.distance_to(p2.position)
    texte = ""
    if distance == 0:
        return
    else:
        force = constant.G * p1.mass * p2.mass / (distance*1000 )**2
        force = force/ p1.mass
        force = round(force, 2) 
        texte = f'{force}m/s^2'
        texte = font1.render(texte, True, "black", "white")
        text_rect = texte.get_rect(center = (p1.position.x, p1.position.y + p1.radius + 5))
        map.blit(texte, text_rect)

def lockcam_texte_affiche(screen, x, y, lock):
    if lock:
        text = "Cam: Locked "
    else:
        text = "Cam: Free "    
    text = font2.render(text, True, "white")
    text_rect = text.get_rect(topright = (x,y))
    
    #text_rect.x = x - text_rect.width
    #text_rect.y = y + text_rect.height
    screen.blit(text, text_rect)        

 