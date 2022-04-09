import pyglet
import random
from pyglet.window import key
from pyglet.window import mouse

window = pyglet.window.Window()
fps_display = pyglet.window.FPSDisplay(window=window)
main_batch = pyglet.graphics.Batch()
bg_batch = pyglet.graphics.Batch()
background = []
pipes = []
pipesUp = []
ground = []
mobs_to_collide = []

winsize = window.get_size()
print("Winsize", winsize)
player_x_start = (winsize[0]/3)
player_y_start = (winsize[1]/2)

gravity = 10

def load_assets():
    global music, playerImage, backgroundImage, groundImage, pipeImageUp, pipeImageDown, jumpsnd
    # sounds
    music = pyglet.resource.media('assets/snd/star60.wav')
    jumpsnd = pyglet.resource.media('assets/snd/wing.wav')
    # images
    playerImage = pyglet.resource.image('assets/img/yellowbird-midflap.png')
    backgroundImage = pyglet.resource.image('assets/img/background.png')
    groundImage =  pyglet.resource.image('assets/img/base.png')
    pipeImageUp = pyglet.resource.image('assets/img/pipe-green.png')
    pipeImageDown = pyglet.resource.image('assets/img/pipe-green.png')
    


def init():
    # music = pyglet.resource.media('assets/snd/star60.wav')
    load_assets()
    # music.play()
    drawBackground(background, backgroundImage)
    drawPipes(groundImage, pipeImageUp, pipeImageDown)
    drawPlayer(playerImage)

def drawPlayer(playerImage):
    global player
    # playerImage = pyglet.resource.image('assets/img/yellowbird-midflap.png')
    player = pyglet.sprite.Sprite(playerImage, batch=main_batch)
    player.x = 0
    player.y = 0
    player.update(player_x_start, player_y_start)

def drawBackground(background, backgroundImage):
    # global background
    # backgroundImage = pyglet.resource.image('assets/img/background.png')
    backgroundFillAmount = int((window.get_size()[0]/backgroundImage.width)+2)
    for i in range(backgroundFillAmount):
        background.append(pyglet.sprite.Sprite(backgroundImage, (i*backgroundImage.width), backgroundImage.y, batch=bg_batch))



def drawPipes(groundImage, pipeImageUp, pipeImageDown):
    global pipes, pipesUp, ground
    # Draw background
    backgroundFillAmount = int((window.get_size()[0]/(backgroundImage.width/2))+2)
    # print(backgroundFillAmount)
    for i in range (backgroundFillAmount):
        heightMod = random.randrange(0, 200)
        pipesUp.append(pyglet.sprite.Sprite(pipeImageUp, ((i*2*100)+pipeImageUp.width), 550+heightMod, batch=main_batch))
        pipes.append(pyglet.sprite.Sprite(pipeImageDown, (i*2*100), -200+heightMod , batch=main_batch))
    for j in pipesUp:
        j.update(j.x, rotation=180)
    pipes = (pipes + pipesUp) 
    for k in pipes:
        print ("pipeX: ", k.x)
        # print((pipes))
    # pipesx = [pipes.index(), pipes[pipes.index()].x]
    # print(pipesx)
 
    # Draw groundelement
    groundFillAmount = int((window.get_size()[0]/groundImage.width)+3)
    # print("groundFillAmount", groundFillAmount)
    for i in range (groundFillAmount):
        ground.append(pyglet.sprite.Sprite(groundImage, (i*backgroundImage.width), (backgroundImage.y-50 ), batch=main_batch))
        # print (backgroundImage.height)

def distance_to_closest_pipe_x(player_x):
    global pipes

    pipesx = []
    pipesx=(int(pipe.x-player_x) for pipe in pipes if (int(pipe.x-player_x) > 0))
    newlist = list(pipesx)
    return min(newlist)

# def check_collision(self):
#     for i in list_of_mobs:
#         if self.distance(i) < (self.width/2 + i.width/2):
#             return True

# def check_collision(self):
#     global mobs_to_collide, pipes
#     if mobs_to_collide == []:
#         mobs_to_collide = pipes[:]
#     if self in mobs_to_collide:
#         mobs_to_collide.remove(self)
#     for i in mobs_to_collide:
#         if self.distance(i) < (self.width/2 + i.width/2):
#             return True

def jump():
    global jumpsnd, gravity
    jumpsnd = pyglet.resource.media('assets/snd/wing.wav')
    jumpsnd.play()
    gravity = gravity - 15

def update(dt):
    global gravity, ground, pipes, background
    player.y = player.y - (gravity)
    if (gravity < 11):  
        gravity = gravity + 1
    # print("gravity is: ", gravity)
    player.rotation = gravity*2

    # # failstate 1
    # if (player.y < 0) or (player.y > 480):
    #     pyglet.app.exit()

    # move ground, pipes and background to right after going offscreen
    for i in ground:
        i.x = i.x - 2  
        if (i.x < -i.width): # 288 width
            i.x = winsize[0]
    for j in pipes:
        j.x = j.x - 1
        if (j.x < -j.width): # 52 width
            j.x = winsize[0]+j.width
    target = distance_to_closest_pipe_x(player.x)
    print(target)
    if target == 1:
        print('hit')

    for k in background:
        k.x = k.x - .5
        if (k.x < -k.width): # 288 width
            k.x = winsize[0]


@window.event
def on_key_press(symbol, modifiers):
    global player_x, player_y
    if symbol == key.SPACE:
        print('Jump key was pressed')
        jump()

@window.event
def on_draw():
    window.clear()
    bg_batch.draw()
    main_batch.draw()
    fps_display.draw()

if __name__ == "__main__":
    init()

    pyglet.clock.schedule_interval(update, 1/60.0)
    pyglet.app.run()

# # debug
# event_logger = pyglet.window.event.WindowEventLogger()
# window.push_handlers(event_logger)