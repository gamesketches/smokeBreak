import pygame, sys, os
from pygame.locals import *

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

main_dir = os.path.split(os.path.abspath(sys.argv[0]))[0]
data_dir = os.path.join(main_dir, 'data')

allsprites = pygame.sprite.Group()

def load_image(name, colorkey=None):
    fullname = os.path.join(data_dir, name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error:
        print('Cannot load image:', fullname)
        raise SystemExit(str(geterror()))
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

def load_sound(name):
    class NoneSound:
        def play(self):pass
    if not pygame.mixer or not pygame.mixer.get_init():
        return NoneSound()
    fullname = os.path.join(data_dir, name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error:
        print ('Cannot load sound: %s' % fullname)
        raise SystemExit(str(geterror()))
    return sound

class Cigarette():
    def __init__(self):
        self.curLength = 100
        self.burnDelay = 0
        self.whitePart = pygame.Surface((self.curLength, 20))
        self.whitePart.fill((250,250,250))
        self.whitePart.convert()
        self.filterLine = pygame.Surface((5, 20))
        self.filterLine.convert()
        self.filterLine.fill((0,100,250))

    def update(self, screen):
        self.burnDelay += 1
        if self.curLength > 30 and self.burnDelay >= 10:
            self.curLength -= 1
            self.whitePart = pygame.transform.scale(self.whitePart, (self.curLength, 20))
            self.burnDelay = 0
        screen.blit(self.whitePart, (200,200))
        screen.blit(self.filterLine, (230, 200))

class Arm(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #self.mainPart = pygame.Surface((10, 200))
        #self.mainPart.fill((214, 134, 21))
        #self.mainPart.convert()
        self.image, self.rect = load_image('arm.bmp', -1)
        self.cig = Cigarette()

    def update(self, screen):
        #screen.blit(self.mainPart, (200,200))
        self.cig.update(screen)

    def rotate(self, amount):
        self.mainPart = pygame.transform.rotate(self.mainPart, amount)

def main():
    
    #Initialize Everything
    pygame.init()
    screen = pygame.display.set_mode((468, 300))
    pygame.display.set_caption('Smoke Break')
    pygame.mouse.set_visible(0)

    #Create the background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))

    #Display The Background
    screen.blit(background, (0,0))
    pygame.display.flip()

    #Prepare Game Objects
    clock = pygame.time.Clock()
    #cig = Cigarette()
    arm = Arm()

    going = True
    while going:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
            elif event.type == KEYDOWN and event.key == K_RIGHT:
                arm.rotate(45)
            elif event.type == KEYDOWN and event.key == K_LEFT:
                arm.rotate(-90)

        screen.blit(background, (0,0))
        arm.update(screen)
        pygame.display.flip()

if __name__ == '__main__':
    main()
