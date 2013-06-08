#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
# Source File: slow_machine.0.1.py
# Author Name: Justin Hellsten
# Last Modified By: Justin Hellsten
# Last Modified Date: June 6, 2013
#
# Program Description: 
#
#        This is a slot machine game made by Justin Hellsten. In this slot machine game the player is allowed to choose between 
#        bet levels 1, 2, 5, 10, 25, 50, 100 and the reel options include: Orange, Pear, Banana, Cherry, Bar, and Seven. 
#        The slot machine will animate for every reel when the the spin button is pressed. There is also a reset and quit button at
#        the top right.
#        
#
# Revision History:
#
# Version 0.8
#
#    - Removing Reels class. Instead using variables in Slot Machine class to define reel outcome
#    - Cropped reels for default position
#    - Added spinning animation for all 5 reels, each progressive reel gets faster
#    - Now updates credits based on results
#    - Fixed reels so that they don't display result right away when animating
#    - Fixed reset button
#    - Added jackpot message
#
# Version 0.7
#
#    - Removed threading for event handler due to conflicts with pygame
#    - Added poll components method for slot machine to sync component
#    events with main loop
#    - Added shutdown method for slotmachine
#    - Made Reset and Exit button actually work
#    - bet amount and credits now render
#    - Bet amount ranges between 1, 2, 5, 10, 25, 50, 100
#    - Greyed out spin button if bet amount exceeds credit amount
#    - Started implementing reels
#    - Added slot_machine_brain module for easy referencing. Might not
#    use exact code.
#
# Version 0.6
#
#    - Added state constants to ButtonEventHandler and a field variable
#    to keep track of the state.
#      This also fixes any issues if two different buttons are set to
#    the same event handler callback routine.
#    - Added flags for release, hover, etc.
#    - Added isHovering, isPressed methods
#    - Added enable attribute to button class
#
#
# Version 0.5
#
#    - Added meta data on ButtonEventHandler for quick referencing on
#    the button
#    - Added state listeners on the button object (e.g hover, press, release)
#    - Changed run method on ButtonEventHandler to execute event listeners
#    - Added static class ExEventHandler (a storage place for our event handler functions)
#        -> quit_button_hover_listener(), quit_button_release_listener(), quit_button_press_listener()
#        -> reset_button_hover_listener(), reset_button_release_listener(), reset_button_press_listener()
#    - Made the buttons scale and work with even listeners
#
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
#
# Version 0.3
#
#    - Added text field to button, set and get methods
#    - Added new class called slot machine.
#        -> Can add and extract components
#        -> Can access or change slot machine image
#
#
# Version 0.2
#    - Added color button images (without text)
#    - Added Button class
#        -> x y coordinates - mutator + accessor
#        -> img reference accessor
#
# Version 0.1
#    - Added utility module (for configuration file access)
#    - Added resource class
#    - Added init function
#        -> Loads from configuration file
#        -> Displays pygame window
#        -> Loads some of the images use for the interface
#    - Added deinitialize, update, and render functions (mostly unimplemented, render function draws interface image)
#    - Added main function, runs and executes the game.
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------


#Import and initialize
import pygame
import utility 
import random

# Global Vars
global slotmachine
        
class Resource:
    """
        Class: Resource
        Description: The purpose of this class is to serve as a space for game resources, many include images, and game constants.
    """
    
    #Images
    blurReel = None
    slotMachine = None
    redButton = None
    blueButton = None
    greenButton = None
    purpleButton = None
    blackButton = None
    
    #Other essential game definitions (bets, outcomes, etc)
    betAmountOptions = [1, 2, 5, 10, 25, 50, 100]
    outcomePositions = ['Orange', 'Banana', 'Pear', 'Cherry', 'Seven', 'Bar']
    animatingline = [' ', ' ', ' ', ' ', ' ']
    
