#CPT: BreakFast
# Authors : Idara & Arun
# Course: ICS-3U
# Date: 2019/01/07

#Imports
import pygame
from random import *

#------------ Swatches--------------
GREY = (35, 35, 35)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (66, 134, 244)
RED = (247, 51, 51)

#Setting Keys for Controls
ESC = chr(pygame.K_ESCAPE); U_ARROW = chr(pygame.K_UP); D_ARROW = chr(pygame.K_DOWN); R_ARROW = chr(pygame.K_RIGHT); L_ARROW = chr(pygame.K_LEFT);
NUM1 = chr(pygame.K_KP1);NUM2 = chr(pygame.K_KP2);NUM3 = chr(pygame.K_KP3);

class Player(pygame.sprite.Sprite):
    #Idara
    # Parameter - pos: initial position
    # Parameter - sprite: sprite image
    
    def __init__ (self, pos, sprite):
        
        #Sprite image information
        super(). __init__()
        self.image = pygame.image.load(sprite).convert()
        self.image.set_colorkey(BLACK)
        self.initSprite = sprite
        
        #Sprite mobility information
        self.pos = [pos[0], pos[1]]
        self.xVelocity = 0
        self.yVelocity = 0
        self.movementSpeed = 6
        
        #Item slot information - itemName, itemImage, itemSprite, itemRicochet, itemDieCollidewall, itemArc
        self.itemSlots = [["", "", None, None, None, None],\
        ["", "", None, None, None, None], \
        ["", "", None, None, None, None]]
        
        """
        #Item slot 1
        self.slot1Name = ""
        self.slot1Image = None
        self.slot1Sprite = None
        self.slot1Ricochet = None
        self.slot1DieCollideWall = None
        self.slot1Arc = None
        
        #Item slot 2
        self.slot2Name = ""
        self.slot2Image = None
        self.slot2Sprite = None
        self.slot2Ricochet = None
        self.slot2DieCollideWall = None
        self.slot2Arc = None
        
        #Item slot 3
        self.slot3Name = ""
        self.slot3Image = None
        self.slot3Sprite = None
        self.slot3Ricochet = None
        self.slot3DieCollideWall = None
        self.slot3Arc = None
        """
        
        #Weopon Usage Stats
        self.fireCooldown = 0
        self.indexSelection = 0
        
        #Location Data
        self.rect = self.image.get_rect()
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]
        self.initPosition = pos
        
        #Sprites that Player can bump into
        self.platformList = pygame.sprite.Group()
        
        #Setting User as alive
        self.alive = True
        self.deathTimer = 0
        
        #Setting User score
        self.score = 0
        
        #If player has either their flag or enemy flag
        self.blueFlag = False
        self.redFlag = False
        
    def gravity (self):
        #Set gravity to 1 when user is standing on platform
        if (self.yVelocity == 0):
            self.yVelocity = 1
        #Regularily increase gravity while user is not on platform
        else:
            self.yVelocity += .35
    #Parameter - velocity: direction of player movement
    def move(self, velocity):
        self.xVelocity = velocity * self.movementSpeed
        
    def kill(self):
        self.deathTimer = 60
        self.pos = [self.rect.x, self.rect.y - 1]
        self.image = pygame.image.load("deathSkull.png").convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]
        self.alive = False
        
        #Reset User's Items
        self.itemSlots = [["", "", None, None, None, None],\
        ["", "", None, None, None, None], \
        ["", "", None, None, None, None]]
       
        """
        #Item slot 1
        self.slot1Name = ""
        self.slot1Image = None
        self.slot1Sprite = None
        self.slot1Ricochet = None
        self.slot1DieCollideWall = None
        self.slot1Arc = None
        
        #Item slot 2
        self.slot2Name = ""
        self.slot2Image = None
        self.slot2Sprite = None
        self.slot2Ricochet = None
        self.slot2DieCollideWall = None
        self.slot2Arc = None
        
        #Item slot 3
        self.slot3Name = ""
        self.slot3Image = None
        self.slot3Sprite = None
        self.slot3Ricochet = None
        self.slot3DieCollideWall = None
        self.slot3Arc = None
        """ 
        
    def update(self):
        #If user is Alive, do this...
        if(self.alive == True):
            #Apply gravity
            self.gravity()
            
            #Move left or right
            self.rect.x += self.xVelocity
            
            #Check if collision occured (Right and Left)
            blockHitList = pygame.sprite.spritecollide(self, self.platformList, False)
            for block in blockHitList:
                #If User is walking towards the right
                if self.xVelocity > 0:
                    self.rect.right = block.rect.left
                #If User is walking towards the left
                if self.xVelocity < 0:
                    self.rect.left = block.rect.right
            
            #Stopping User from running off screen        
            if(self.rect.x < 0):
                self.rect.x = 0
            
            elif(self.rect.x > 1170):
                self.rect.x = 1170
        
            #Move up or down
            self.rect.y += self.yVelocity
            #Check if collision occured (Up and Down)
            blockHitList = pygame.sprite.spritecollide(self, self.platformList, False)
            for block in blockHitList:
                #If User makes contact downwards
                if self.yVelocity > 0:
                    self.rect.bottom = block.rect.top
                    #Stop vertical movement
                    self.yVelocity = 0
                #If User makes contact upwards
                elif self.yVelocity < 0:
                    self.rect.top = block.rect.bottom
                    #Stop vertical movement
                    self.yVelocity = 0
                
            #Lower fire cooldown by one
            if self.fireCooldown > 0:
                self.fireCooldown -= 1
        
        #If user is not alive, do this
        elif(self.alive == False):
            #Check if collision occured (Up and Down)
            blockHitList = pygame.sprite.spritecollide(self, self.platformList, False)
            for block in blockHitList:
                #If User makes contact downwards
                if self.yVelocity > 0:
                    self.rect.bottom = block.rect.top
                    #Stop vertical movement
                    self.yVelocity = 0
                #If User makes contact upwards
                elif self.yVelocity < 0:
                    self.rect.top = block.rect.bottom
                    #Stop vertical movement
                    self.yVelocity = 0
            self.yVelocity = 0
            
            #User's respawn timer
            if (self.deathTimer >= 0):
                self.deathTimer -= 1
            #User's respawn information
            else:
                self.image = pygame.image.load(self.initSprite).convert()
                self.image.set_colorkey(BLACK)
                self.rect = self.image.get_rect()
                self.rect.x = self.initPosition[0]
                self.rect.y = self.initPosition[1]
                self.alive = True
                self.fireCooldown = 0
            
    def jump(self):
        #Move down to check if there are any platforms below us
        self.rect.y += 2
        platformHitList = pygame.sprite.spritecollide(self, self.platformList, False)
        self.rect.y -= 2
        
        #If Player is colliding with a platform, they will jump
        if len(platformHitList) > 0:
            self.yVelocity = -8
    #Parameter- direction: direction of bullet travel
    def shoot(self, direction):
        #See if shooting cooldown is over and if there is something in the item slot
        if(self.fireCooldown == 0 and self.itemSlots[self.indexSelection][1] != ""):
            #create a new bullet
            newBullet = Bullet([self.rect.x , self.rect.y], self.itemSlots[self.indexSelection][0], self.itemSlots[self.indexSelection][2], self.itemSlots[self.indexSelection][3], self.itemSlots[self.indexSelection][4], self)
            newBullet.bulletDirection = direction
            newBullet.platformList = self.platformList
            #reset fire cooldown
            self.fireCooldown = 20
            #Take the used item out of user's item slots
            self.itemSlots[self.indexSelection] = ["", "", None, None, None, None]
            return newBullet
        #no bullet
        return None
    
    #Parameter - colour: Colour of the flag you want to be dropped   
    def dropFlag(self, colour):
        #If player drops the blue flag and they possess it
        if(colour == "blue" and self.blueFlag):
            xOffset = randrange(0,15)
            newBlueFlag = Flag([(self.rect.x + xOffset), self.rect.y], colour)
            newBlueFlag.platformList = self.platformList
            self.blueFlag = False
            return newBlueFlag
        #If player drops the red flag and they possess it
        elif(colour == "red" and self.redFlag):
            xOffset = randrange(0,15)
            newRedFlag = Flag([(self.rect.x + xOffset), self.rect.y], colour)
            newRedFlag.platformList = self.platformList
            self.redFlag = False
            return newRedFlag
        #No flag
        return None

