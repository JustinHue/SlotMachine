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
# Version 0.6
#
#    - Added state constants to ButtonEventHandler and a field variable to keep track of the state.
#      This also fixes any issues if two different buttons are set to the same event handler callback routine.
#    - Added flags for release, hover, etc.
#    - Added isHovering, isPressed methods
#    - Added enable attribute to button class
#
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------


#I - Import and initialize
import pygame
import threading
import utility 


class Resource:
    normalReel = None
    blurReel = None
    slotMachine = None
    

    redButton = None
    blueButton = None
    greenButton = None
    purpleButton = None
    
    
class ExEventHandler:
    @staticmethod
    def button_hover_listener(button, hover_state, x, y):
        if hover_state:
            button.changeImage(Resource.purpleButton)
            pygame.mouse.set_cursor(*pygame.cursors.diamond)
        else:
            button.changeImage(Resource.redButton)
            pygame.mouse.set_cursor(*pygame.cursors.arrow)

            
        
    @staticmethod
    def button_release_listener(button, m1, m2, m3, x, y):
        button.changeWidth(60)
        button.changeHeight(60)        


    @staticmethod
    def button_press_listener(button, m1, m2, m3, x, y):
        button.changeWidth(55)
        button.changeHeight(55)


    @staticmethod
    def spin_button_hover_listener(button, hover_state, x, y):
        if button.isEnabled():
            if hover_state:
                button.changeImage(Resource.redButton)
                pygame.mouse.set_cursor(*pygame.cursors.diamond)
            else:
                button.changeImage(Resource.greenButton)
                pygame.mouse.set_cursor(*pygame.cursors.arrow)

            
        
    @staticmethod
    def spin_button_release_listener(button, m1, m2, m3, x, y):
        button.changeWidth(60)
        button.changeHeight(60)        


    @staticmethod
    def spin_button_press_listener(button, m1, m2, m3, x, y):
        button.changeWidth(55)
        button.changeHeight(55)


         
class ButtonEventHandler(threading.Thread):
    
    def __init__(self, buttonRef):
        threading.Thread.__init__(self)

        self.__buttonRef = buttonRef
        self.__isRunning = True
        # Add meta data for quick referencing on the button for better performance.        
        self.__meta__buttonX = self.__buttonRef.getX()
        self.__meta__buttonY = self.__buttonRef.getY()
        self.__meta__buttonWidth = self.__buttonRef.getWidth()
        self.__meta__buttonHeight = self.__buttonRef.getHeight()

        self.__hover = False
        self.__pressed = False
        
        
    def run(self):
        while self.__isRunning:
            pygame.time.wait(1)

            mousePos = pygame.mouse.get_pos()
            
            if mousePos[0] >= self.__meta__buttonX and \
            mousePos[0] <= self.__meta__buttonX + self.__meta__buttonWidth and \
            mousePos[1] >= self.__meta__buttonY and \
            mousePos[1] <= self.__meta__buttonY + self.__meta__buttonHeight:
            
                self.__hover = True
                
                self.__buttonRef.getOnHoverListener()(self.__buttonRef, True, mousePos[0], mousePos[1])
                mousePress = pygame.mouse.get_pressed()

                if mousePress[0]:
                    self.__buttonRef.getOnPressListener()(self.__buttonRef, mousePress[0], mousePress[1], 
                                                          mousePress[2], mousePos[0], mousePos[1])
                    self.__pressed = True
                elif self.__pressed: 
                    self.__buttonRef.getOnReleaseListener()(self.__buttonRef, mousePress[0], mousePress[1], 
                                                            mousePress[2], mousePos[0], mousePos[1])
                    self.__pressed = False
                    
            elif self.__hover:
                self.__buttonRef.getOnHoverListener()(self.__buttonRef, False, mousePos[0], mousePos[1])
                self.__pressed = False
                self.__buttonRef.getOnReleaseListener()(self.__buttonRef, mousePress[0], mousePress[1], 
                                                        mousePress[2], mousePos[0], mousePos[1])                
                self.__hover = False
               
    def isHovering(self):
        return self.__hover
    
    def isPressed(self):
        return self.__pressed


    
class Button:

    def __init__(self, x, y, width, height, text, imgRef):
        self.__x = x
        self.__y = y
        self.__imgRef = imgRef
        self.__text = text
        self.__width = width
        self.__height = height
        self.__eventthread = ButtonEventHandler(self)

        self.__enabled = True
        
        # Event listeners
        self.__hoverEventListener = None
        self.__pressEventListener = None
        self.__releaseEventListener = None
        
        self.__eventthread.start()
        
    def isEnabled(self):
        return self.__enabled
    
    def enable(self, boolean):
        self.__enabled = boolean
        
    def isHovering(self):
        return self.__eventthread.isHovering()
    
    def isPressed(self):
        return self.__eventthread.isPressed()
    
    
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
        self.__imgRef = imgRef
        
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
    
    def changeWidth(self, width):
        self.__width = width
        
    def changeHeight(self, height):
        self.__height = height
        
    def setOnHoverListener(self, eventListener):
        self.__hoverEventListener = eventListener
        
    def setOnPressListener(self, eventListener):
        self.__pressEventListener = eventListener
        
    def setOnReleaseListener(self, eventListener):
        self.__releaseEventListener = eventListener
        
    def getOnHoverListener(self):
        return self.__hoverEventListener
        
    def getOnPressListener(self):
        return self.__pressEventListener
    
    def getOnReleaseListener(self):
        return self.__releaseEventListener

        
class Render:
    @staticmethod
    def draw_button(destination, button):
        scaleImage = pygame.transform.scale(button.getImage(), (button.getWidth(),button.getHeight()))
        destination.blit(scaleImage, (button.getX(), button.getY()))
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
        return self.__components[index]
    
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
    quitButton = Button(630, 50, 60, 60, 'Quit', Resource.redButton)
    quitButton.setOnHoverListener(ExEventHandler.button_hover_listener)
    quitButton.setOnPressListener(ExEventHandler.button_press_listener)
    quitButton.setOnReleaseListener(ExEventHandler.button_release_listener)
    slotmachine.addComponent(quitButton)
    
    resetButton = Button(731, 52, 60, 60, 'Reset', Resource.redButton)
    resetButton.setOnHoverListener(ExEventHandler.button_hover_listener)
    resetButton.setOnPressListener(ExEventHandler.button_press_listener)
    resetButton.setOnReleaseListener(ExEventHandler.button_release_listener)
    slotmachine.addComponent(resetButton)
       
    spinButton = Button(420, 495, 60, 60, 'Spin', Resource.greenButton)
    spinButton.setOnHoverListener(ExEventHandler.spin_button_hover_listener)
    spinButton.setOnPressListener(ExEventHandler.spin_button_press_listener)
    spinButton.setOnReleaseListener(ExEventHandler.spin_button_release_listener)
    slotmachine.addComponent(spinButton)

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
            