class ExEventHandler:
    """
        Class: ExEventHandler
        Description: This class holds all event listener functions which are used for the button widgets on the slot machine.
                     Various buttons that need event listeners include bet, spin, exit, reset...
    """
    @staticmethod
    def bet_button_hover_listener(button, hover_state, x, y):
        if hover_state:
            button.changeImage(Resource.redButton)
            pygame.mouse.set_cursor(*pygame.cursors.diamond)
        else:
            button.changeImage(Resource.blueButton)
            pygame.mouse.set_cursor(*pygame.cursors.arrow)            
        
    @staticmethod
    def bet_button_release_listener(button, m1, m2, m3, x, y):
        global slotmachine
        button.changeWidth(60)
        button.changeHeight(60)     
        newBetOption = Resource.betAmountOptions.index(slotmachine.getBetAmount()) + 1
        if newBetOption < len(Resource.betAmountOptions):
            slotmachine.changeBet(Resource.betAmountOptions[newBetOption])
        else:
            slotmachine.changeBet(Resource.betAmountOptions[0])

    @staticmethod
    def bet_button_press_listener(button, m1, m2, m3, x, y):
        button.changeWidth(55)
        button.changeHeight(55)


    @staticmethod
    def quit_button_hover_listener(button, hover_state, x, y):
        if hover_state:
            button.changeImage(Resource.purpleButton)
            pygame.mouse.set_cursor(*pygame.cursors.diamond)
        else:
            button.changeImage(Resource.redButton)
            pygame.mouse.set_cursor(*pygame.cursors.arrow)

            
        
    @staticmethod
    def quit_button_release_listener(button, m1, m2, m3, x, y):
        global slotmachine
        button.changeWidth(60)
        button.changeHeight(60)    
        slotmachine.shutdown()    
        
    @staticmethod
    def quit_button_press_listener(button, m1, m2, m3, x, y):
        button.changeWidth(55)
        button.changeHeight(55)


    @staticmethod
    def reset_button_hover_listener(button, hover_state, x, y):
        if hover_state:
            button.changeImage(Resource.purpleButton)
            pygame.mouse.set_cursor(*pygame.cursors.diamond)
        else:
            button.changeImage(Resource.redButton)
            pygame.mouse.set_cursor(*pygame.cursors.arrow)


    @staticmethod
    def reset_button_release_listener(button, m1, m2, m3, x, y):
        global slotmachine
        button.changeWidth(60)
        button.changeHeight(60)    
        if not slotmachine.isSpinning():
            slotmachine.setCreditAmount(100)
            slotmachine.changeBet(5)

    @staticmethod
    def reset_button_press_listener(button, m1, m2, m3, x, y):
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
        slotmachine.spin()


    @staticmethod
    def spin_button_press_listener(button, m1, m2, m3, x, y):
        global slotmachine
        button.changeWidth(55)
        button.changeHeight(55)
        

         
         
class ButtonEventHandler():
    """
        Class: ButtonEventHandler
        Description: I made my own event handler for buttons because pygame lacks a decent event control for widget like objects. I
                     could have used another game library but pygame I am more comfortable with. This class keeps all the event states
                     the button is in and MUST be run by the main looper using the button method poll
    """
    def __init__(self, buttonRef):

        self.__buttonRef = buttonRef
        # Add meta data for quick referencing on the button for better performance.        
        self.__meta__buttonX = self.__buttonRef.getX()
        self.__meta__buttonY = self.__buttonRef.getY()
        self.__meta__buttonWidth = self.__buttonRef.getWidth()
        self.__meta__buttonHeight = self.__buttonRef.getHeight()

        self.__hover = False
        self.__pressed = False

        
    def run(self):
        """
            The basis of the event handler. This method checks mouse collision via hover, press, and release. All
            listeners are called and maintained here. This method must be constantly executed to ensure the button
            is event handled. Usually done through the main loop.
        """
        pygame.time.wait(1)

        mousePos = pygame.mouse.get_pos()
        mousePress = pygame.mouse.get_pressed()
        
        if self.__buttonRef.isEnabled() == False:
            return
        
        if mousePos[0] >= self.__meta__buttonX and \
        mousePos[0] <= self.__meta__buttonX + self.__meta__buttonWidth and \
        mousePos[1] >= self.__meta__buttonY and \
        mousePos[1] <= self.__meta__buttonY + self.__meta__buttonHeight:
            
            self.__hover = True
                
            self.__buttonRef.getOnHoverListener()(self.__buttonRef, True, mousePos[0], mousePos[1])

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
            self.__hover = False
      
    def isHovering(self):
        return self.__hover
    
    def isPressed(self):
        return self.__pressed

    def stop(self):
        self.__isRunning = False
    
    

