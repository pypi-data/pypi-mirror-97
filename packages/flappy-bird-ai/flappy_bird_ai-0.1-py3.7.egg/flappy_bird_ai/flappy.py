import pkg_resources
from itertools import cycle
import random
import sys

import pygame
from pygame.locals import *
pygame.init()

# list of all possible players (tuple of 3 positions of flap)
PLAYERS_LIST = (
    # red bird
    (
        'assets/sprites/redbird-upflap.png',
        'assets/sprites/redbird-midflap.png',
        'assets/sprites/redbird-downflap.png',
    ),
    # blue bird
    (
        'assets/sprites/bluebird-upflap.png',
        'assets/sprites/bluebird-midflap.png',
        'assets/sprites/bluebird-downflap.png',
    ),
    # yellow bird
    (
        'assets/sprites/yellowbird-upflap.png',
        'assets/sprites/yellowbird-midflap.png',
        'assets/sprites/yellowbird-downflap.png',
    ),
)

PLAYERS_LIST = [
    [
        pkg_resources.resource_filename(__name__, fname)
        for fname in player
    ]
    for player in PLAYERS_LIST
]

# list of backgrounds
BACKGROUNDS_LIST = [
    'assets/sprites/background-day.png',
    'assets/sprites/background-night.png',
]

BACKGROUNDS_LIST = [
    pkg_resources.resource_filename(__name__, fname)
        for fname in BACKGROUNDS_LIST
]

# list of pipes
PIPES_LIST = [
    'assets/sprites/pipe-green.png',
    'assets/sprites/pipe-red.png',
]

PIPES_LIST = [
    pkg_resources.resource_filename(__name__, fname)
        for fname in PIPES_LIST
]

NUMBERS_LIST = [
    'assets/sprites/0.png',
    'assets/sprites/1.png',
    'assets/sprites/2.png',
    'assets/sprites/3.png',
    'assets/sprites/4.png',
    'assets/sprites/5.png',
    'assets/sprites/6.png',
    'assets/sprites/7.png',
    'assets/sprites/8.png',
    'assets/sprites/9.png',
]

NUMBERS_LIST = [
    pkg_resources.resource_filename(__name__, fname)
        for fname in NUMBERS_LIST
]

# image, sound and hitmask  dicts
IMAGES, SOUNDS, HITMASKS = {}, {}, {}

def load_image_assets():
    if len(IMAGES): # do nothing if already populated
        return

    # numbers sprites for score display
    IMAGES['numbers'] = [
        pygame.image.load(fname).convert_alpha()
            for fname in NUMBERS_LIST
    ]

    # game over sprite
    IMAGES['gameover'] = pygame.image.load(
        pkg_resources.resource_filename(__name__,
            'assets/sprites/gameover.png')).convert_alpha()
    # message sprite for welcome screen
    IMAGES['message'] = pygame.image.load(
        pkg_resources.resource_filename(__name__,
            'assets/sprites/message.png')).convert_alpha()
    # base (ground) sprite
    IMAGES['base'] = pygame.image.load(
        pkg_resources.resource_filename(__name__,
            'assets/sprites/base.png')).convert_alpha()

    # select random background sprites
    randBg = random.randint(0, len(BACKGROUNDS_LIST) - 1)
    IMAGES['background'] = pygame.image.load(BACKGROUNDS_LIST[randBg]).convert()

    # select random player sprites
    randPlayer = random.randint(0, len(PLAYERS_LIST) - 1)
    IMAGES['player'] = (
        pygame.image.load(PLAYERS_LIST[randPlayer][0]).convert_alpha(),
        pygame.image.load(PLAYERS_LIST[randPlayer][1]).convert_alpha(),
        pygame.image.load(PLAYERS_LIST[randPlayer][2]).convert_alpha(),
    )

    # select random pipe sprites
    pipeindex = random.randint(0, len(PIPES_LIST) - 1)
    IMAGES['pipe'] = (
        pygame.transform.flip(
            pygame.image.load(PIPES_LIST[pipeindex]).convert_alpha(), False, True),
        pygame.image.load(PIPES_LIST[pipeindex]).convert_alpha(),
    )

    # hitmask for pipes
    HITMASKS['pipe'] = (
        getHitmask(IMAGES['pipe'][0]),
        getHitmask(IMAGES['pipe'][1]),
    )

    # hitmask for player
    HITMASKS['player'] = (
        getHitmask(IMAGES['player'][0]),
        getHitmask(IMAGES['player'][1]),
        getHitmask(IMAGES['player'][2]),
    )

