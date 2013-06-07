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
# Version 0.4
#
#    - Updated Render class
#        -> Updated button render function
#        -> Updated slot machine render function
#        -> Added draw component function (checks class name and draws corresponding render function)
#
#    - Added threading for button even handling
#    - Added Event Handler object
#        -> run method implemented
# 
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------


#I - Import and initialize
import pygame
import threading
import utility 

class ButtonEventHandler(threading.Thread):
    
    def __init__(self, buttonRef):
        self.__buttonRef = buttonRef
        self.__isRunning = True
        self.__meta__buttonX = self.__buttonRef.getX()
        
                    mousePos = pygame.mouse.get_pos()
            buttonX = self.__buttonRef.getX()
            buttonY = self.__buttonRef.getY()
            buttonWidth = self.__buttonRef.getWidth()
            buttonHeight = self.__buttonRef.getHeight()
        
    def run(self):
        while self.__isRunning:
            pygame.time.wait(1)

            if mousePos[0] >= buttonX && mousePos[0] <= buttonX + buttonWidth &&
               mousePos[0] >= buttonX && mousePos[0] <= buttonX + buttonWidth
    

class Button:

    def __init__(self, x, y, width, height, text, imgRef):
        self.__x = x
        self.__y = y
        self.__imgRef = imgRef
        self.__text = text
        self.__width = width
        self.__height = height
        self.__eventhandler = ButtonEventHandler()
        self.__eventhandler.start()

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
        
    def getImage(self):
        return self.__imgRef
    
    def changeImage(self, imgRef):
        self.____imgRef = imgRef
        
    def getText(self):
        return self.__text
    
    def changeText(self, text):
        self.__text = text

    def getSize(self):
        return self.getWidth(), self.getHeight()
    
    def getWidth(self):
        return self.__width
        
    def getHeight(self):
        return self.__height
    
    @staticmethod
    def isPressed
class Render:
    @staticmethod
    def draw_button(destination, button):
        destination.blit(button.getImage(), (button.getX(), button.getY()))
        myfont = pygame.font.SysFont(None, 24)
        label = myfont.render(button.getText(), True, (0, 0, 0))
        labeldims = myfont.size(button.getText())
        destination.blit(label, (button.getX() + button.getWidth() / 2 - labeldims[0] / 2,
                                 button.getY() + button.getHeight() / 2 - labeldims[1] / 2))
    
    @staticmethod
    def draw_component(destination, component):
        if component.__class__.__name__ == 'Button':
            Render.draw_button(destination, component)
            
            
    @staticmethod    
    def draw_slotmachine(destination, slotmachine):
        # Draw Slot Machine Interface
        destination.blit(slotmachine.getImage(), (0,0))        
        # Draw slot machine components
        for component in slotmachine.getComponents():
            Render.draw_component(destination, component)
            
    
    
class Resource:
    normalReel = None
    blurReel = None
    slotMachine = None
    

    redButton = None
    blueButton = None
    greenButton = None
    purpleButton = None
    
    
class SlotMachine:
    def __init__(self, imgRef):
        self.__imgRef = imgRef
        self.__components = []
        
    def getImage(self):
        return self.__imgRef
    
    def setImage(self, imgRef):
        self.__imgRef = imgRef
        
    def addComponent(self, component):
        self.__components.append(component)
        
    def getComponentAtReference(self, component):
        return self.__components[component]
    
    def getComponentAtIndex(self, index):
        return self.__components.index(index)
    
    def getComponents(self):
        return self.__components
    
    
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
    Resource.slotMachine = pygame.image.load('imgs/slot_machine.png')
    
    Resource.redButton = pygame.image.load('imgs/red_button.png')
    Resource.blueButton = pygame.image.load('imgs/blue_button.png')
    Resource.greenButton = pygame.image.load('imgs/green_button.png')
    Resource.purpleButton = pygame.image.load('imgs/purple_button.png')
    
    # Initialize the Slot Machine
    slotmachine = SlotMachine(Resource.slotMachine)
    slotmachine.addComponent(Button(630, 50, 60, 60, 'Quit', Resource.redButton))
    slotmachine.addComponent(Button(731, 52, 60, 60, 'Reset', Resource.redButton))
    slotmachine.addComponent(Button(300, 400, 60, 60, 'Spin', Resource.greenButton))
    
    return slotmachine, screen, fps


def deinit():
    pygame.quit()
    

def update():
    print 's'
    
    
def render(screen, slotmachine):
    Render.draw_slotmachine(screen, slotmachine)

   
   
def main():
    
    slotmachine, screen, fps = init()

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
        render(screen, slotmachine)        
        pygame.display.flip()
        
            

    deinit()



            

if __name__ == "__main__": main()
            