#Parameter - x: location on the x axis of the platform
#            y: location on the y axis of the platform
#            width: width of the platform
#            height: height of the platform      
class Platform(pygame.sprite.Sprite): #Arun
    def __init__(self, x, y, width, height):
        #Calling parent constructor
        super().__init__()
        #Settting dimesions to what parameters have been passed in
        self.width = width
        self.height = height
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(GREY)
        self.rect = self.image.get_rect()
        #Setting location to what parameters have been passed in
        self.rect.x = x
        self.rect.y = y
        
#Parameter - pos: list of the coordinates of the drop
#            bulletName: name of the projectile
#            bulletSprite: image of the bullet
#            bulletImage: icon of the bullet
#            ricochet: can the bullet ricochet?
#            dieCollideWall: will the bullet die when collding with a wall?
#            arc: will the bullet arc?
class Drops(pygame.sprite.Sprite): #Idara
    def __init__(self, pos, bulletName, bulletSprite, bulletImage, ricochet, dieCollideWall, arc):
        super().__init__()
         
        #Initalizing attributes
        self.pos = [pos[0], pos[1]]
        self.attributes = [bulletSprite, bulletImage, ricochet, dieCollideWall, arc]
        self.image = pygame.image.load("drops.png").convert()
        self.rect = self.image.get_rect()
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]
        
        #List of objects drops can bump into
        self.platformList = pygame.sprite.Group()
        
        #If the object has a valid location
        self.collision = False
    
    #Parameter - sprites: Other sprites that the drop can collide with        
    def checkCol(self,sprites):
        collisionList = pygame.sprite.spritecollide(self,sprites,False)
        if len(collisionList) == 0:
            return False
        else:
            return True
            
    def respawn(self):
        self.rect.x = randrange(30, 1170)
        self.rect.y = randrange(0, 450)
        self.collision = self.checkCol(self.platformList)
        while(self.collision == True):
            self.rect.x = randrange(30, 1170)
            self.rect.y = randrange(0, 450)
            self.collision = self.checkCol(self.platformList)
        
    def update(self):
        #Apply Gravity
        self.rect.y += 5
        #Check if collision occured (Up and Down)
        blockHitList = pygame.sprite.spritecollide(self, self.platformList, False)
        for block in blockHitList:
            self.rect.bottom = block.rect.top
        
        #If block goes out of bounds
        if(self.rect.y > 540):
            self.respawn()

