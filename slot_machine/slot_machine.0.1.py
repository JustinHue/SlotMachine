#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
# Source File: slow_machine.0.1.py
# Author Name: Justin Hellsten
# Last Modified By: Justin Hellsten
# Last Modified Date: June 6, 2013
#
# Program Description: 
#
#        This is a slot machine game.
#        to pick a choice for every node (1 or 2). Which decision you can do will be described by
#        the game and all the user has to do is input 1 or 2 for the appropriate decision. There will
#        be 8 outcomes, where only 1 will be the good outcome. I hope you enjoy this game and I hope to
#        improve it more on my free time.
#
# Version 0.1:
#
#
#
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------


#I - Import and initialize
import pygame
import utility

utility.init()
utility.set_config_file('config/config.cfg')

print utility.get_config_value('width', 100)


pygame.init()
#D - Display configuration
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Hello, world!")
#E - Entities (just background for now)
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((0, 255, 255))
#A - Action (broken into ALTER steps)

#A - Assign values to key variables
clock = pygame.time.Clock()
keepGoing = True
#L - Set up main loop
while keepGoing:
    #T - Timer to set frame rate
    clock.tick(30)

    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            keepGoing = False
            #R - Refresh display 
            screen.blit(background, (0, 0)) 
            pygame.display.flip()
            
            
