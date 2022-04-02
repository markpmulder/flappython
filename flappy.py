import pyglet
from pyglet.window import key
from pyglet.window import mouse

window = pyglet.window.Window()
fps_display = pyglet.window.FPSDisplay(window=window)
main_batch = pyglet.graphics.Batch()
bg_batch = pyglet.graphics.Batch()
background = []
pipes = []

winsize = window.get_size()
player_x_start = (winsize[0]/3)
player_y_start = (winsize[1]/2)

gravspeed = 15

def load_assets():
    global music, playerImage, backgroundImage, groundImage, pipeImage, jumpsnd
    music = pyglet.resource.media('assets/snd/star60.wav')
    playerImage = pyglet.resource.image('assets/img/yellowbird-midflap.png')
    backgroundImage = pyglet.resource.image('assets/img/background.png')
    groundImage =  pyglet.resource.image('assets/img/base.png')
    pipeImage = pyglet.resource.image('assets/img/pipe-green.png')
    jumpsnd = pyglet.resource.media('assets/snd/wing.wav')


def init():
    # music = pyglet.resource.media('assets/snd/star60.wav')
    load_assets()
    # music.play()
    drawBackground(background, backgroundImage)
    drawPipes(groundImage, pipeImage)
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
    backgroundMultiplier = int((window.get_size()[0]/backgroundImage.width)+1)
    for i in range(backgroundMultiplier):
        background.append(pyglet.sprite.Sprite(backgroundImage, (i*backgroundImage.width), backgroundImage.y, batch=bg_batch))

def drawPipes(groundImage, pipeImage):
    global pipes, ground
    backgroundMultiplier = int((window.get_size()[0]/(backgroundImage.width/2))+1)
    print(backgroundMultiplier)
    for i in range (backgroundMultiplier):
        pipes.append(pyglet.sprite.Sprite(pipeImage, (i*2*100), -200, batch=main_batch))
    ground = pyglet.sprite.Sprite(groundImage, 0, -50, batch=main_batch)

def jump():
    global jumpsnd
    jumpsnd = pyglet.resource.media('assets/snd/wing.wav')
    jumpsnd.play()
    player.y = player.y + ((gravspeed**2))
    # player.sprite.Spriterotation(-10)


def update(dt):
    # player.x += player.x * dt
    player.y = player.y - ((gravspeed**2)*dt)
    print(player.y)
    player.rotation = abs(player.y)
    # player.y = player.y - (gravspeed*(dt**2))


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