#Parameter - pos: List of the Base' coordinates
#          - playerName: Player that the base belongs to
#          - player: Name of the player that the base belongs to
class Base(pygame.sprite.Sprite): #Arun
    def __init__(self, pos, playerName, player):
        super().__init__()
        
        #Initialize attributes
        self.pos = [pos[0],pos[1]]
        self.player = player
        self.playerName = playerName
        self.image = pygame.Surface([70, 10])
        
        #Changing the colour of the base depending on the player
        if(self.playerName == "player1"):
            self.image.fill(BLUE)
            
        elif(self.playerName == "player2"):
            self.image.fill(RED)
        
        #Setting location information
        self.rect = self.image.get_rect()
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

#Parameter - pos: list of the coordinates of the bullet
#            sprite: image of the bullet
#            ricochet: can the bullet ricochet?
#            dieCollideWall: will the bullet die when collding with a wall?
#            arc: will the bullet arc?
#            creator: who does the bullet belong to?
class Bullet(pygame.sprite.Sprite): #Idara & Arun
    def __init__(self, pos, sprite, ricochet, dieCollideWall, arc, creator):
        super().__init__()
        
        #Initializing attributes
        self.sprite = sprite
        self.pos = pos
        self.ricochet = ricochet
        self.dieCollideWall = dieCollideWall
        self.arc = arc
        self.creator = creator
        self.xVelocity = 7.5
        self.yVelocity = -9
        self.bulletDirection = 1
        #self.xOffset = 15
        
        #If the bullet is able to ricochet, it will ricochet twice
        if(self.ricochet == True):
            self.ricochet = 3
        elif(self.ricochet == False):
            self.ricochet = 0
            
        #If the bullet is a waffle, increase its speed
        if(self.sprite == "waffle.gif"):
            self.xVelocity = 9
            
        #If the bullet is an egg, increase throw height and speed
        if(self.sprite == "egg.gif"):
            self.yVelocity = -9.75
            self.xVelocity = 9.25
        
        #Bullet Visual
        self.image = pygame.image.load(self.sprite).convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1] + 15
        
        #Platforms that can be collided into
        self.platformList = pygame.sprite.Group()
        
    def gravity(self):
        #Set gravity to 1 when user is standing on platform
        if (self.yVelocity == 0):
            self.yVelocity = 1
        #Regularily increase gravity while user is not on platform
        else:
            self.yVelocity += .4
    
    def update(self):
        if(self.arc == True):
            #Apply gravity
            self.gravity()
            
            #Move to the left or right
            self.rect.x += self.xVelocity * self.bulletDirection
            
            #If Bullet meakes horizontal contact
            blockHitList = pygame.sprite.spritecollide(self, self.platformList, False)
            for block in blockHitList:
                #If Bullet makes contact on the right
                if((self.xVelocity * self.bulletDirection) > 0):
                    if(self.ricochet > 0):
                        self.rect.right = block.rect.left
                        self.bulletDirection = -1
                        self.ricochet -= 1
                    else:
                        self.rect.x = -100
                        
                elif((self.xVelocity * self.bulletDirection) < 0):
                    if(self.ricochet > 0):
                        self.rect.left = block.rect.right
                        self.bulletDirection = 1
                        self.ricochet -= 1
                    else:
                        self.rect.x = -100
            
            #Move upwards or downwards
            self.rect.y += self.yVelocity
            
            #If Bullet makes vertical contact
            blockHitList = pygame.sprite.spritecollide(self, self.platformList, False)
            for block in blockHitList:
                #If bullet makes contact upwards
                if(self.yVelocity < 0):
                    if(self.ricochet > 0):
                        self.rect.top = block.rect.bottom
                        self.yVelocity = 0
                        self.ricochet -= 1
                    else:
                        self.rect.x = -100
                
                elif(self.yVelocity > 0):
                    if(self.ricochet > 0):
                        self.rect.bottom = block.rect.top
                        self.yVelocity = -9.25
                        self.ricochet -= 1
                    else:
                        self.rect.x = -100
                        
        elif(self.arc == False):
            self.rect.x += self.xVelocity * self.bulletDirection
            
            #If Bullet collides
            blockHitList = pygame.sprite.spritecollide(self, self.platformList, False)
            for block in blockHitList:
                #If Bullet makes contact on the right
                if((self.xVelocity * self.bulletDirection) > 0):
                    if(self.ricochet > 0):
                        self.bulletDirection = -1
                    else:
                        self.bulletDirection = 1
                elif((self.xVelocity * self.bulletDirection) < 0):
                     if(self.ricochet > 0):
                        self.bulletDirection = 1
                        self.ricochet -= 1
                     else:
                         self.bulletDirection = -1 
        
    """           
    def update(self):
        if(self.arc == False):
            self.pos[0] += self.xVelocity * self.bulletDirection
            self.rect.x = self.pos[0]
            blockHitList = pygame.sprite.spritecollide(self, self.platformList, False)
            for block in blockHitList:
                #If Bullet makes contact on the right
                if((self.xVelocity * self.bulletDirection) > 0):
                    #If bullet can ricochet, If so, change the bullet direction
                    if(self.ricochet > 0):
                        self.bulletDirection = -1
                        self.ricochet -= 1
                    else:
                        self.rect.x = -100
                #If Bullet makes contact on the left
                elif((self.xVelocity * self.bulletDirection) < 0):
                    #If bullet can ricochet, If so, change the bullet direction
                    if(self.ricochet > 0):
                        self.bulletDirection = 1
                        self.ricochet -= 1
                    else:
                        self.rect.x = -100
        
        elif(self.arc == True):
            #Increment the x position
            self.pos[0] += self.xVelocity * self.bulletDirection
            self.rect.x = self.pos[0] + 30
            
            #If block impacts any platforms horizontally
            blockHitList = pygame.sprite.spritecollide(self, self.platformList, False)
            for block in blockHitList:
                #If Bullet makes contact on the right
                if((self.xVelocity * self.bulletDirection) > 0):
                    #If bullet can ricochet, If so, change the bullet direction
                    if(self.ricochet > 0):
                        self.bulletDirection = -1
                        self.ricochet -= 1
                    else:
                        self.rect.x = -100
                #If bullet impacts on the left
                elif((self.xVelocity * self.bulletDirection) < 0):
                    if(self.ricochet > 0):
                        self.bulletDirection = 1
                        self.ricochet -= 1
                    else:
                        self.rect.x = -100
            
            #Increment the y position
            self.previousY = self.rect.y            
            self.pos[1] = -0.07 * (self.pos[0] - self.xOffset)**2 + 15.75
            self.rect.y = self.pos[1] + 30
            
            #If block impacts any platforms vertically
            blockHitList = pygame.sprite.spritecollide(self, self.platformList, False)
            for block in blockHitList:
                #If bullet impacts downwards
                if((self.pos[1] - self.previousY) > 0):
                    self.xOffset += 15
                    self.pos[0] = 0
                #If User impacts upwards
                elif((self.pos[1] - self.previousY) < 0):
                    self.rect.top = block.rect.bottom
    """
