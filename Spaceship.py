# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0.5
ang_vel = 0.0
ship_x = 0
friction = 0.03
thrust = 0.25
rocks = set()
missiles = set()
explosion_group = set()
started = False

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def draw(self,canvas):
        #canvas.draw_circle(self.pos, self.radius, 1, "White", "White")
        canvas.draw_image(self.image, [self.image_center[0] + ship_x, self.image_center[1]], self.image_size, self.pos, self.image_size, self.angle)

    def update(self):
        #self.image_center[0] += 90
        self.angle += self.angle_vel
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        if self.pos[0] >= WIDTH or self.pos[0] < 0:
            self.pos[0] += WIDTH
            self.pos[0] %= WIDTH
        if self.pos[1] >= HEIGHT or self.pos[1] < 0:
            self.pos[1] += HEIGHT
            self.pos[1] %= HEIGHT
        
        self.vel[0] *= (1 - friction)
        self.vel[1] *= (1 - friction)
        self.direction = angle_to_vector(self.angle)
        if self.thrust == True:
            self.vel[0] += thrust * self.direction[0]
            self.vel[1] += thrust * self.direction[1]
        
    def update_ang(self, ang_vel):
        self.angle_vel += ang_vel
    
    def update_thrust(self, val):
        self.thrust = val
    
    def get_position(self):
        return self.pos

    def get_radius(self):
        return self.radius
    
    def shoot(self):
        global missiles
        face = angle_to_vector(self.angle)
        mis_pos = [self.pos[0] + 35 * face[0], self.pos[1] + 35 * face[1]]
        mis_vel = [self.vel[0] + 6 * face[0], self.vel[1] + 6 * face[1]]
        a_missile = Sprite(mis_pos, mis_vel, 0, 0, missile_image, missile_info, missile_sound)
        missiles.add(a_missile)
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def get_position(self):
        return self.pos

    def get_radius(self):
        return self.radius
    
    def draw(self, canvas):
        if self.animated == False:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
        else: 
            canvas.draw_image(self.image, [self.image_center[0] + (self.age % self.lifespan) * self.image_size[0], self.image_center[1]], self.image_size, self.pos, self.image_size, self.angle)
    
    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.angle += self.angle_vel
        self.age += 1
        if self.pos[0] >= WIDTH or self.pos[0] < 0:
            self.pos[0] += WIDTH
            self.pos[0] %= WIDTH
        if self.pos[1] >= HEIGHT or self.pos[1] < 0:
            self.pos[1] += HEIGHT
            self.pos[1] %= HEIGHT
        if self.age > self.lifespan:
            return True
        return False
    
    def collide(self, other_obj):
        global explosion_group
        other_pos = other_obj.get_position()
        if dist(self.pos, other_pos) <= self.radius + other_obj.get_radius():
            an_explosion = Sprite([(self.pos[0] + other_pos[0]) // 2 , (self.pos[1] + other_pos[1]) // 2], [0,0], 0, 0, explosion_image, explosion_info, explosion_sound)
            explosion_group.add(an_explosion)
            return True
        return False
           
def group_collide(grp, other_obj):
    rem = set()
    for inst in grp:
        if inst.collide(other_obj):
            rem.add(inst)
    if len(rem) == 0:
        return False
    grp.difference_update(rem)
    return True

def group_group_collide(grp1, grp2):
    rem = set()
    for inst in grp1:
        if group_collide(grp2, inst):
            rem.add(inst)
    grp1.difference_update(rem)
    return len(rem)
    
def keydown(key):
    global ship_x, ang_vel
    if key==simplegui.KEY_MAP["up"]:
        ship_x = 90
        ship_thrust_sound.play()
        my_ship.update_thrust(True)
    elif key==simplegui.KEY_MAP["left"]:
        my_ship.update_ang(-0.05)
    elif key==simplegui.KEY_MAP["right"]:
        my_ship.update_ang(0.05)
    elif key == simplegui.KEY_MAP["space"]:
        my_ship.shoot()
   
def keyup(key):
    global ship_x, ang_vel
    if key==simplegui.KEY_MAP["up"]:
        ship_x = 0
        my_ship.update_thrust(False)
        ship_thrust_sound.pause()
        ship_thrust_sound.rewind()
    elif key==simplegui.KEY_MAP["left"]:
        my_ship.update_ang(0.05)
    elif key==simplegui.KEY_MAP["right"]:
        my_ship.update_ang(-0.05)

def process_sprite_group(grp, canvas):
    rem = set()
    for inst in grp:
        inst.draw(canvas)
    for inst in grp:
        if inst.update():
            rem.add(inst)
    grp.difference_update(rem)
    
def draw(canvas):
    global time, lives, score, rocks, missiles, started
    
    # animiate background
    time += 1
    center = debris_info.get_center()
    size = debris_info.get_size()
    wtime = (time / 8) % center[0]
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, [center[0] - wtime, center[1]], [size[0] - 2 * wtime, size[1]], 
                                [WIDTH / 2 + 1.25 * wtime, HEIGHT / 2], [WIDTH - 2.5 * wtime, HEIGHT])
    canvas.draw_image(debris_image, [size[0] - wtime, center[1]], [2 * wtime, size[1]], 
                                [1.25 * wtime, HEIGHT / 2], [2.5 * wtime, HEIGHT])
    canvas.draw_text("Lives", (50, 50), 24, "White")
    canvas.draw_text("Score", (700, 50), 24, "White")
    canvas.draw_text(str(lives), (50, 80), 24, "White")
    canvas.draw_text(str(score), (700, 80), 24, "White")
    
    if lives <=0:
        started = False
        rocks.difference_update(rocks)
        missiles.difference_update(missiles)
        explosion_group.difference_update(explosion_group)
    else:
        if group_collide(rocks, my_ship):
            lives -= 1
        count = group_group_collide(missiles, rocks)
        score += count * 10
        my_ship.draw(canvas)
        process_sprite_group(rocks, canvas)
        process_sprite_group(missiles, canvas)
        process_sprite_group(explosion_group, canvas)
        # update ship and sprites
        my_ship.update()
            
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], splash_info.get_size())

def click(pos):
    global started, lives, score
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True
        lives = 3
        score = 0
        soundtrack.rewind()
        soundtrack.play()
        
# timer handler that spawns a rock    
def rock_spawner():
    global rocks, my_ship
    if len(rocks) >= 12:
        return
    if started:
        new_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
        OK = False
        while not OK:
            if dist(new_pos, my_ship.get_position()) >= asteroid_info.get_radius() + my_ship.get_radius() + 20:
                OK = True
            if not OK:
                new_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
        new_vel = [random.choice([1, -1]) * random.random(), random.choice([1, -1]) * random.random()]
        a_rock = Sprite( new_pos, new_vel, 0, random.choice([0.1, -0.1]) * random.random(), asteroid_image, asteroid_info)
        rocks.add(a_rock)
    
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(click)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
