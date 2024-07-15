import pygame, random
import constant
from astre import Astre
from player import Player
from script import *
from affichagetext import affichetext_milieutrait, lockcam_texte_affiche
#from miniMap import replace_fenetre, move_fenetre



#DEFINITION FENETRE
screen = pygame.display.set_mode((constant.WIDTH, constant.HEIGHT))
pygame.display.set_caption('Gravity Simulation')
clock = pygame.time.Clock()


MINI_MAP_W = 200
MINI_MAP_H = 125

def main():

#DEFINITION DES VARIABLES

    space_map = pygame.Surface((6000,4000))
    fond_miniMap = pygame.Rect(0,0, MINI_MAP_W +4, MINI_MAP_H +4)
    
    planets = []
    big_planets = []

    miniMap_rect = pygame.Rect(2, 2, (screen.get_width() * MINI_MAP_W) /space_map.get_width(), (screen.get_height() * MINI_MAP_H) /space_map.get_height())
    posEcran = pygame.Vector2(0,0)

    nb_clic = 0
    color = ""
    size = 20
    creating = False 
    curseur_visu = pygame.Vector2(0,0)
    pos_init = pygame.Vector2(0,0)
    vect_norm = pygame.Vector2(10,0)

    last = 0
    afficher_vitesse = False
    afficher_direction = False
    afficher_rayon = False
    pause = False
    cam_lock = True
    key_zD, key_sD, key_qD, key_dD = False, False, False, False
    key_upD, key_downD, key_rightD, key_leftD = False, False, False, False
    key_RshiftD = False
    

#GENERATION GROSSE PLANETES
    for _ in range(constant.NUM_PLANETS):
        new_planet = Astre("Barbatruc", random.randint(100, space_map.get_width()-100), random.randint(100, space_map.get_height()-100), random.uniform(constant.MIN_MASS, constant.MAX_MASS), "red")
        planets.append(new_planet)
        big_planets.append(new_planet)

#GENERATION PETIT ASTEROIDES
    for _ in range(constant.NUM_ASTEROID):
        x, y = 500, 300
        x = random.randint(1, space_map.get_width()-1)    
        y = random.randint(1, space_map.get_height()-1)
        new_planet = Astre("asteroid", x, y, random.uniform(1*(10**4), 1*(10**6)), "blue")
        planets.append(new_planet)

#GENERATION JOUEUR
    player = Player(1000, 200, 200)
    planets.append(player)

#APPARITION MANUELLE
    soleil = Astre("Soleil", space_map.get_width()/2, space_map.get_height()/2, constant.MAX_MASS, "yellow")
    planets.append(soleil)
    big_planets.append(soleil)
    """
    centaurus = Astre("Soleil", space_map.get_width()/2 + 600, space_map.get_height()/2, constant.MAX_MASS, "yellow")
    planets.append(centaurus)
    big_planets.append(centaurus)
    
    elios = Astre("Soleil", space_map.get_width()/2 + 300, space_map.get_height()/2 -520, constant.MAX_MASS, "yellow")
    planets.append(elios)
    big_planets.append(elios) 
    """      


