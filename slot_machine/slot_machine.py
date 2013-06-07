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
#
# Version 0.1:
#
#    - Added utility module (for configuration file access)
#    - Added resource class
#    - Added init function
#        -> Loads from configuration file
#        -> Displays pygame window
#        -> Loads some of the images use for the interface
#    - Added deinitialize, update, and render functions (mostly unimplemented, render function draws interface image)
#    - Added main function, runs and executes the game.
#
# Version 0.2
#
#    - Added color button images (without text)
#    - Added Button class
#        -> x y coordinates - mutator + accessor
#        -> img reference accessor
#
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------


#I - Import and initialize
import pygame
import utility 

class Button:

    def __init__(self, x, y, img_ref):
        self.__x = x
        self.__y = y
        self.__img_ref = img_ref

    def getX(self):
        return self.__x
    
    def getY(self):
        return self.__y
    
    def setPosition(self, x, y):
        self.setX(x)
        self.setY(y)
        
    def setX(self, x):
        self.__x = x
   
        
    def setY(self, y):
        self.__y = y
        
    def getImageReference(self):
        return self.__img_ref
    
    
class Resource:
    normalReel = None
    blurReel = None
    slotMachine = None
    

    redButton = None
    blueButton = None
    greenButton = None
    purpleButton = None
    
    
def init():
    
    pygame.init()    
    utility.init()    

    # Load Settings via Configuration File 
    utility.set_config_file('config/config.cfg')
    
    width = int(utility.get_config_value('width', 640))
    height = int(utility.get_config_value('height', 480))
    depth = int(utility.get_config_value('depth', 0))
    mode = int(utility.get_config_value('mode', 0))
    title = utility.get_config_value('title', '')
    fps = float(utility.get_config_value('fps', 30.0))
    
    screen = pygame.display.set_mode([width, height], mode, depth)
    pygame.display.set_caption(title)

    Resource.normalReel = pygame.image.load('imgs/reel_normal.png')
    Resource.blurReel = pygame.image.load('imgs/reel_blur.png')
    Resource.slotMachine = pygame.image.load('imgs/slot_machine.jpg')
    
    Resource.redButton = pygame.image.load('imgs/red_button.png')
    Resource.blueButton = pygame.image.load('imgs/blue_button.png')
    Resource.greenButton = pygame.image.load('imgs/green_button.png')
    Resource.purpleButton = pygame.image.load('imgs/purple_button.png')
    
    
    screen.blit(Resource.slotMachine, (0, 0))
    
    return screen, fps


def deinit():
    pygame.quit()
    

def update():
    print 's'
    
    
def render(screen):
    screen.blit(Resource.redButton, (610, 25))
    screen.blit(Resource.redButton, (690, 25))
   
   
def main():
    
    screen, fps = init()

    clock = pygame.time.Clock()
    keepGoing = True
    
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))

    while keepGoing:
        clock.tick(fps)
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                keepGoing = False
                
        update()        
        render(screen)        
        pygame.display.flip()
        
            

    deinit()



            

if __name__ == "__main__": main()
            