def load_audio_assets():
    if len(SOUNDS): # do nothing if already populated
        return

    # sounds
    if 'win' in sys.platform:
        soundExt = '.wav'
    else:
        soundExt = '.ogg'

    SOUNDS['die']    = pygame.mixer.Sound('assets/audio/die' + soundExt)
    SOUNDS['hit']    = pygame.mixer.Sound('assets/audio/hit' + soundExt)
    SOUNDS['point']  = pygame.mixer.Sound('assets/audio/point' + soundExt)
    SOUNDS['swoosh'] = pygame.mixer.Sound('assets/audio/swoosh' + soundExt)
    SOUNDS['wing']   = pygame.mixer.Sound('assets/audio/wing' + soundExt)    

def pixelCollision(rect1, rect2, hitmask1, hitmask2):
    """Checks if two objects collide and not just their rects"""
    rect = rect1.clip(rect2)

    if rect.width == 0 or rect.height == 0:
        return False

    x1, y1 = rect.x - rect1.x, rect.y - rect1.y
    x2, y2 = rect.x - rect2.x, rect.y - rect2.y

    for x in range(rect.width):
        for y in range(rect.height):
            if hitmask1[x1+x][y1+y] and hitmask2[x2+x][y2+y]:
                return True
    return False

def getHitmask(image):
    """returns a hitmask using an image's alpha."""
    mask = []
    for x in range(image.get_width()):
        mask.append([])
        for y in range(image.get_height()):
            mask[x].append(bool(image.get_at((x,y))[3]))
    return mask

def playerShm(playerShm):
    """oscillates the value of playerShm['val'] between 8 and -8"""
    if abs(playerShm['val']) == 8:
        playerShm['dir'] *= -1

    if playerShm['dir'] == 1:
         playerShm['val'] += 1
    else:
        playerShm['val'] -= 1

def checkCrash(player, upperPipes, lowerPipes, basey):
    """returns [collided, collided_ground], where:
        collided: indicates whether there was a collision;
        collided_ground: indicates whether a collision was with the ground
    """
    pi = player['index']
    player['w'] = IMAGES['player'][0].get_width()
    player['h'] = IMAGES['player'][0].get_height()

    # if player crashes into ground
    if player['y'] + player['h'] >= basey - 1:
        return [True, True]
    else:
        playerRect = pygame.Rect(player['x'], player['y'],
                      player['w'], player['h'])
        pipeW = IMAGES['pipe'][0].get_width()
        pipeH = IMAGES['pipe'][0].get_height()

        for uPipe, lPipe in zip(upperPipes, lowerPipes):
            # upper and lower pipe rects
            uPipeRect = pygame.Rect(uPipe['x'], uPipe['y'], pipeW, pipeH)
            lPipeRect = pygame.Rect(lPipe['x'], lPipe['y'], pipeW, pipeH)

            # player and upper/lower pipe hitmasks
            pHitMask = HITMASKS['player'][pi]
            uHitmask = HITMASKS['pipe'][0]
            lHitmask = HITMASKS['pipe'][1]

            # if bird collided with upipe or lpipe
            uCollide = pixelCollision(playerRect, uPipeRect, pHitMask, uHitmask)
            lCollide = pixelCollision(playerRect, lPipeRect, pHitMask, lHitmask)

            if uCollide or lCollide:
                return [True, False]

    return [False, False]

