import pygame

def replace_fenetre(screen, map, map_posx, map_posy):
    if map.get_width() > screen.get_width():
        if map_posx > 0:
            map_posx = 0
        elif map_posx < screen.get_width() - map.get_width():
            map_posx = screen.get_width() - map.get_width()
        if map_posy > 0:
            map_posy = 0
        elif map_posy < screen.get_height() - map.get_height():
            map_posy = screen.get_height() - map.get_height()
    
    else:
        map_posx = 0
        if map_posy > 0:
            map_posy = 0
        elif map_posy < screen.get_height() - map.get_height():
            map_posy = screen.get_height() - map.get_height()
    return map_posx, map_posy

def move_fenetre(up, down, right, left):
     dir = pygame.Vector2(0,0)
     if up:
          dir += pygame.Vector2(0,10)
     if down:
          dir += pygame.Vector2(0,-10)
     if left:
          dir += pygame.Vector2(-10,0)
     if right:
          dir += pygame.Vector2(10,0)
     return dir

def focus_player(player, screen):
    screen_focus = -player.position
    screen_focus.x = screen_focus.x + screen.get_width()/2
    screen_focus.y = screen_focus.y + screen.get_height()/2
    return screen_focus