#DEBUT DE LA BOUCLE
    running = True
    while running:
        dt = 0.02
        clock.tick(60)/1000.0

        if creating:
            vect_norm = strength_direction(vect_norm, key_zD, key_sD, key_dD, key_qD, key_RshiftD)
        else:
            if key_qD or key_dD:
                player.rotate(key_qD, key_dD)
            if key_zD:    
                player.accelerate()  
        if not cam_lock:
            posEcran += move_fenetre(key_upD, key_downD, key_leftD, key_rightD)
        else:
            posEcran = focus_player(player, screen)


        posEcran.x, posEcran.y = replace_fenetre(screen, space_map, posEcran.x, posEcran.y)     
        miniMap_rect.x = (-posEcran.x * MINI_MAP_W) /space_map.get_width() +2
        miniMap_rect.y = (-posEcran.y * MINI_MAP_H) /space_map.get_height() +2
        
        
    #POUR QUITTER LE JEU
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        #DETECTE LES TOUCHES

            #Pour afficher ou non des infos
                elif event.key == pygame.K_e:
                    afficher_vitesse = not afficher_vitesse
                elif event.key == pygame.K_t:
                    afficher_direction = not afficher_direction 
                elif event.key == pygame.K_r:
                    afficher_rayon = not afficher_rayon

            #Pour modifier la v et l'orientation de la planète créer                
                elif event.key == pygame.K_d:
                    key_dD = True
                elif event.key == pygame.K_q:
                    key_qD = True
                elif event.key == pygame.K_z:
                    key_zD = True
                    if not creating:
                        player.is_accelerating = True
                elif event.key == pygame.K_s:
                    key_sD = True
                elif event.key == pygame.K_RSHIFT:
                    key_RshiftD = True
            #Pour modifier la taille de la planète créer
                elif event.key == pygame.K_KP1 or event.key == pygame.K_1:    
                    size = switch_size(1)
                    planets[last-1].update_mass(1*(10**size))
                elif event.key == pygame.K_KP2 or event.key == pygame.K_2:
                    size = switch_size(2)
                    planets[last-1].update_mass(1*(10**size))
                elif event.key == pygame.K_KP3 or event.key == pygame.K_3:
                    size = switch_size(3)
                    planets[last-1].update_mass(1*(10**size))        

            #Pour ce déplacer sur la carte
                elif event.key == pygame.K_UP:
                    key_upD = True
                elif event.key == pygame.K_DOWN:
                    key_downD = True
                elif event.key == pygame.K_RIGHT:
                    key_rightD = True
                elif event.key == pygame.K_LEFT:
                    key_leftD = True

            #Met la simulation en pause
                elif event.key == pygame.K_p:
                    if not creating:
                        pause = not pause

                elif event.key == pygame.K_o:
                    pass
                    #vect_norm = miseOrbit(planets[last-1], soleil)  Ne fonctionne plus
                        
            #VALIDER AVEC ENTREE
                elif event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:                    
                    planets[last-1].v = vect_norm
                    vect_norm = pygame.Vector2(10,0)
                    creating = False
            #Supprimer la dernière planète
                elif event.key == pygame.K_DELETE:
                    if len(big_planets) > 0:                                            
                        last = delete_planet(last, planets, big_planets)   

                elif event.key == pygame.K_SPACE:                    
                    cam_lock = not cam_lock    
        #Détecte le relachement des touches
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    key_dD = False
                elif event.key == pygame.K_q:
                    key_qD = False
                elif event.key == pygame.K_z:
                    key_zD = False
                    if not creating:
                        player.is_accelerating = False
                elif event.key == pygame.K_s:
                    key_sD = False 
                elif event.key == pygame.K_UP:
                    key_upD = False
                elif event.key == pygame.K_DOWN:
                    key_downD = False
                elif event.key == pygame.K_RIGHT:
                    key_rightD = False
                elif event.key == pygame.K_LEFT:
                    key_leftD = False         
                elif event.key == pygame.K_RSHIFT:
                    key_RshiftD = False    

        #CLIC SOURIS POUR CREER UNE NOUVELLE PLANETE
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if not creating:
                        mousex, mousey = pygame.mouse.get_pos()
                        nb_clic, color = switch_color(nb_clic)
                        new_planet = Astre("nouveau", mousex -posEcran.x, mousey -posEcran.y, 1*(10**20), color)            
                        planets.append(new_planet)
                        big_planets.append(new_planet)
                        last = len(planets)
                    #VARIABLE UPDATE
                        creating = True
                        curseur_visu.x = planets[last-1].position.x
                        curseur_visu.y = planets[last-1].position.y
                        pos_init = curseur_visu
          


#MISE A JOUR ECRAN
        screen.fill("white")  
        space_map.fill("black")

        for planet in planets:
            planet.draw(space_map)
       # player.draw(space_map)    

        if pause:
            pass
        else: 
        #SI EN TRAIN DE CREER UNE PLANETE
            if creating:
                curseur_visu = pos_init + (vect_norm)               
                
                pygame.draw.line(space_map, "red", planets[last-1].position, curseur_visu, 2)
                planets[last-1].v = vect_norm
                predictPos(space_map, planets[last-1], big_planets, dt)
                affiche_distance(space_map, planets[last-1], soleil, dt)
                affichetext_milieutrait(space_map, vect_norm.length(), pos_init, curseur_visu)
                            

        #TOUT LE RESTE DU TEMPS
            else:  
                #player.update_pos(dt)          

                for planet in planets:
                    planet.update_position(dt)

                #repose(space_map, planets)        #pour que les objets réaparaissent de l'autre coté du monde lorsqu'ils touchent un bord
                wall_bounce(space_map, planets)    #pour que les objets rebondissent sur les bords du monde   
                update_velocities(planets, big_planets, dt)                
                no_touch(planets)

        for planet in big_planets:
            if afficher_vitesse:    
                planet.affiche_vitesse(space_map)
            if afficher_direction:
                planet.affiche_direction(space_map)
            if afficher_rayon:        
                planet.affiche_rayon(space_map)                

        screen.blit(space_map, posEcran)

        #Blit la miniMap    
        mini_map = pygame.transform.scale(space_map, (MINI_MAP_W,MINI_MAP_H))
        pygame.draw.rect(screen, "light grey", fond_miniMap)
        screen.blit(mini_map, (2,2))
        pygame.draw.rect(screen, 'red', miniMap_rect, 1)

        
        lockcam_texte_affiche(screen, screen.get_width(), 0, cam_lock)


        pygame.display.flip()
        

    pygame.quit()

if __name__ == '__main__':
    main()