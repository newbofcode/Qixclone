import pygame
import random
import sys

pygame.init()    

WIN_H,WIN_W = 800,800
FIELD_TOP_LEFT = (100,100)
FIELD_TOP_RIGHT = (700,100)
FIELD_BOTTOM_RIGHT = (700,705)
FIELD_BOTTOM_LEFT = (100,705)
window = pygame.display.set_mode((WIN_W,WIN_H))
pygame.display.set_caption("Qix Clone")
FPS = 60
PLAYER_IMAGE = pygame.image.load('Assets/player.png')
PLAYER = pygame.transform.scale(PLAYER_IMAGE,(11,11))
WHITE = (255,255,255)
BLACK = (0,0,0)
FILLCOLOR = (255,0,0)
QCOLOR = (0, 255, 0)
TRAILCOLOR = (255, 255, 0)
TOTALFILLED = 0
WINTHRESHOLD = 181500 #half of playable space
SPARK_IMAGE = pygame.image.load('Assets/spark.jpg')
SPARK = pygame.transform.scale(SPARK_IMAGE,(11,11))
QIXMASK = pygame.Surface((1,1))
QIXMASK.fill(BLACK)
direct = 1
sparx_speed = 2
qix_speed = [3,3]
qixee = pygame.image.load("Assets/qixEn.png")
qix = qixee.get_rect()
qix.centery = 365
qix.centerx = 250
player = pygame.Rect(95,300,11,11)
trail = []
list1 = []
rightdir = False
leftdir = False
downdir = False
updir = False
field = WHITE