class Button:
    """
        Class: Button
        Description: The button class is a component for the slot machine. The button has an event handlers
        and listener references. I made the button from scratch dude to the lack of support from pygame.
    """
    
    def __init__(self, x, y, width, height, text, imgRef):
        self.__x = x
        self.__y = y
        self.__imgRef = imgRef
        self.__text = text
        self.__width = width
        self.__height = height
        self.__eventhandler = ButtonEventHandler(self)

        self.__enabled = True
        
        # Event listeners
        self.__hoverEventListener = None
        self.__pressEventListener = None
        self.__releaseEventListener = None

        
    def isEnabled(self):
        return self.__enabled
    
    def enable(self, boolean):
        self.__enabled = boolean
        
    def isHovering(self):
        return self.__eventhandler.isHovering()
    
    def isPressed(self):
        return self.__eventhandler.isPressed()
    
    
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

    def getEventHandler(self):
        return self.__eventhandler
    
        
class Render:
    @staticmethod
    def draw_button(destination, button):
        """
            Draws the button component using the reference image and it's text. The text
            is centered on the button.
        """
        scaleImage = pygame.transform.scale(button.getImage(), (button.getWidth(),button.getHeight()))
        destination.blit(scaleImage, (button.getX(), button.getY()))
        myfont = pygame.font.SysFont(None, 24)
        label = myfont.render(button.getText(), True, (0, 0, 0))
        labeldims = myfont.size(button.getText())
        destination.blit(label, (button.getX() + button.getWidth() / 2 - labeldims[0] / 2,
                                 button.getY() + button.getHeight() / 2 - labeldims[1] / 2))
         
    
    @staticmethod
    def draw_component(destination, component):
        """
            Draws a component of the slot machine. The only component at the moment is a Button.
        """
        if component.__class__.__name__ == 'Button':
            Render.draw_button(destination, component)
            
            
    @staticmethod
    def draw_slotmachine(destination, slotmachine):
        """
            Renders the slot machine entirely. Slot machine interface, labels, and reels.
        """
    
        # Draw Slot Machine Interface
        destination.blit(slotmachine.getImage(), (0,0))        
        # Draw slot machine components
        
        for component in slotmachine.getComponents():
            Render.draw_component(destination, component)
            
        # Draw all labels (E.G credit, bet...)
        myfont = pygame.font.SysFont(None, 46)
        label = myfont.render(str(slotmachine.getCreditAmount()), True, (255, 255, 255))            
        destination.blit(label, (50, 480))
   
        label = myfont.render(str(slotmachine.getBetAmount()), True, (255, 255, 255))            
        destination.blit(label, (560, 480))
    
        label = myfont.render(str(slotmachine.getWinnings()), True, (255, 255, 255))            
        destination.blit(label, (650, 480))
        
        if slotmachine.jackpot():
            label = myfont.render(str("JACKPOT!"), True, (255, 0, 0))            
            destination.blit(label, (330, 65))
        
        # Determine reel output when animating...
        reelCount = 0
        reelSize = 300
        currentReel = slotmachine.getCurrentReel()
        currentSlotBetLine = slotmachine.getBetLine()
        
        if Resource.animatingline != slotmachine.getLastLine():
            Resource.animatingline = slotmachine.getLastLine()

        if Resource.animatingline[currentReel] != currentSlotBetLine[currentReel]:
            Resource.animatingline[currentReel] = currentSlotBetLine[currentReel]
        else:
            Resource.animatingline = slotmachine.getLastLine()

        # Draw reels
        for reelOutcome in Resource.animatingline:
            reelCopy = Resource.normalReel.copy()
            
            if currentReel == reelCount: 
                cropTop = pygame.transform.chop(reelCopy,
                                                     pygame.Rect(0, 0, 
                                                                 0, slotmachine.getRollingIndex() + 330 + Resource.outcomePositions.index(reelOutcome)*70))
                cropBottom = pygame.transform.chop(cropTop, pygame.Rect(0, reelSize, 0, 1000))
                destination.blit(cropBottom, (90 + reelCount * 138, 135))
            else:
                cropTop = pygame.transform.chop(reelCopy,
                                                     pygame.Rect(0, 0, 
                                                                 0, 330 + Resource.outcomePositions.index(reelOutcome)*70))
                cropBottom = pygame.transform.chop(cropTop, pygame.Rect(0, reelSize, 0, 1000))
                destination.blit(cropBottom, (90 + reelCount * 138, 135))
                
            reelCount += 1
            