def ensure_container(obj):
    if isinstance(obj, list) or isinstance(obj, tuple):
        return obj
    else:
        return [obj]

physics_config = dict(
    playerMaxVelY=10, # max vel along Y, max descend speed
    playerMinVelY=-8, # min vel along Y, max ascend speed
    playerAccY=1, # players downward accleration
    playerVelRot=3, # angular speed
    playerRotThr=20, # rotation threshold
    playerFlapAcc=-9 # players speed on flapping
)

class Bird:
    def __init__(self,
        player_controller,
        playerx,
        playery,
        playerVelY=-9, # player's velocity along Y, default same as playerFlapped
        playerRot=45, # player's rotation
        playerAlive=True,
        score=0
    ):
        self.player_controller = player_controller
        self.playerx = playerx
        self.playery = playery
        self.playerVelY = playerVelY
        self.playerRot = playerRot
        self.playerAlive = playerAlive
        self.score = score
        self.current_score = 0

    def step(self, animIndex, next_animIndex, upperPipes, lowerPipes, basex, basey):
        self.current_score = 0

        if not self.playerAlive:
            return

        self.playerFlapped = self.player_controller(
            self, upperPipes, lowerPipes
        )

        if self.playerFlapped and self.playery > -2 * IMAGES['player'][0].get_height():
            self.playerVelY = physics_config['playerFlapAcc']
        else:
            self.playerFlapped = False

        # check for crash here
        crashTest = checkCrash(
            {'x': self.playerx, 'y': self.playery, 'index': animIndex},
            upperPipes, lowerPipes, basey
        )

        if crashTest[0]:
            self.playerAlive = False

            return {
                'y': self.playery,
                'groundCrash': crashTest[1],
                'basex': basex,
                'upperPipes': upperPipes,
                'lowerPipes': lowerPipes,
                'score': self.score,
                'playerVelY': self.playerVelY,
                'playerRot': self.playerRot
            }

        # check for score
        playerMidPos = self.playerx + IMAGES['player'][0].get_width() / 2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + IMAGES['pipe'][0].get_width() / 2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                self.current_score = 1
                self.score += self.current_score

        # rotate the player
        if self.playerRot > -90:
            self.playerRot -= physics_config['playerVelRot']

        # player's movement
        if self.playerVelY < physics_config['playerMaxVelY'] and not self.playerFlapped:
            self.playerVelY += physics_config['playerAccY']
        if self.playerFlapped:
            # more rotation to cover the threshold (calculated in visible rotation)
            self.playerRot = 45

        playerHeight = IMAGES['player'][next_animIndex].get_height()
        self.playery += min(self.playerVelY, basey - self.playery - playerHeight)

        # Player rotation has a threshold
        self.visibleRot = physics_config['playerRotThr']
        if self.playerRot <= physics_config['playerRotThr']:
            self.visibleRot = self.playerRot