#Parameters - pos: List of the coordinates of the flag
#           - colour: colour of the flag
class Flag(pygame.sprite.Sprite): #Arun
    def __init__(self, pos, colour):
        super().__init__()
        
        self.pos = pos
        self.colour = colour
        self.creator = None
        
        #If this is player 1's flag
        if(self.colour == "blue"):
            self.image = pygame.image.load("player1Flag.gif").convert()
        #If this is player 2's flag
        elif(self.colour == "red"):
            self.image = pygame.image.load("player2Flag.gif").convert()
        self.image.set_colorkey(WHITE)
        
        #Location Information
        self.rect = self.image.get_rect()
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]
        self.yVelocity = 0
        
        #List of platforms that flag can bump into
        self.platformList = pygame.sprite.Group()
        
    def gravity(self):
        if(self.yVelocity == 0):
            self.yVelocity = 1
        else:
            self.yVelocity += .2
            
    def update(self):
        #Apply gravity
        self.gravity()
        self.rect.y += self.yVelocity
        
        #Check if flag has landed on top of a platform        
        blockHitList = pygame.sprite.spritecollide(self, self.platformList, False)
        for block in blockHitList:
            #If Flag makes contact downwards
            if self.yVelocity > 0:
                self.rect.bottom = block.rect.top
                #Stop vertical movement
                self.yVelocity = 0
                
        if(self.rect.y > 510):
            self.rect.y = 0
               
            

    
