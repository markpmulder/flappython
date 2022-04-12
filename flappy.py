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
points = 0
gameplay = True

winsize = window.get_size()
print("Winsize", winsize)
player_x_start = (winsize[0]/3)
player_y_start = (winsize[1]/2)

gravity = 10

def load_assets():
    global music, playerImage, backgroundImage, groundImage, pipeImageUp, pipeImageDown, jumpsnd, hitsound, pointsound, soundeffects
    # sounds 
    soundeffects = pyglet.media.Player()
    music = pyglet.media.load('assets/snd/star60.wav')
    jumpsnd = pyglet.media.load('assets/snd/wing.wav')
    hitsound = pyglet.media.load('assets/snd/hit.wav')
    pointsound = pyglet.media.load('assets/snd/point.wav')
    # images
    playerImage = pyglet.resource.image('assets/img/yellowbird-midflap.png')
    backgroundImage = pyglet.resource.image('assets/img/background.png')
    groundImage =  pyglet.resource.image('assets/img/base.png')
    pipeImageUp = pyglet.resource.image('assets/img/pipe-green.png')
    pipeImageDown = pyglet.resource.image('assets/img/pipe-green.png')

def init():
    global soundeffects
    # music = pyglet.resource.media('assets/snd/star60.wav')
    load_assets()
    soundeffects.play()
    drawBackground(background, backgroundImage)
    drawPipes(groundImage, pipeImageUp, pipeImageDown)
    drawPlayer(playerImage)

def drawPlayer(playerImage):
    global player
    player = pyglet.sprite.Sprite(playerImage, batch=main_batch)
    player.x = 0
    player.y = 0
    player.update(player_x_start, player_y_start)

def drawBackground(background, backgroundImage):
    backgroundFillAmount = int((window.get_size()[0]/backgroundImage.width)+2)
    for i in range(backgroundFillAmount):
        background.append(pyglet.sprite.Sprite(backgroundImage, (i*backgroundImage.width), backgroundImage.y, batch=bg_batch))

def drawPipes(groundImage, pipeImageUp, pipeImageDown):
    global pipes, pipesUp, ground
    # Draw background
    backgroundFillAmount = int((window.get_size()[0]/(backgroundImage.width/2))+2)
    for i in range (backgroundFillAmount):
        heightMod = random.randrange(0, 200)
        pipesUp.append(pyglet.sprite.Sprite(pipeImageUp, (player_x_start+100+(i*2*100)+pipeImageUp.width), 550+heightMod, batch=main_batch))
        pipes.append(pyglet.sprite.Sprite(pipeImageDown, (player_x_start+100+i*2*100), -200+heightMod , batch=main_batch))
        # pipesUp.append(pyglet.sprite.Sprite(pipeImageUp, ((i*2*100)+pipeImageUp.width), 550+heightMod, batch=main_batch))
        # pipes.append(pyglet.sprite.Sprite(pipeImageDown, (i*2*100), -200+heightMod , batch=main_batch))
    for j in pipesUp:
        j.update(j.x, rotation=180)
    pipes = (pipes + pipesUp) 
    # Draw groundelement
    groundFillAmount = int((window.get_size()[0]/groundImage.width)+3)
    for i in range (groundFillAmount):
        ground.append(pyglet.sprite.Sprite(groundImage, (i*backgroundImage.width), (backgroundImage.y-50 ), batch=main_batch))

def distance_to_closest_pipe_x(player_x):
    global pipes
    # get x and y values of pipe closest to the player
    pipesx=(int(pipe.x-player_x) for pipe in pipes if (int(pipe.x-player_x) > 0))
    pipesy=(int(pipe.y) for pipe in pipes)
    pipesx_list = list(pipesx)
    pipesy_list = list(pipesy)
    # get get values of closest pipe to player
    minx = min(pipesx_list)
    minvalues = [minx, pipesy_list[pipesx_list.index(minx)]]
    return minvalues

def create_collision_area(startvalue):
    leftbound = startvalue[0] + player_x_start - (52/2)
    rightbound = startvalue[0] + player_x_start + (52/2)
    
    lowerpipe_lowerbound = startvalue[1]
    lowerpipe_upperbound = startvalue[1] + 288
    upperpipe_lowerbound = startvalue[1] +462
    upperpipe_upperbound = startvalue[1] + 288 + 462
    pipearea_up = [leftbound, rightbound, lowerpipe_lowerbound, lowerpipe_upperbound]
    pipearea_down = [leftbound, rightbound, upperpipe_lowerbound, upperpipe_upperbound]
    return [pipearea_up, pipearea_down] 

def check_collision(player_pos, collisionarea):
    if (collisionarea[0][0] < player_pos[0] < collisionarea[0][1]):
        if (collisionarea[0][2] < player_pos[1] < collisionarea[0][3]):
            collision = 'hit'
            return collision 
        elif (collisionarea[1][2] < player_pos[1] < collisionarea [1][3]):
            collision = 'hit'
            return collision
    elif (int(player_pos[0]) == int(collisionarea[1][1] - 52)):
        collision = 'point'
        return collision
    return None

def jump():
    global jumpsnd, gravity
    jumpsnd = pyglet.resource.media('assets/snd/wing.wav')
    jumpsnd.play()
    gravity = gravity - 15

def update_bgelements(element, speed):
    for i in element:
        i.x = i.x - speed
    if (i.x < -i.width):
        i.x = winsize[0]

def update_pipes(element, speed):
        for j in element:
            j.x = j.x - 1
        if (j.x < -j.width):
            j.x = winsize[0]+j.width

def fail_state(points):
    global gameplay
    print('Game Over! you\'ve gathered: ',points, ' points.')
    gameplay = False
    label = pyglet.text.Label('Hello, world', font_name='Times New Roman', font_size=36, x=window.width//2, y=window.height//2, anchor_x='center', anchor_y='center')
    print(window.width//2)
    print(window.height//2)
    label.draw()


def update(dt):
    global gravity, ground, pipes, background, hitsound, pointsound, soundeffects, gameplay, points

    if gameplay == True:
        # gravity
        player.y = player.y - (gravity)
        if (gravity < 11):  
            gravity = gravity + 1
        player.rotation = gravity*2
        # # move ground, pipes and background to right after going offscreen
        # update_bgelements(ground, 2) # 288 width
        # update_bgelements(background, 0.5) # 288 width
        # update_pipes(pipes, 1) # 52 width
        for i in ground:
            i.x = i.x - 2  
            if (i.x < -i.width): # 288 width
                i.x = winsize[0]
        for j in pipes:
            j.x = j.x - 1
            if (j.x < -j.width): # 52 width
                j.x = winsize[0] + j.width
        for k in background:
            k.x = k.x - .5
            if (k.x < -k.width): # 288 width
                k.x = winsize[0]

        # collision # get x value of closest pipe x and y value of that pipe # create boundary over that pipe # check if player is in that pipe
        minvalues = distance_to_closest_pipe_x(player.x)
        collisionarea = create_collision_area(minvalues) 
        player_pos = [player.x, player.y]
        collision = check_collision(player_pos, collisionarea)

        # collision handling
        if collision == 'hit':
            print('hit')   
            soundeffects.queue(hitsound)
            fail_state(points)
        elif collision == 'point':
            points = points + 1 
            print('point')
            soundeffects.queue(pointsound)

        # failstate 1
        if (player.y < 0) or (player.y > 480):
            fail_state(points)
    elif gameplay == False:
        gravity = 10
        player.y = player.y - (gravity)
        player.rotation += 10

@window.event
def on_key_press(symbol, modifiers):
    global player_x, player_y
    if gameplay == True:  
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