class FlappyGame:
    def __init__(self, screen_width=288, screen_height=512,
        fps=30, pipe_gap_size=100, basey_coeff=0.79, 
        use_video=True, use_audio=True, player_controllers=None,
        x_offset=200
    ):
        if player_controllers is None:
            self.player_controllers = [KeyboardController()]
        else:
            self.player_controllers = ensure_container(player_controllers)

        self.screen_width = screen_width
        self.screen_height = screen_height
        self.fps = fps
        self.pipe_gap_size = pipe_gap_size
        self.basey = self.screen_height * basey_coeff
        self.use_audio = use_audio
        self.x_offset = x_offset

        self.fps_clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height))
        load_image_assets()

        if use_audio:
            load_audio_assets()

        pygame.display.set_caption('Flappy Bird')

    def showWelcomeAnimation(self):
        """Shows welcome screen animation of flappy bird"""
        # index of player to blit on screen
        animIndex = 0
        animIndexGen = cycle([0, 1, 2, 1])
        # iterator used to change animIndex after every 5th iteration
        loopIter = 0

        playerx = int(self.screen_width * 0.2)
        playery = int((self.screen_height - IMAGES['player'][0].get_height()) / 2)

        messagex = int((self.screen_width - IMAGES['message'].get_width()) / 2)
        messagey = int(self.screen_height * 0.12)

        basex = 0
        # amount by which base can maximum shift to left
        baseShift = IMAGES['base'].get_width() - IMAGES['background'].get_width()

        # player shm for up-down motion on welcome screen
        playerShmVals = {'val': 0, 'dir': 1}

        while True:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                    # make first flap sound and return values for mainGame
                    if self.use_audio:
                        SOUNDS['wing'].play()

                    return {
                        'playery': playery + playerShmVals['val'],
                        'basex': basex,
                        'animIndexGen': animIndexGen,
                    }

            # adjust playery, animIndex, basex
            if (loopIter + 1) % 5 == 0:
                animIndex = next(animIndexGen)
            loopIter = (loopIter + 1) % 30
            basex = -((-basex + 4) % baseShift)
            playerShm(playerShmVals)

            # draw sprites
            self.screen.blit(IMAGES['background'], (0,0))
            self.screen.blit(IMAGES['player'][animIndex],
                        (playerx, playery + playerShmVals['val']))
            self.screen.blit(IMAGES['message'], (messagex, messagey))
            self.screen.blit(IMAGES['base'], (basex, self.basey))

            pygame.display.update()
            self.fps_clock.tick(self.fps)

    def getRandomPipe(self):
        """returns a randomly generated pipe"""
        # y of gap between upper and lower pipe
        gapY = random.randrange(0, int(self.basey * 0.6 - self.pipe_gap_size))
        gapY += int(self.basey * 0.2)
        pipeHeight = IMAGES['pipe'][0].get_height()
        pipeX = self.screen_width + 10

        return [
            {'x': pipeX, 'y': gapY - pipeHeight},  # upper pipe
            {'x': pipeX, 'y': gapY + self.pipe_gap_size}, # lower pipe
        ]

    def showNumber(self, number, yoffset):
        """displays a number on the screen"""
        numberDigits = [int(x) for x in list(str(number))]
        totalWidth = 0 # total width of all numbers to be printed

        for digit in numberDigits:
            totalWidth += IMAGES['numbers'][digit].get_width()

        xoffset = (self.screen_width - totalWidth) / 2

        for digit in numberDigits:
            self.screen.blit(IMAGES['numbers'][digit], (xoffset, yoffset))
            xoffset += IMAGES['numbers'][digit].get_width()

    def showGameOverScreen(self, crashInfo):
        """crashes the player down ans shows gameover image"""
        score = crashInfo['score']
        playerx = self.screen_width * 0.2
        playery = crashInfo['y']
        playerHeight = IMAGES['player'][0].get_height()
        playerVelY = crashInfo['playerVelY']
        playerAccY = 2
        playerRot = crashInfo['playerRot']
        playerVelRot = 7

        basex = crashInfo['basex']

        upperPipes, lowerPipes = crashInfo['upperPipes'], crashInfo['lowerPipes']

        if self.use_audio:
            # play hit and die sounds
            SOUNDS['hit'].play()
            if not crashInfo['groundCrash']:
                SOUNDS['die'].play()

        while True:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                    if playery + playerHeight >= self.basey - 1:
                        return

            # player y shift
            if playery + playerHeight < self.basey - 1:
                playery += min(playerVelY, self.basey - playery - playerHeight)

            # player velocity change
            if playerVelY < 15:
                playerVelY += playerAccY

            # rotate only when it's a pipe crash
            if not crashInfo['groundCrash']:
                if playerRot > -90:
                    playerRot -= playerVelRot

            # draw sprites
            self.screen.blit(IMAGES['background'], (0,0))

            for uPipe, lPipe in zip(upperPipes, lowerPipes):
                self.screen.blit(IMAGES['pipe'][0], (uPipe['x'], uPipe['y']))
                self.screen.blit(IMAGES['pipe'][1], (lPipe['x'], lPipe['y']))

            self.screen.blit(IMAGES['base'], (basex, self.basey))
            self.showScore(score)

            playerSurface = pygame.transform.rotate(IMAGES['player'][1], playerRot)
            self.screen.blit(playerSurface, (playerx,playery))
            self.screen.blit(IMAGES['gameover'], (50, 180))

            self.fps_clock.tick(self.fps)
            pygame.display.update()

    def mainGame(self, movementInfo=None):
        if movementInfo is None:
            movementInfo = {
                'playery': int((self.screen_height - IMAGES['player'][0].get_height()) / 2),
                'basex': 0,
                'animIndexGen': cycle([0, 1, 2, 1]),
            }

        score = animIndex = loopIter = 0
        animIndexGen = movementInfo['animIndexGen']
        playerx, playery = int(self.screen_width * 0.2), movementInfo['playery']

        basex = movementInfo['basex']
        baseShift = IMAGES['base'].get_width() - IMAGES['background'].get_width()

        # get 2 new pipes to add to upperPipes lowerPipes list
        newPipe1 = self.getRandomPipe()
        newPipe2 = self.getRandomPipe()

        # list of upper pipes
        upperPipes = [
            {'x': self.screen_width + self.x_offset, 'y': newPipe1[0]['y']},
            {'x': self.screen_width + self.x_offset + (self.screen_width / 2), 'y': newPipe2[0]['y']},
        ]

        # list of lowerpipe
        lowerPipes = [
            {'x': self.screen_width + self.x_offset, 'y': newPipe1[1]['y']},
            {'x': self.screen_width + self.x_offset + (self.screen_width / 2), 'y': newPipe2[1]['y']},
        ]

        pipeVelX = -4

        # player velocity, max velocity, downward accleration, accleration on flap
        playerVelY    =  -9   # player's velocity along Y, default same as playerFlapped
        playerMaxVelY =  10   # max vel along Y, max descend speed
        playerMinVelY =  -8   # min vel along Y, max ascend speed
        playerAccY    =   1   # players downward accleration
        playerRot     =  45   # player's rotation
        playerVelRot  =   3   # angular speed
        playerRotThr  =  20   # rotation threshold
        playerFlapAcc =  -9   # players speed on flapping
        playerFlapped = False # True when player flaps

        birds = [Bird(ctrl, playerx, playery) for ctrl in self.player_controllers]
        birdsAlive = len(birds)
        max_score = 0

        while True:
            # draw sprites
            self.screen.blit(IMAGES['background'], (0, 0))

            # animIndex basex change
            next_animIndex = animIndex
            if (loopIter + 1) % 3 == 0:
                next_animIndex = next(animIndexGen)
            loopIter = (loopIter + 1) % 30
            basex = -((-basex + 100) % baseShift)

            score_sound = False
            flap_sound = False
          
            for bird in birds:
                crash_info = bird.step(
                    animIndex, next_animIndex,
                    upperPipes, lowerPipes,
                    basex, self.basey
                )

                max_score = max(max_score, bird.score)

                if bird.playerFlapped:
                    flap_sound = True

                if bird.current_score:
                    score_sound = True

                if not crash_info is None:
                    birdsAlive -= 1
                    if not birdsAlive:
                        return crash_info, birds

            if self.use_audio:
                if score_sound:
                    SOUNDS['point'].play()
                
                if flap_sound:
                    SOUNDS['wing'].play()

            animIndex = next_animIndex
            self.screen.blit(IMAGES['base'], (basex, self.basey))
            
            for bird in birds:
                if not bird.playerAlive: continue
                playerSurface = pygame.transform.rotate(IMAGES['player'][animIndex], bird.visibleRot)
                self.screen.blit(playerSurface, (bird.playerx, bird.playery))

            # move pipes to left
            for uPipe, lPipe in zip(upperPipes, lowerPipes):
                uPipe['x'] += pipeVelX
                lPipe['x'] += pipeVelX

            # add new pipe when first pipe is about to touch left of screen
            if len(upperPipes) > 0 and 0 < upperPipes[0]['x'] < 5:
                newPipe = self.getRandomPipe()
                upperPipes.append(newPipe[0])
                lowerPipes.append(newPipe[1])

            # remove first pipe if its out of the screen
            if len(upperPipes) > 0 and upperPipes[0]['x'] < -IMAGES['pipe'][0].get_width():
                upperPipes.pop(0)
                lowerPipes.pop(0)

            for uPipe, lPipe in zip(upperPipes, lowerPipes):
                self.screen.blit(IMAGES['pipe'][0], (uPipe['x'], uPipe['y']))
                self.screen.blit(IMAGES['pipe'][1], (lPipe['x'], lPipe['y']))

            # print score so player overlaps the score
            self.showNumber(max_score, self.screen_height * 0.1)
            # print the number of birds alive
            if len(birds) > 1:
                self.showNumber(birdsAlive, self.screen_height * 0.9)

            pygame.display.update()
            self.fps_clock.tick(self.fps)

        return {}, birds

    def run(self):
        while True:
            movementInfo = self.showWelcomeAnimation()
            crashInfo = self.mainGame(movementInfo)
            self.showGameOverScreen(crashInfo)

