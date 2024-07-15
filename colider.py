import constant


def detect_collide(p1, p2):
    distance = p1.position.distance_to(p2.position)
    return distance < p1.radius + p2.radius

def no_touch(planets):
    for i, p1 in enumerate(planets):
        for j, p2 in enumerate(planets):            
            if j > i:
                same_dir = False                
                if detect_collide(p1,p2):
                    if p1.v.dot(p2.v) >= 20:
                        same_dir = True
                    vect = p1.position - p2.position
                    dist = vect.length()
                    if dist == 0:
                        dist = 0.1
                    vect_delta = vect * (p1.radius + p2.radius - dist) / dist
                    v1 = p1.v
                    v2 = p2.v
                    delta_speed = v1-v2
                    vect_delta_norm = vect_delta.normalize()
                    p = delta_speed.dot(vect_delta_norm)                    
                    
                    if p1.radius == 2 and p2.radius == 2:
                        p1.position += vect_delta / 2
                        p2.position -= vect_delta / 2
                        p1.v -= p * vect_delta_norm
                        p2.v += p * vect_delta_norm
                    elif p1.nom == "asteroid" and p2.nom == "asteroid":
                        p1.position += vect_delta / 2
                        p2.position -= vect_delta / 2
                        p1.v -= p * vect_delta_norm
                        p2.v += p * vect_delta_norm    
                    
                    elif p1.radius - p2.radius < -2:
                        p1.position += vect_delta
                        p1.v -= vect_delta_norm * p
                        if not same_dir:
                            p1.v *= 0.8
                                
                    elif p1.radius - p2.radius > 2:
                        p2.position -= vect_delta
                        p2.v += vect_delta_norm * p
                        if not same_dir:
                            p2.v *= 0.8
                             
                    else:                                                           
                        p1.position += vect_delta / 2
                        p2.position -= vect_delta / 2

                        # Calculer les vitesses normales
                        v1_norm = p1.v.dot(vect_delta.normalize()) * vect_delta.normalize()
                        v2_norm = p2.v.dot(vect_delta.normalize()) * vect_delta.normalize()

                        # Calculer les vitesses tangentielles
                        v1_tang = (p1.v - v1_norm) /2
                        v2_tang = (p2.v - v2_norm) /2
                        
                        if p1.v.length() < 30 or p2.v.length() < 30:
                            new_v1_norm = v2_norm *1
                            new_v2_norm = v1_norm *1
                        else:    
                            new_v1_norm = v2_norm * 0.7
                            new_v2_norm = v1_norm * 0.7 #coefficient_restitution
                            
                        
                        p1.v = v1_tang + new_v1_norm
                        p2.v = v2_tang + new_v2_norm
    

        if p1.v.length() > constant.MAX_SPEED:
            p1.v = p1.v.normalize() * constant.MAX_SPEED 