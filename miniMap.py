import pygame

def dezoom(zoomforce, map, ecran_rect):

    match zoomforce:
        case 1:
                map = pygame.transform.scale(map, (2000, 2000))
                ecran_rect.w = (ecran_rect.w*150) /2000
                ecran_rect.h = (ecran_rect.h*150) /2000             
                return map,1, ecran_rect
        case 0:
                map = pygame.transform.scale(map, (1000, 1000))
                return map,2, ecran_rect
        case 2:
                map = pygame.transform.scale(map, (2500, 2500))
                ecran_rect.w = (ecran_rect.w*150) /2500
                ecran_rect.h = (ecran_rect.h*150) /2500
                return map,0.8, ecran_rect
        case 3:
                map = pygame.transform.scale(map, (3000, 3000))
                ecran_rect.w = (ecran_rect.w*150) /3000
                ecran_rect.h = (ecran_rect.h*150) /3000 
                return map,0.67, ecran_rect
        case 4:
                map = pygame.transform.scale(map, (4000, 4000))
                ecran_rect.w = (ecran_rect.w*150) /4000
                ecran_rect.h = (ecran_rect.h*150) /4000
                return map,0.5, ecran_rect
                