class SlotMachine:
    """
        Class: SlotMachine
        Description: This is the main object for the slot machine game. The slot machine holds all the values, flags and components for
        the slot machine game. The main loop must interact using a slot machine object.
    """
    # Slot Machine Constants
    ANIMATION_SPEED = 50
    NUM_OF_REELS = 5
    NUMBER_OF_SPINS_PER_REEL = 3
    
    def __init__(self, imgRef):
        """
            Constructor for the slot machine... 
        """
        self.__imgRef = imgRef
        self.__components = []
        self.__credits = 100
        self.__betAmount = 5
        self.__isOn = True
        self.__outcome = [0,0,0,0,0]
        # [ FRUIT, FRUIT, FRUIT, FRUIT, FRUIT]
        self.__betline = ["Orange", "Orange", "Orange", "Orange", "Orange"]
        self.__lastline = list(self.__betline)
        
        self.__currentReel = 0
        self.__reelRolling = 0
        self.__countNumReelSpin = 0
        self.__spinning = False
        self.__winnings = 0
        self.__jackpot = False
        
    def jackpot(self):
        """ 
            A flag which determines if the player has gotten a jackpot with the slot machine.
        """
        return self.__jackpot
    
    def getImage(self):
        """
            Grabs the interface image of the slot machine.
        """
        return self.__imgRef
    
    def setImage(self, imgRef):
        """
            Sets/Changes the image of the slot machine. The image is the interface.
        """
        self.__imgRef = imgRef
        
    def addComponent(self, component):
        """
            Adds/Appends a component to the slot machine components list.
        """
        self.__components.append(component)
        
    def getComponentAtReference(self, component):
        """
            Grabs a component via reference.
        """
        return self.__components[component]

    def getComponentAtIndex(self, index):
        """
            Grabs the component via index.
        """
        return self.__components[index]
    
    def getComponents(self):
        """
            Grabs all the components on the slot machine.
        """
        return self.__components
    
    def pollComponents(self):
        """
            Loops through all the components and only finds button classes. If the component found is a button
            class the corresponding event handler run method is executed. This is need otherwise buttons on the slot machine
            would have no events.
        """
        for component in self.__components:
            if component.__class__.__name__ == 'Button':
                component.getEventHandler().run()
    
    def getCreditAmount(self):
        """
            Gets the credit value on the slot machine.
        """
        return self.__credits
    
    def getBetAmount(self):
        """
            Gets the current bet amount on the slot machine.
        """
        return self.__betAmount
    
    def changeBet(self, betAmount):
        """
            Changes the bet amount on the slot machine to pass args.
        """
        self.__betAmount = betAmount
        
    
    def isOn(self):
        """
            A shutdown flag used to determine if the slot machine has been turned off. This flag is set by the exit button.
        """
        return self.__isOn
    
    def shutdown(self):
        """
            This method shuts down the slot machine. The isOn flag is set.
        """
        self.__isOn = False
        
    def setCreditAmount(self, creditAmount):
        """
            Sets the credit amount to whatever is passed via argument.
        """
        self.__credits = creditAmount
        
    def getRollingIndex(self):
        """ ***
            Returns the rolling index, a counter for bliting the sprite sheet during rendering.
            This is a MUST have in order to have the animation render properly. If this doesn't exist
            the Render function for the slot machine will not animate.
        """
        return self.__reelRolling
    
    def isSpinning(self):
        """
            A flag determining the spin state of the slot machine.
        """
        return self.__spinning
    
    def animateSpin(self):
        """
            Figuratively animates the spinning action of the slot machine by changing inner private field variables.
            In order to render the animation the slot machine render method must be called in the Render class.
            The animation spin is based on the animation speed and the height of the reel spritesheet (454).
            The current reel is updated and the spin checking is called here at the end of the animation.
        """
        self.__reelRolling += SlotMachine.ANIMATION_SPEED
        
        if self.__reelRolling >= 454:
            self.__reelRolling = 0
            self.__countNumReelSpin += 1
            
        if self.__countNumReelSpin == SlotMachine.NUMBER_OF_SPINS_PER_REEL:
            self.__currentReel += 1
            self.__countNumReelSpin = 0
            
        if self.__currentReel == SlotMachine.NUM_OF_REELS:
            self.__spinning = False
            self.checkSpin()
            self.__lastline = list(self.__betline)
            self.__currentReel = 0
            
    def getCurrentReel(self):
        """
            Returns the current reel when the slot machine is spinning. This is
            important for when the slot machine is rendered.
        """
        return self.__currentReel
        
    
    def spin(self):
        """
            Spins the reels of the slot machine and gives an outcome.
        """
        # Make the bet
        self.__spinning = True
        self.__credits -= self.__betAmount
        
        for spin in range(5):
            self.__outcome[spin] = random.randrange(1,100,1)
            # Spin those Reels!
            if self.__outcome[spin] >= 1 and self.__outcome[spin] <= 34:  # 35.00% Chance
                self.__betline[spin] = "Orange"
            if self.__outcome[spin] >= 35 and self.__outcome[spin] <=59:  # 25.00% Chance
                self.__betline[spin] = "Banana"
            if self.__outcome[spin] >= 60 and self.__outcome[spin] <=79:  # 20.00% Chance
                self.__betline[spin] = "Pear"
            if self.__outcome[spin] >= 80 and self.__outcome[spin] <=91:  # 12.00% Chance
                self.__betline[spin] = "Cherry"
            if self.__outcome[spin] >= 92 and self.__outcome[spin] <=99:  # 7.00%  Chance
                self.__betline[spin] = "Bar"
            if self.__outcome[spin] >= 100:                               # 1.00%  Chance
                self.__betline[spin] = "Seven"
 
    def getWinnings(self):
        """
            Determines the winnings on the slot machine
        """
        return self.__winnings
    
    
    def checkSpin(self):
        """
            Used to check the results of the reels when the spin() method is activated.
            5, 4, and 3 lines of any outcome is checked and the winnings is updated based on the hardest
            match.
        """
        self.__winnings = 0
        self.__jackpot = False
        
        # Match 5
        if self.__betline.count("Orange") == 5:
            self.__winnings = self.__betAmount*15
        elif self.__betline.count("Banana") == 5:
            self.__winnings = self.__betAmount*25
        elif self.__betline.count("Pear") == 5:
            self.__winnings = self.__betAmount*50
        elif self.__betline.count("Cherry") == 5:
            self.__winnings = self.__betAmount*100
        elif self.__betline.count("Bar") == 5:
            self.__winnings = self.__betAmount*250
        elif self.__betline.count("Seven") == 5:
            self.__winnings = self.__betAmount*500
            self.__jackpot = True
    
            
        # Match 4
        elif self.__betline.count("Orange") == 4:
            self.__winnings = self.__betAmount*10
        elif self.__betline.count("Banana") == 4:
            self.__winnings = self.__betAmount*17
        elif self.__betline.count("Pear") == 4:
            self.__winnings = self.__betAmount*33
        elif self.__betline.count("Cherry") == 4:
            self.__winnings = self.__betAmount*66
        elif self.__betline.count("Bar") == 4:
            self.__winnings = self.__betAmount*166
        elif self.__betline.count("Seven") == 4:
            self.__winnings = self.__betAmount*500
            
        # Match 3
        elif self.__betline.count("Orange") == 3:
            self.__winnings = self.__betAmount*7
        elif self.__betline.count("Banana") == 3:
            self.__winnings = self.__betAmount*11
        elif self.__betline.count("Pear") == 3:
            self.__winnings = self.__betAmount*23
        elif self.__betline.count("Cherry") == 3:
            self.__winnings = self.__betAmount*44
        elif self.__betline.count("Bar") == 3:
            self.__winnings = self.__betAmount*110
        elif self.__betline.count("Seven") == 3:
            self.__winnings = self.__betAmount*250
            
        
        self.__credits += self.__winnings
        
        
    def stopSpin(self):
        """
            A boolean return that says if the slot machine has stopped spinning.
        """
        self.__spinning = False
        
        
    def getBetLine(self):
        """
            Returns the bet line list. The list is 5 outcomes long (e.g [FRUIT, FRUIT, FRUIT, FRUIT, FRUIT]
        """
        return self.__betline
    
    def getLastLine(self):
        return self.__lastline

        