class BaseController:
    def __init__(self, action_delay=200):
        self.action_delay = action_delay    
        self.last_action_time = -action_delay

    def choose_action(self, *args):
        """
        Arguments: determined by preproc.
        Returns: A boolean value that expressed whether to flap or not.
        """
        raise NotImplementedError()        

    def preproc(self, bird, upperPipes, lowerPipes):
        """
        Preprocesses the input into:
            velocity: The vertical component of the bird's velocity.
            dist_horiz: The horizontal distance between the center of the gap
                        and the center of the bird.
            dist_verti: The vertical distance between the center of the gap
                        and the center of the bird.
        """
        playerw = IMAGES['player'][0].get_width()
        playerh = IMAGES['player'][0].get_height()
        player_centerx = bird.playerx + playerw / 2
        player_centery = bird.playery + playerh / 2

        pipeW = IMAGES['pipe'][0].get_width()
        pipeH = IMAGES['pipe'][0].get_height()

        for uPipe, lPipe in zip(upperPipes, lowerPipes):
            assert(uPipe['x'] == lPipe['x'])

            if bird.playerx > uPipe['x'] + pipeW:
                continue

            pipe_centerx = uPipe['x'] + pipeW / 2
            pipe_gap = lPipe['y'] - uPipe['y'] - pipeH
            pipe_centery = uPipe['y'] + pipeH + pipe_gap / 2

            break

        velocity = bird.playerVelY
        dist_horiz = pipe_centerx - player_centerx
        dist_verti = pipe_centery - player_centery

        return velocity, dist_horiz, dist_verti

    def __call__(self, bird, upperPipes, lowerPipes):
        playerFlapped = False

        if pygame.time.get_ticks() - self.last_action_time >= self.action_delay:
            args = self.preproc(bird, upperPipes, lowerPipes)            
            playerFlapped = self.choose_action(*args)
            self.last_action_time = pygame.time.get_ticks()

        return playerFlapped

class KeyboardController(BaseController):
    def __init__(self):
        super().__init__(action_delay=0)

    def preproc(self, *args):
        return []

    def choose_action(self, *args):
        playerFlapped = False

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                playerFlapped = True

        return playerFlapped

class RandomController(BaseController):
    def preproc(self, *args):
        return []

    def choose_action(self, *args):
        return random.randint(0, 1)

if __name__ == '__main__':
    game = FlappyGame()
    game.run()

