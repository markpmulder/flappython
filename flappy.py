import pyglet
from pyglet.window import key
from pyglet.window import mouse

window = pyglet.window.Window()
fps_display = pyglet.window.FPSDisplay(window=window)
main_batch = pyglet.graphics.Batch()
bg_batch = pyglet.graphics.Batch()
game_objects = []
background = []

winsize = window.get_size()
player_x_start = (winsize[0]/3)
player_y_start = (winsize[1]/2)

gravspeed = 10

def init():
    music = pyglet.resource.media('assets/snd/star60.wav')
    music.play()
    drawBackground()
    drawPlayer()

def drawPlayer():
    global player
    playerImage = pyglet.resource.image('assets/img/yellowbird-midflap.png')
    player = pyglet.sprite.Sprite(playerImage, batch=main_batch)
    player.x = 0
    player.y = 0
    player.update(player_x_start, player_y_start)

def drawBackground():
    global background
    backgroundImage = pyglet.resource.image('assets/img/background.png')
    backgroundMultiplayer = int((window.get_size()[0]/backgroundImage.width)+1)
    for i in range(backgroundMultiplayer):
        background.append(pyglet.sprite.Sprite(backgroundImage, (i*backgroundImage.width), backgroundImage.y, batch=bg_batch))

def jump():
    global jumpsnd, dt
    jumpsnd = pyglet.resource.media('assets/snd/wing.wav')
    jumpsnd.play()
    player.y = player.y + ((gravspeed**2)*dt)
    # player.sprite.Spriterotation(-10)


def update(dt):
    # player.x += player.x * dt
    player.y = player.y - ((gravspeed**2)*dt)
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