def init():
    """
        Initialize pygame, utility, and the game (slot machine). The game is installed by grabbing
        config values from the configuration file. All buttons images are loaded into the Resource class
        and the event handler functions are set.
    """
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
    Resource.blackButton = pygame.image.load('imgs/black_button.png')
    
    # Initialize the Slot Machine
    slotmachine = SlotMachine(Resource.slotMachine)
    quitButton = Button(630, 50, 60, 60, 'Quit', Resource.redButton)
    quitButton.setOnHoverListener(ExEventHandler.quit_button_hover_listener)
    quitButton.setOnPressListener(ExEventHandler.quit_button_press_listener)
    quitButton.setOnReleaseListener(ExEventHandler.quit_button_release_listener)
    slotmachine.addComponent(quitButton)
    
    resetButton = Button(731, 52, 60, 60, 'Reset', Resource.redButton)
    resetButton.setOnHoverListener(ExEventHandler.reset_button_hover_listener)
    resetButton.setOnPressListener(ExEventHandler.reset_button_press_listener)
    resetButton.setOnReleaseListener(ExEventHandler.reset_button_release_listener)
    slotmachine.addComponent(resetButton)
       
    spinButton = Button(420, 495, 60, 60, 'Spin', Resource.greenButton)
    spinButton.setOnHoverListener(ExEventHandler.spin_button_hover_listener)
    spinButton.setOnPressListener(ExEventHandler.spin_button_press_listener)
    spinButton.setOnReleaseListener(ExEventHandler.spin_button_release_listener)
    slotmachine.addComponent(spinButton)

    betButton = Button(320, 495, 60, 60, 'Bet', Resource.blueButton)
    betButton.setOnHoverListener(ExEventHandler.bet_button_hover_listener)
    betButton.setOnPressListener(ExEventHandler.bet_button_press_listener)
    betButton.setOnReleaseListener(ExEventHandler.bet_button_release_listener)
    slotmachine.addComponent(betButton)
    
    return slotmachine, screen, fps


    

