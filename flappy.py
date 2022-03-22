import pyglet
from pyglet.window import key
from pyglet.window import mouse

window = pyglet.window.Window()
main_batch = pyglet.graphics.Batch()
bg_batch = pyglet.graphics.Batch()
game_objects = []
player = None

def init():
    # Set up window
    fps_display = pyglet.window.FPSDisplay(window=window)
    # game_objects = player

    # load assets
    jumpsnd = pyglet.resource.media('assets/snd/wing.wav')
    drawBackground()
    drawPlayer()


# sound example
# sound = pyglet.resource.media('assets/audio/hit.wav', streaming=False)
# sound.play()
music = pyglet.resource.media('assets/snd/star60.wav')
music.play()

def drawPlayer():
    global player
    player.dx = 1 #00.0
    playerImage = pyglet.resource.image('assets/img/yellowbird-midflap.png')
    player = pyglet.sprite.Sprite(playerImage, batch=main_batch)

def drawBackground():
    backgroundImage = pyglet.resource.image('assets/img/background.png')
    background = pyglet.sprite.Sprite(backgroundImage, batch=bg_batch)
    winx = window.get_size()[1]
    bginfo = background.image.get_image_data()
    windowfit = int((winx/bginfo.width)+2)
    for i in range(windowfit):
        newwinwidth = (i*bginfo.width)
    #     background.blit(newwinwidth,0)

# # debug
# event_logger = pyglet.window.event.WindowEventLogger()
# window.push_handlers(event_logger)

def jump():
    jumpsnd.play()
    player.sprite.Spriterotation(-10)


def update(dt):
    global player
    winx = window.get_size()[1]
    print (player.position)
    playx = player.position[0]
    while (player.position[0] < winx/3):
        player.x += player.dx * dt
        print(player.x)
        print(player.position[0])
        print(winx/3)
pyglet.clock.schedule_interval(update, 1/60.0)

# flappy = PhysicalObject(img)


@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.SPACE:
        print('Jump key was pressed')
        jump()

@window.event
def on_draw():
    window.clear()
    bg_batch.draw()
    main_batch.draw()



if __name__ == "__main__":
    init()

    pyglet.app.run()