font = pygame.font.Font('freesansbold.ttf',32)
lives_value = 3
textX = 10
textY = 10
def show_score(x,y):
    score = font.render("Score : " + str(TOTALFILLED),True, (0,255,0))
    lives = font.render("Lives : "+ str(lives_value),True,(0,255,0))
    percent = font.render("Percent Captured : "+ str((TOTALFILLED*100)//(2*WINTHRESHOLD)) +"% (50% to win!)" ,True,(0,255,0))
    window.blit(score,(x,y))
    window.blit(lives,(x,y+32))
    window.blit(percent,(x+200,y+32))

def resetPlayer():
    global player
    global field 
    global trail 
    global list1 
    global leftdir
    global rightdir
    global updir
    global downdir
    global lives_value
    lives_value -= 1
    if lives_value <= 0:  #lose screen
            message = font.render("GAME OVER", True, (0,255,0))
            message2 = font.render("press Q to exit", True, (0,255,0) )
            window.blit(message,(320, 325))
            window.blit(message2,(300, 375))
            pygame.display.update()
            while True:
                for event in pygame.event.get():
                    if event.type ==  pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            pygame.quit()
                            sys.exit()

    player = pygame.Rect(95,300+ random.randint(-200,200),11,11)
    trail = []
    list1 = []
    rightdir = False
    leftdir = False
    downdir = False
    updir = False
    field = WHITE
    

def removingback(directlist):
    if direct == 0:
        directlist.remove(2)
    elif direct == 1:
        directlist.remove(3)
    elif direct == 2:
        directlist.remove(0)
    elif direct == 3:
        directlist.remove(1)

def enemyspark(enemy,checkL,checkR,checkU,checkD):
    global direct, sparx_speed
    if checkL & checkU & checkR & checkD:
        a = [0,1,2,3]
        removingback(a)
        direct = random.choice(a)
        sparx_speed = 2
    elif checkL & checkR & checkU:
        b = [0,1,2]
        removingback(b)
        direct = random.choice(b)
        sparx_speed = 2
    elif checkL & checkR & checkD:
        c = [0,2,3]
        removingback(c)
        direct = random.choice(c)
        sparx_speed = 2
    elif checkL & checkU & checkD:
        d = [0,1,3]
        removingback(d)
        direct = random.choice(d)
        sparx_speed = 2
    elif checkR & checkU & checkD:
        e = [2,1,3]
        removingback(e)
        direct = random.choice(e)
        sparx_speed = 2
    elif checkL & checkD:
        f = [0,3]
        removingback(f)
        direct = random.choice(f)
        sparx_speed = 2
    elif checkL & checkU:
        g = [0,1]
        removingback(g)
        direct = random.choice(g)
        sparx_speed = 2
    elif checkR & checkD:
        h = [2,3]
        removingback(h)
        direct = random.choice(h)
        sparx_speed = 2
    elif checkR & checkU:
        i = [1,2]
        removingback(i)
        direct = random.choice(i)
        sparx_speed = 2
    
    if direct == 0:
        if checkL == False:
            sparx_speed = 1
        enemy.move_ip(-sparx_speed,0)
    elif direct == 1:
        if checkU == False:
            sparx_speed = 1
        enemy.move_ip(0,-sparx_speed)
    elif direct == 2:
        if checkR == False:
            sparx_speed = 1
        enemy.move_ip(sparx_speed,0)
    elif direct == 3:
        if checkD == False:
            sparx_speed = 1
        enemy.move_ip(0,sparx_speed)    

def floodFill(window, point): 
    tempArea = 0
    Sf = window.copy()
    unexplored = [point]
    count = 0
    while len(unexplored) != 0:
        newPoint = unexplored.pop()
        if Sf.get_at((newPoint[0],newPoint[1]))[:3] == WHITE or Sf.get_at((newPoint[0],newPoint[1]))[:3] == FILLCOLOR:
            continue
        elif Sf.get_at((newPoint[0],newPoint[1]))[:3] == BLACK:
            Sf.set_at((newPoint[0],newPoint[1]), FILLCOLOR)
            tempArea +=1
            unexplored.append((newPoint[0] + 1, newPoint[1]))  
            unexplored.append((newPoint[0] - 1, newPoint[1]))  
            unexplored.append((newPoint[0], newPoint[1] + 1))  
            unexplored.append((newPoint[0], newPoint[1] - 1))
        else:
            return None   #Anything that is not WHITE, BLACK,  or FILLCOLOR is considered the Qix and fill is rejected
    global TOTALFILLED
    TOTALFILLED += tempArea
    return Sf


def main():
    global player
    global field 
    global trail 
    global list1 
    global leftdir
    global rightdir
    global updir
    global downdir
    clock = pygame.time.Clock()
    
    playing = True
    linelist = []
    s2 = window.copy()
    somethingfilled = False
    spark = pygame.Rect(95,100,11,11)
    
    while playing:

        clock.tick(FPS)

        window.fill((0,0,255)) # makes the outside colour
        window.fill((0,0,0),(100,100,600,605)) # makes the field colour
        
        #drawing the filld area
        if somethingfilled: 
            window.blit(s2, (0,0))
        
        #drawing the field border
        pygame.draw.lines(window,(255,255,255),True,[FIELD_TOP_LEFT,FIELD_TOP_RIGHT,FIELD_BOTTOM_RIGHT,FIELD_BOTTOM_LEFT])
        
        #drawing the white lines
        for ln in linelist:
            pygame.draw.lines(window,WHITE,False,ln) 
        
        pygame.draw.rect(window, QCOLOR, pygame.Rect(qix.centerx, qix.centery, 1, 1))
        for t in trail:
            window.set_at(t, TRAILCOLOR)
            if qix.collidepoint(t):
                resetPlayer()
                break

        bl = window.get_at((player.centerx-1,player.centery))[:3] != BLACK
        br = window.get_at((player.centerx+1,player.centery))[:3] != BLACK
        bu = window.get_at((player.centerx,player.centery-1))[:3] != BLACK
        bd = window.get_at((player.centerx,player.centery+1))[:3] != BLACK
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
            if event.type ==  pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    field = BLACK
                if (bl&br&bu&bd):
                    field = WHITE

        
        keys_pressed = pygame.key.get_pressed()

        #if keys_pressed[pygame.K_SPACE]: #This will change the field
         #   field = (0,0,0)
        #player movements, can be moved to the player class later to make things cleaner
        if keys_pressed[pygame.K_LEFT] & (window.get_at((player.centerx-1,player.centery))[:3] == field) & (window.get_at((player.centerx-2,player.centery))[:3] != TRAILCOLOR):
            if field == (0,0,0):
                trail.append(player.center)
                if rightdir == False:
                    if not leftdir:
                        list1.append(player.center)
                    player.move_ip(-1,0)
                    leftdir = True
                    updir = False
                    downdir = False
            else:
                player.move_ip(-1,0)
            #changes the field back to normal and reset some variables. Can be moved to a different method for clearner code. Example fieldReset()
            if (window.get_at((player.centerx-1,player.centery))[:3] == (255,255,255)) & (field == (0,0,0)):
                field = (255,255,255)
                #adding into list of lines for drawlines loop and resets corner lists (list1)
                list1.append(player.center)
                linelist.append(list1)
                pygame.draw.lines(window,(255,255,255),False, list1)   
                s2 = floodFill(window, (list1[-1][0]+1,list1[-1][1]+1 ) )
                if s2 == None:
                    s2 = floodFill(window, (list1[-1][0]+1,list1[-1][1]-1 ) )
                somethingfilled = True
                list1 = []
                trail =[]
                rightdir = False
                leftdir = False
                downdir = False
                updir = False
        elif keys_pressed[pygame.K_RIGHT] & (window.get_at((player.centerx+1,player.centery))[:3] == field) & (window.get_at((player.centerx+2,player.centery))[:3] != TRAILCOLOR):
            if field == (0,0,0):
                trail.append(player.center)
                if leftdir == False:
                    if not rightdir:
                        list1.append(player.center)
                    player.move_ip(1,0)
                    rightdir = True
                    updir = False
                    downdir = False
            else:
                player.move_ip(1,0)
            if (window.get_at((player.centerx+1,player.centery))[:3] == (255,255,255)) & (field == (0,0,0)): #if the center hits the white line the field changes
                field = (255,255,255)
                #adding into list of lines for drawlines loop and resets corner lists (list1)
                list1.append(player.center)
                linelist.append(list1)
                pygame.draw.lines(window,(255,255,255),False, list1)
                s2 = floodFill(window, (list1[-1][0]-1,list1[-1][1]+1 ) )
                if s2 == None:
                    s2 = floodFill(window, (list1[-1][0]-1,list1[-1][1]-1 ) )
                somethingfilled = True
                list1 = []
                trail =[]
                rightdir = False
                leftdir = False
                downdir = False
                updir = False
        elif keys_pressed[pygame.K_DOWN] & (window.get_at((player.centerx,player.centery+1))[:3] == field) & (window.get_at((player.centerx,player.centery+2))[:3] != TRAILCOLOR):
            if field == (0,0,0):
                trail.append(player.center)
                if updir == False:
                    if not downdir:
                        list1.append(player.center)
                    player.move_ip(0,1)
                    downdir = True
                    leftdir = False
                    rightdir = False
            else:
                player.move_ip(0,1)
            if (window.get_at((player.centerx,player.centery+1))[:3] == (255,255,255)) & (field == (0,0,0)): #if the center hits the white line the field changes
                field = (255,255,255)
                #adding into list of lines for drawlines loop and resets corner lists (list1)
                list1.append(player.center)
                linelist.append(list1)
                pygame.draw.lines(window,(255,255,255),False, list1)
                s2 = floodFill(window, (list1[-1][0]+1, list1[-1][1]-1 ) )
                if s2 == None:
                    s2 = floodFill(window, (list1[-1][0]-1, list1[-1][1]-1 ) )
                somethingfilled = True
                list1 = []
                trail =[]
                rightdir = False
                leftdir = False
                downdir = False
                updir = False
        elif keys_pressed[pygame.K_UP] & (window.get_at((player.centerx,player.centery-1))[:3] == field) & (window.get_at((player.centerx,player.centery-2))[:3] != TRAILCOLOR):
            if field == (0,0,0):
                trail.append(player.center)
                if downdir == False:
                    if not updir:
                        list1.append(player.center)
                    player.move_ip(0,-1)
                    updir = True
                    leftdir = False
                    rightdir = False
            else:
                player.move_ip(0,-1)
            if (window.get_at((player.centerx,player.centery-1))[:3] == (255,255,255)) & (field == (0,0,0)): #if the center hits the white line the field changes
                field = (255,255,255)
                #adding into list of lines for drawlines loop and resets corner lists (list1)
                list1.append(player.center)
                linelist.append(list1)
                pygame.draw.lines(window,(255,255,255),False, list1)
                s2 = floodFill(window, (list1[-1][0]+1, list1[-1][1]+1 ) )
                if s2 == None:
                    s2 = floodFill(window, (list1[-1][0]-1, list1[-1][1]+1 ) )
                somethingfilled = True
                list1 = []
                trail =[]
                rightdir = False
                leftdir = False
                downdir = False
                updir = False


        if somethingfilled:
            s2.blit( QIXMASK, (qix.centerx, qix.centery))
        window.blit(PLAYER, (player.x, player.y))
        

        l = window.get_at((spark.centerx-sparx_speed,spark.centery))[:3] == WHITE
        r = window.get_at((spark.centerx+sparx_speed,spark.centery))[:3] == WHITE
        u = window.get_at((spark.centerx,spark.centery-sparx_speed))[:3] == WHITE
        d = window.get_at((spark.centerx,spark.centery+sparx_speed))[:3] == WHITE
        enemyspark(spark,l,r,u,d)
        
        if len(list1) > 0 & (field == BLACK) :
            if spark.collidepoint(list1[0]):
                resetPlayer()
        if player.colliderect(spark) & (field == WHITE):
            resetPlayer()
            #lives -= 1
        
        '''
        #qix player collision
        if qix.colliderect(player):
            resetPlayer()
        '''
        #qix boundary collision
        
        for i in range(1,6):

            s = [-1,1]
            sign = random.choice(s)
            if window.get_at((qix.centerx + i, qix.centery )) != BLACK:
                qix_speed[0] = -qix_speed[0]
            elif window.get_at((qix.centerx -i, qix.centery )) != BLACK: 
                qix_speed[0] = -qix_speed[0]
            if window.get_at((qix.centerx, qix.centery -i )) != BLACK:
                qix_speed[1] = -qix_speed[1]
            elif window.get_at((qix.centerx, qix.centery +i )) != BLACK: 
                qix_speed[1] = -qix_speed[1]
                


        qix.centerx += qix_speed[0]
        qix.centery += qix_speed[1]             #movement for qix
        window.blit(qixee, qix)
        window.blit(PLAYER,(player.x,player.y))
        window.blit(SPARK,(spark.x,spark.y))
        show_score(textX,textY)
        pygame.display.update()
        

        #win screen 
        
        if TOTALFILLED >= WINTHRESHOLD:
            window.blit(s2, (0,0))
            show_score(textX,textY)
            message = font.render("YOU WIN!", True, (0,255,0))
            message2 = font.render("press Q to exit", True, (0,255,0) )
            window.blit(message,(335, 325))
            window.blit(message2,(285, 375))
            pygame.display.update()
            while True:
                for event in pygame.event.get():
                    if event.type ==  pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            pygame.quit()
                            sys.exit()

       
    pygame.quit()
main()