def update(slotmachine):
    """
        This function updates the slot machine. Widget event handling is executed using the pollComponents method. Also
        the slot machine's bet/credits is checked. If it is going below 0 than the spin button is disabled.
    """
    slotmachine.pollComponents()
    button = slotmachine.getComponentAtIndex(2) 
    if slotmachine.getCreditAmount() - slotmachine.getBetAmount() < 0:
        button.enable(False)
        button.changeImage(Resource.blackButton)
    else:
        button.enable(True)
        button.changeImage(Resource.greenButton)
    
    
            
def render(screen, slotmachine):
    """
        This function renders the slot machine by calling the draw slot machine method in Render class.
        It also checks if the slot machine is spinning, and will start animating the slot machine.
    """
    if slotmachine.isSpinning():
        slotmachine.animateSpin()
    Render.draw_slotmachine(screen, slotmachine)
   

def main():
    """
        This is the main method which initializes, executes main loop, and uninitializes. The main loop calls the update and render functions.
    """
    global slotmachine
    slotmachine, screen, fps = init()

    clock = pygame.time.Clock()

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))

    while slotmachine.isOn():
        clock.tick(fps)
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                slotmachine.shutdown()

                
        update(slotmachine)        
        render(screen, slotmachine)        
        pygame.display.flip()
        
            


            

if __name__ == "__main__": main()
            