#=========================== Main Class ===============================
class Main:
    #Idara
    def __init__(self):
        pygame.mixer.pre_init(44100,16,2,4096)
        pygame.init()
        self.screen = pygame.display.set_mode([1200, 700])
        pygame.display.set_caption("Breakfast Battles")
        pygame.mouse.set_visible(True)
        self.clock = pygame.time.Clock()

        #Player1 w,s,a,d, r,t,y
        #Player2 U,D,L,R, 1,2,3
        self.pressed = {ESC:False, \
            "w":False, "s":False, "a":False, "d":False, "r":False, "t":False, "y":False, \
            U_ARROW:False, D_ARROW:False, L_ARROW:False, R_ARROW:False, NUM1:False, NUM2:False, NUM3:False}        
       
        self.play = True
        
        #Play the music on repeat, theme created by Arun
        pygame.mixer.music.load("breakfast.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
        
    def initLevel(self):
        self.allSprites = pygame.sprite.Group()
        self.rigidbodySprites = pygame.sprite.Group()
        
        self.playerSprites = pygame.sprite.Group()
        self.bulletSprites = pygame.sprite.Group()
        self.platformList = pygame.sprite.Group()
        self.dropSprites = pygame.sprite.Group()
        self.baseSprites = pygame.sprite.Group()
        self.flagSprites = pygame.sprite.Group()
        
        #Initializing Objects for Players
        self.player1 = Player([0,0], "playerOneSprite.png")
        self.player1.blueFlag = True
        self.allSprites.add(self.player1)
        self.playerSprites.add(self.player1)
        self.rigidbodySprites.add(self.player1)
        self.player2 = Player([1170,0], "playerTwoSprite.png")
        self.player2.redFlag = True
        self.allSprites.add(self.player2)
        self.playerSprites.add(self.player2)
        self.rigidbodySprites.add(self.player2)
        
        #Initializing all Platforms
        platforms = [[0, 510, 400, 30], [475, 415, 250, 30], [0, 415, 85, 30], [65, 320, 400, 30], \
        [0, 225, 85, 30], [140, 0, 30, 350], [170, 235, 80, 30], [225, 150, 275, 30], [562.5, 220, 75, 30], [800, 510, 400, 30],\
        [1115, 415, 85, 30], [735, 320, 400, 30], [1115, 225, 85, 30], [1030, 0, 30, 350], [950, 235, 80, 30], [700, 150, 275, 30]]
        
        for platform in platforms:
            newPlatform = Platform(platform[0], platform[1], platform[2], platform[3])
            self.allSprites.add(newPlatform)
            self.rigidbodySprites.add(newPlatform)
            self.platformList.add(newPlatform)
            self.player1.platformList.add(newPlatform)
            self.player2.platformList.add(newPlatform)
            
        #Initializing Both Player Bases
        bases = [[[7.5, 224], "player1", self.player1], [[1124, 224], "player2", self.player2]]
        
        for base in bases:
            newBase = Base(base[0], base[1], base[2])
            self.allSprites.add(newBase)
            self.baseSprites.add(newBase)
                        
        #Different Types of bullets
        #Egg
        bulletTypes = [[[0,0], "Egg", "egg.gif", "eggImage.gif", False, True, True],\
        [[0,0], "Waffle", "waffle.gif", "waffleImage.gif", False, True, False],\
        [[0,0], "Spoon", "spoon.gif", "spoonImage.gif", True, False, True]]
        
        for numberOfDrops in range(2):
            param = bulletTypes[randrange(0,3)]
            newX = randrange(30,1170)
            newY = randrange(0,450)
            param[0] = (newX, newY)
            newDrop = Drops(param[0], param[1], param[2], param[3], param[4], param[5], param[6])
            while newDrop.checkCol(self.allSprites) == True:
                newX = randrange(30,1170)
                newY = randrange(0, 450)
                param[0] = (newX, newY)
                newDrop = Drops(param[0], param[1], param[2], param[3], param[4], param[5], param[6])
            newDrop.platformList = self.platformList
            self.allSprites.add(newDrop)
            self.dropSprites.add(newDrop)
    
    def eventHandler(self):
        for event in pygame.event.get():
            #Quits the Game if User chooses to
            if event.type == pygame.QUIT:
                self.play = False
            #If user presses a key set key pressed to true
            if event.type == pygame.KEYDOWN:
                self.pressed[chr(event.key)] = True
            #If user lets go of a key, set key pressed to false
            if event.type == pygame.KEYUP:
                self.pressed[chr(event.key)] = False
    
    def loop(self):
        self.initLevel()
        while self.play == True:
            self.eventHandler()
            self.update()
            self.render()
            self.clock.tick(60)
    
    def update(self):
        #If User presses ESC, exit the game
        if self.pressed[ESC]:
            self.play = False
        
        #Player1 Actions
        changeX = 0
        #if player1 presses d, move them to the right
        if self.pressed["d"] == True:
            changeX += 1
        #if player1 presses a, move them to the left
        if self.pressed["a"] == True:
            changeX -= 1
        #if player1 presses w, jump
        if self.pressed["w"] == True:
            self.player1.jump()
        #if player 1 pressed t, select the next item
        if self.pressed["t"] == True:
            self.player1.indexSelection += 1
            #if player 1 has gone past the 3rd index
            if(self.player1.indexSelection > 2):
                self.player1.indexSelection = 0
            self.pressed["t"] = False
        #Apply Player 1 Movements
        self.player1.move(changeX)
        
        #Player2 Actions
        changeX = 0
        #if player2 presses right arrow, move them to the right
        if self.pressed[R_ARROW] == True:
            changeX = 1
        #if player2 presses left arrow, move them to the left
        if self.pressed[L_ARROW] == True:
            changeX = -1
        #if player2 presses up arrow, jump
        if self.pressed[U_ARROW] == True:
            self.player2.jump()
        #if player2 presses 2, select the next item
        if self.pressed[NUM2] == True:
            self.player2.indexSelection += 1
            #if player 1 has gone past the 3rd index
            if(self.player2.indexSelection > 2):
                self.player2.indexSelection = 0
            self.pressed[NUM2] = False
        
        #Apply Player 2 Movements
        self.player2.move(changeX)
        
        #Creating Drops
        #Different Types of bullets
        #Egg
        bulletTypes = [[[0,0], "Egg", "egg.gif", "eggImage.gif", False, True, True],\
        [[0,0], "Waffle", "waffle.gif", "waffleImage.gif", False, True, False],\
        [[0,0], "Spoon", "spoon.gif", "spoonImage.gif", True, False, True]]
        
        #If User picks up a drop
        for player in self.playerSprites:
            for currentSlot in range(3):
                if(player.itemSlots[currentSlot][0] == ""):
                    collisionList = pygame.sprite.spritecollide(player, self.dropSprites, False)
                    for collisionObject in collisionList:
                        player.itemSlots[currentSlot] = collisionObject.attributes
                        self.dropSprites.remove(collisionObject)
                        self.allSprites.remove(collisionObject)
                        
            """       
            #If Player has no items in slot 1, add the item characteristics to slot 1
            if(player.slot1Name == ""):
                collisionList = pygame.sprite.spritecollide(player, self.dropSprites, False)
                for collisionObject in collisionList:
                    self.dropSprites.remove(collisionObject)
                    self.allSprites.remove(collisionObject)
                    player.slot1Name = collisionObject.bulletName
                    player.slot1Image = collisionObject.bulletImage
                    player.slot1Sprite = collisionObject.bulletSprite
                    player.slot1Ricochet = collisionObject.ricochet
                    player.slot1DieCollideWall = collisionObject.dieCollideWall
                    player.slot1Arc = collisionObject.arc
            
            #If player has no items in slot 2, and has an item in slot 1, add item characteristics to slot 2
            elif(player.slot1Name != "" and player.slot2Name == ""):
                collisionList = pygame.sprite.spritecollide(player, self.dropSprites, False)
                for collisionObject in collisionList:
                    self.dropSprites.remove(collisionObject)
                    self.allSprites.remove(collisionObject)
                    player.slot2Name = collisionObject.bulletName
                    player.slot2Image = collisionObject.bulletImage
                    player.slot2Sprite = collisionObject.bulletSprite
                    player.slot2Ricochet = collisionObject.ricochet
                    player.slot2DieCollideWall = collisionObject.dieCollideWall
                    player.slot2Arc = collisionObject.arc
            
            #If player has no items in slot 3, and has items in slots 1 and 3, add item characteristics to slot 3
            elif(player.slot1Name != "" and player.slot2Name != "" and player.slot3Name == ""):
                collisionList = pygame.sprite.spritecollide(player, self.dropSprites, False)
                for collisionObject in collisionList:
                    self.dropSprites.remove(collisionObject)
                    self.allSprites.remove(collisionObject)
                    player.slot3Name = collisionObject.bulletName
                    player.slot3Image = collisionObject.bulletImage
                    player.slot3Sprite = collisionObject.bulletSprite
                    player.slot3Ricochet = collisionObject.ricochet
                    player.slot3DieCollideWall = collisionObject.dieCollideWall
                    player.slot3Arc = collisionObject.arc
            """
#============================== Bullet Stuff ======================================
        #If Player 1 shoots
        #If Player 1 shoots to the right
        if(self.pressed["r"] and self.pressed["d"]):
            newBullet = self.player1.shoot(1)
            if newBullet != None:
                self.allSprites.add(newBullet)
                self.bulletSprites.add(newBullet)
                self.rigidbodySprites.add(newBullet)
        #If Player 1 shoots to the left        
        if(self.pressed["r"] and self.pressed["a"]):
            newBullet = self.player1.shoot(-1)
            if newBullet != None:
                self.allSprites.add(newBullet)
                self.bulletSprites.add(newBullet)
                self.rigidbodySprites.add(newBullet)
                
        #If Player 2 shoots
        #If Player 2 shoots to the right
        if(self.pressed[NUM1] and self.pressed[R_ARROW]):
            newBullet = self.player2.shoot(1)
            if newBullet != None:
                self.allSprites.add(newBullet)
                self.bulletSprites.add(newBullet)
                self.rigidbodySprites.add(newBullet)
        #If Player 2 shoots to the left
        if(self.pressed[NUM1] and self.pressed[L_ARROW]):
            newBullet = self.player2.shoot(-1)
            if newBullet != None:
                self.allSprites.add(newBullet)
                self.bulletSprites.add(newBullet)
                self.rigidbodySprites.add(newBullet)
        
        #Update All Bullets        
        for bullet in self.bulletSprites:
            bullet.update()
        
        #If bullet goes off screen, kill it
            if(bullet.rect.x > 1230 or bullet.rect.x < -30):
                self.bulletSprites.remove(bullet)
                self.allSprites.remove(bullet)
                self.rigidbodySprites.remove(bullet)
            #If player gets hit by a bullet
            collisionList = pygame.sprite.spritecollide(bullet, self.playerSprites, False)
            #If player gets hit by their own bullet they don't die
            if(bullet.creator in collisionList):
                collisionList.remove(bullet.creator)
            
            for collisionObject in collisionList:
                #If player 1 dies
                if collisionObject == self.player1:
                    #kill the player
                    self.player1.kill()
                    
                    #delete the bullet
                    self.bulletSprites.remove(bullet)
                    self.allSprites.remove(bullet)
                    self.rigidbodySprites.remove(bullet)
                    
                    #Drop flags
                    #drop the blue flag if they have it
                    self.blueFlag = self.player1.dropFlag("blue")
                    if(self.blueFlag != None):
                        self.blueFlag.creator = self.player1
                        self.allSprites.add(self.blueFlag)
                        self.rigidbodySprites.add(self.blueFlag)
                        self.flagSprites.add(self.blueFlag)
                    #drop the red flag if they have it
                    self.redFlag = self.player1.dropFlag("red")
                    if(self.redFlag != None):
                        self.redFlag.creator = self.player2
                        self.allSprites.add(self.redFlag)
                        self.rigidbodySprites.add(self.redFlag)
                        self.flagSprites.add(self.redFlag)
                        
                
                #If player 2 dies    
                if collisionObject == self.player2:
                    #kill the player
                    self.player2.kill()
                    
                    #delete the bullet
                    self.bulletSprites.remove(bullet)
                    self.allSprites.remove(bullet)
                    self.rigidbodySprites.remove(bullet)
                    
                    #Drop flags
                    #drop the blue flag if they have it
                    self.blueFlag = self.player2.dropFlag("blue")
                    if(self.blueFlag != None):
                        self.blueFlag.creator = self.player1
                        self.allSprites.add(self.blueFlag)
                        self.rigidbodySprites.add(self.blueFlag)
                        self.flagSprites.add(self.blueFlag)
                    #drop the red flag if they have it
                    self.redFlag = self.player2.dropFlag("red")
                    if(self.redFlag != None):
                        self.redFlag.creator = self.player2
                        self.allSprites.add(self.redFlag)
                        self.rigidbodySprites.add(self.redFlag)
                        self.flagSprites.add(self.redFlag) 
              
#================================ Flag Stuff ====================================
        #Check for if player collides with a flag
        for flag in self.flagSprites:
            #Update all flags
            flag.update()
            
            #If player collides with a flag
            collisionList = pygame.sprite.spritecollide(flag, self.playerSprites, False)
            for collisionObject in collisionList:
                #If player1 collides with the flag
                if(collisionObject == self.player1 and self.player1.alive):
                    if(flag.colour == "blue"):
                        self.player1.blueFlag = True
                        self.allSprites.remove(self.blueFlag)
                        self.rigidbodySprites.remove(self.blueFlag)
                        self.flagSprites.remove(self.blueFlag)
                    if(flag.colour == "red"):
                        self.player1.redFlag = True
                        self.allSprites.remove(self.redFlag)
                        self.rigidbodySprites.remove(self.redFlag)
                        self.flagSprites.remove(self.redFlag)
                
                #If player2 collides with the flag
                elif(collisionObject == self.player2 and self.player2.alive):
                    if(flag.colour == "blue"):
                        self.player2.blueFlag = True
                        self.allSprites.remove(self.blueFlag)
                        self.rigidbodySprites.remove(self.blueFlag)
                        self.flagSprites.remove(self.blueFlag)
                    if(flag.colour == "red"):
                        self.player2.redFlag = True
                        self.allSprites.remove(self.redFlag)
                        self.rigidbodySprites.remove(self.redFlag)
                        self.flagSprites.remove(self.redFlag)
        
        #If player has both flags, lower their speed
        for player in self.playerSprites:
            if(player.blueFlag and player.redFlag):
                player.movementSpeed = 3
            else:
                player.movementSpeed = 6

#=============================== Base Stuff ================================        
        #If player touches their base, while holding enemyFlag
        for player in self.playerSprites:
            collisionList = pygame.sprite.spritecollide(player, self.baseSprites, False)
            
            for collisionObject in collisionList:
                #If player1 collides with their base while possessing red flag
                if(player == self.player1 and self.player1.redFlag and collisionObject.player == self.player1):
                    self.player1.score += 1
                    self.player1.redFlag = False
                    self.player2.redFlag = True
                #If player2 collides with their base while possessing blue flag
                elif(player == self.player2 and self.player2.blueFlag and collisionObject.player == self.player2):
                    self.player2.score += 1
                    self.player2.blueFlag = False
                    self.player1.blueFlag = True
        
#============================== Drops Stuff =========================================        
        # Drops only spwan if there are less than 3 already present
        if len(self.dropSprites) < 3:
            # There is a one in 300 chance of spawning a drop
            if randrange(0, 250) == 0:
                param = bulletTypes[randrange(0,3)]
                newX = randrange(30, 1170)
                newY = randrange(0, 450)
                param[0] = [newX,newY]
                newDrop = Drops(param[0],param[1],param[2],param[3],param[4],param[5],param[6])
                while newDrop.checkCol(self.allSprites) == True:
                    newX = randrange(30,1170)
                    newY = randrange(0,450)
                    param[0] = (newX,newY)
                    newDrop = Drops(param[0],param[1],param[2],param[3],param[4],param[5],param[6])
                newDrop.platformList = self.platformList
                self.allSprites.add(newDrop)
                self.dropSprites.add(newDrop)
        
#=========================== User Death Scenerios ===================================
        for player in self.playerSprites:
            player.update()
            if(player == self.player1 and player.rect.y > 510):
                #kill the player
                self.player1.kill()
                
                #Drop flags
                #drop the blue flag if they have it
                if(player.blueFlag):
                    self.blueFlag = self.player1.dropFlag("blue")
                    if(self.blueFlag != None):
                        self.blueFlag.creator = self.player1
                        self.allSprites.add(self.blueFlag)
                        self.rigidbodySprites.add(self.blueFlag)
                        self.flagSprites.add(self.blueFlag)
                
                if(player.redFlag):
                    #drop the red flag if they have it
                    self.redFlag = self.player1.dropFlag("red")
                    if(self.redFlag != None):
                        self.redFlag.creator = self.player2
                        self.allSprites.add(self.redFlag)
                        self.rigidbodySprites.add(self.redFlag)
                        self.flagSprites.add(self.redFlag)
            
            if(player == self.player2 and player.rect.y > 510):
                #kill the player
                self.player2.kill()
                
                #Drop flags
                #drop the blue flag if they have it
                if(player.blueFlag):
                    self.blueFlag = self.player2.dropFlag("blue")
                    if(self.blueFlag != None):
                        self.blueFlag.creator = self.player1
                        self.allSprites.add(self.blueFlag)
                        self.rigidbodySprites.add(self.blueFlag)
                        self.flagSprites.add(self.blueFlag)
                #drop the red flag if they have it
                if(player.redFlag):
                    self.redFlag = self.player2.dropFlag("red")
                    if(self.redFlag != None):
                        self.redFlag.creator = self.player2
                        self.allSprites.add(self.redFlag)
                        self.rigidbodySprites.add(self.redFlag)
                        self.flagSprites.add(self.redFlag)  
        
        #update drop sprites
        self.dropSprites.update()
        
    def render(self):
        self.screen.fill((68, 95, 142))
        
        #Drawing All sprites
        self.platformList.draw(self.screen)
        self.dropSprites.draw(self.screen)
        self.playerSprites.draw(self.screen)
        self.baseSprites.draw(self.screen)
        self.bulletSprites.draw(self.screen)
        self.flagSprites.draw(self.screen)
        
        #Drawing HUD
        hudBackground = pygame.image.load("HUDbackground.png").convert()
        self.screen.blit(hudBackground, [0, 550])
        
        #Drawing Item images
        for player in self.playerSprites:
            for currentSlot in range (3):
                itemImage = str(player.itemSlots[currentSlot][1])
                if(itemImage != ""):
                    itemBlitImage = pygame.image.load(itemImage).convert()
                    # itemBlitImage.set_colorkey(WHITE)
                    if(player == self.player1):
                        self.screen.blit(itemBlitImage,[(15 + 135 * currentSlot), 570])
                    elif(player == self.player2):
                        self.screen.blit(itemBlitImage,[(795 + 135 * currentSlot), 570])
        
        #Drawing Boxes for Item Images
        for xOffset in range(15, 400, 135):
            pygame.draw.rect(self.screen, GREY, [xOffset, 570, 115, 115], 8)
            pygame.draw.rect(self.screen, GREY, [(1080 - xOffset), 570, 115, 115], 8)
            
        #Drawing Score
        font = pygame.font.SysFont('Consolas', 55, True, False)
        text = font.render("Score:", True, GREY)
        player1Score = font.render(str(self.player1.score), True, BLUE)
        player2Score = font.render(str(self.player2.score), True, RED)
        hyphen = font.render("-", True, GREY)
        self.screen.blit(text, (455, 600))
        self.screen.blit(player1Score, [635, 600])
        self.screen.blit(hyphen, [665, 600])
        self.screen.blit(player2Score, (695, 600))
        
        #Drawing Player's Item select choices
        #Player 1
        pygame.draw.rect(self.screen, BLUE, [(15 + (135 * self.player1.indexSelection)), 570, 115, 115], 8)
        #Player 2
        pygame.draw.rect(self.screen, RED, [(795 + (135 * self.player2.indexSelection)), 570, 115, 115], 8)
        
        #Drawing Player's Flag Icons
        player1FlagSprite = pygame.image.load("player1FlagSprite.gif").convert()
        player2FlagSprite = pygame.image.load("player2FlagSprite.gif").convert()
        
        #Flag icon conditions for if a player posesses a flag
        if(self.player1.blueFlag):
            self.screen.blit(player1FlagSprite, [410, 570])
        if(self.player1.redFlag):
            self.screen.blit(player2FlagSprite, [410, 595])
        if(self.player2.redFlag):
            self.screen.blit(player2FlagSprite, [770, 570])
        if(self.player2.blueFlag):
            self.screen.blit(player1FlagSprite, [770, 595])
        
        #End of Drawing Code
        pygame.display.flip()

#Calling Main - Arun 
if __name__ == "__main__":
    main = Main()
    main.loop()
    pygame.quit()

        
        







