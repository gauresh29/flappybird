"""
date 7 nov
auther gauresh
"""

from os import pipe
import random #for random number genarator
import sys #for exit programe
import pygame
from pygame.display import set_caption
from pygame.locals import * #basicpygame import

#Global variable for game
FPS =36
SCREENWIDTH = 289
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUNDY = SCREENHEIGHT * 0.8
GAME_SPRITE = {}
GAME_SOUND = {}
PLAYER = "gallery/sprites/bird.png"
BACKGROUND ="gallery/sprites/background.png"
PIPE = "gallery/sprites/pipe.png"
def welcomeScreen():
    """shows images on screen"""
    playerx = int(SCREENWIDTH/5)
    playery = int((SCREENHEIGHT - GAME_SPRITE['player'].get_height())/2)
    messagex = int((SCREENWIDTH - GAME_SPRITE['message'].get_width())/2)
    messagey = int(SCREENHEIGHT*0.13)
    basex = 0
    while True:
        for event in pygame.event.get():
            # if user clicks on cross button, close the game
            if event.type == QUIT or (event.type==KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            # If the user presses space or up key, start the game for them
            elif event.type==KEYDOWN and (event.key==K_SPACE or event.key == K_UP):
                return
            else:
                SCREEN.blit(GAME_SPRITE['background'], (0, 0))    
                SCREEN.blit(GAME_SPRITE['player'], (playerx, playery))    
                SCREEN.blit(GAME_SPRITE['message'], (messagex,messagey ))    
                SCREEN.blit(GAME_SPRITE['base'], (basex, GROUNDY))    
                pygame.display.update()
                FPSCLOCK.tick(FPS)
    
   

def mainGame():
    score = 0
    playerx = int(SCREENWIDTH/5)
    playery = int(SCREENWIDTH/2)
    Basex = 0

    #create 2 pipes blitting on screen
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    #list of the upper pipe
    upperPipes = [
        {'x':SCREENWIDTH+200, 'y':newPipe1[0]['y']},
        {'x':SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newPipe2[0]['y']},
    ]
    #list of the lower pipe
    lowerPipes = [
        {'x':SCREENWIDTH+200, 'y':newPipe1[1]['y']},
        {'x':SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newPipe2[1]['y']},
    ]

    
    pipeVelx =-4
    playerVely = -9
    playerMaxvely = 10
    playerMinVely = -8
    playerAccy = 1
    playerFlapAccv = -8 #velocity while flaping
    playerFlapped = False #it only true when bird is flapping
     
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.type == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN or (event.type == K_SPACE or event.type == K_UP):
                if playery>0:
                    playerVely = playerFlapAccv
                    playerFlapped = True
                    GAME_SOUND['wing'].play()

        crashTest = isCollide(playerx, playery, upperPipes, lowerPipes)
        #this function return true if player is crash
        if crashTest:
            return
        
        #check score
        playerMidPos = playerx + GAME_SPRITE['player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_SPRITE['pipe'][0].get_width()/2
            
            if pipeMidPos <= playerMidPos < pipeMidPos +4:
                score += 1
                print(f"your score is {score}")
                GAME_SOUND['point'].play()     
            if playerVely <playerMaxvely and not playerFlapped:
                playerVely += playerAccy
            if playerFlapped:
                playerFlapped = False
            playerHeight = GAME_SPRITE['player'].get_height()
            playery = playery + min(playerVely, GROUNDY - playery - playerHeight)

            #move pipe to left
            for upperPipe , lowerPipe in zip(upperPipes, lowerPipes):
                upperPipe['x'] += pipeVelx
                lowerPipe['x'] += pipeVelx
            
            #Add new pipe when first pipe will be disapear
            if 0<upperPipes[0]['x']<5:
                newpipe = getRandomPipe()
                upperPipes.append(newpipe[0])
                lowerPipes.append(newpipe[1])
            #if pipe out of range just rempove it
            if upperPipes[0]['x'] < -GAME_SPRITE['pipe'][0].get_width():
                upperPipes.pop(0)
                lowerPipes.pop(0) 
            
            #lets blits our sprites now
            SCREEN.blit(GAME_SPRITE['background'],(0,0))
            for upperPipe , lowerPipe in zip(upperPipes, lowerPipes):
                SCREEN.blit(GAME_SPRITE['pipe'][0],(upperPipe['x'],upperPipe['y']))
                SCREEN.blit(GAME_SPRITE['pipe'][1],(lowerPipe['x'],lowerPipe['y']))
            SCREEN.blit(GAME_SPRITE['base'],(Basex,GROUNDY))
            SCREEN.blit(GAME_SPRITE['player'],(playerx,playery))
            myDigits = [int(x) for x in list(str(score))]
            width = 0
            for digit in myDigits:
                width += GAME_SPRITE['numbers'][digit].get_width()

            Xoffset = (SCREENWIDTH - width)/2

            for digit in myDigits:
                SCREEN.blit(GAME_SPRITE['numbers'][digit],(Xoffset, SCREENHEIGHT*0.10))
                Xoffset += GAME_SPRITE['numbers'][digit].get_width()
            pygame.display.update()
            FPSCLOCK.tick(FPS)
            

def isCollide(playerx, playery, upperPipe, lowerPipe):
    if playery > GROUNDY -25 or playery <0:
        GAME_SOUND['hit'].play()
        return True
    for pipe in upperPipe:
        pipeHeight = GAME_SPRITE['pipe'][0].get_height()
        if(playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITE['pipe'][0].get_width()):
            GAME_SOUND['hit'].play()
            return True

    for pipe in lowerPipe:
        if (playery + GAME_SPRITE  ['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < GAME_SPRITE['pipe'][0].get_width():
            GAME_SOUND['hit'].play()
            return True


    return False
    
def getRandomPipe():
    """
    Generate random position of two pipe(one bottom straight and one top rotted ) blitting on screen
    """
    pipeHeight = GAME_SPRITE['pipe'][0].get_height()
    
    offset = SCREENHEIGHT/3
    y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAME_SPRITE['base'].get_height() - 1.2 * offset))
    pipex = SCREENWIDTH +10
    y1 = pipeHeight -y2 + offset
    pipe = [
        {'x':pipex, 'y': -y1}, #upper pipe
        {'x':pipex, 'y': y2}#lower pipe
    ]
    return pipe

if __name__ == "__main__":
    # this will be the main point where our game will start
    pygame.init() #initialise all pygame module
    FPSCLOCK = pygame.time.Clock()
    pygame.display,set_caption("FLAPPY BIRD GAME BY GAURESH")
    GAME_SPRITE['numbers'] = (
        pygame.image.load("gallery/sprites/0.png").convert_alpha(),
        pygame.image.load("gallery/sprites/1.png").convert_alpha(),
        pygame.image.load("gallery/sprites/2.png").convert_alpha(),
        pygame.image.load("gallery/sprites/3.png").convert_alpha(),
        pygame.image.load("gallery/sprites/4.png").convert_alpha(),
        pygame.image.load("gallery/sprites/5.png").convert_alpha(),
        pygame.image.load("gallery/sprites/6.png").convert_alpha(),
        pygame.image.load("gallery/sprites/7.png").convert_alpha(),
        pygame.image.load("gallery/sprites/8.png").convert_alpha(),
        pygame.image.load("gallery/sprites/9.png").convert_alpha(),
    ) 
    #print(GAME_SPRITE)
    GAME_SPRITE['message'] = pygame.image.load("gallery/sprites/message.png")
    GAME_SPRITE['base'] = pygame.image.load("gallery/sprites/base.png")
    GAME_SPRITE['pipe'] =(pygame.transform.rotate(pygame.image.load( PIPE).convert_alpha(), 180), 
    pygame.image.load(PIPE).convert_alpha()
    )


    #GAME SOUND
    GAME_SOUND['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
    GAME_SOUND['point'] = pygame.mixer.Sound('gallery/audio/point.wav')
    GAME_SOUND['swoosh'] = pygame.mixer.Sound('gallery/audio/swoosh.wav')
    GAME_SOUND['die'] = pygame.mixer.Sound('gallery/audio/die.wav')
    GAME_SOUND['wing'] = pygame.mixer.Sound('gallery/audio/wing.wav')

    GAME_SPRITE['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_SPRITE['player'] = pygame.image.load(PLAYER).convert_alpha()

    while True:
    
        welcomeScreen() #shows user main screen until he press button
        mainGame()
        #this is main game function
