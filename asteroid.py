import random
from if3_game.engine import Sprite, Game, Layer, Text
from pyglet import window, font
from math import cos, sin, radians

RESOLUTION = (800,600) #un tuple ; RESOLUTION tt en majuscules = une constante/ variable qui ne changera pas

MAXLIFE = 5

range_asteroids_lvl1 = 3
range_asteroids_lvl2 = 2
total_asteroids = range_asteroids_lvl1 + range_asteroids_lvl1 * range_asteroids_lvl2 + range_asteroids_lvl2 * range_asteroids_lvl2 * range_asteroids_lvl1

class BrilliantIdeasGame(Game):
    def __init__(self):
        super().__init__()
        
        self.game_won = False

        font.add_file("fonts/ankacoder_r.ttf")

        self.bg_layer = Layer()
        self.add(self.bg_layer)

        self.game_layer = Layer()
        self.add(self.game_layer)

        self.ui_layer = UILayer()
        self.add(self.ui_layer)

        self.bg = Sprite("images/epileptic_scope.gif", (0,0))
        self.bg_layer.add(self.bg)

        self.targetpatch = Sprite("images/targetpatch.png", (0,0))
        self.bg_layer.add(self.targetpatch)

        self.patch_overlay = Sprite("images/patch_overlay.png", (0,0))
        self.bg_layer.add(self.patch_overlay)

#        self.criticalsprite = Sprite("images/criticaldamage.png", (0,0))
#        self.ui_layer.add(self.criticalsprite)

        self.criticaltext = Text("CRITICAL DAMAGE. COVER.",
        (400, 300), 12, anchor="center", font_name="Anka/Coder")
        self.ui_layer.add(self.criticaltext)

        self.text = Text("THIS is an important mission.",
        (400, 30), 12, anchor="center", font_name="Anka/Coder")
        self.ui_layer.add(self.text)

        self.posttext = Text("THIS was an important mission.",
        (400,30), 12, anchor="center", font_name="Anka/Coder")
        self.ui_layer.add(self.posttext)

        self.gameover = Text("A life has gone. You failed.",
        (400, 560), 12, anchor="center", font_name="Anka/Coder")
        self.ui_layer.add(self.gameover)
        
        self.win = Text("A new life has born. You succeeded.",
        (400,568), 12, anchor="center", font_name="Anka/Coder")
        self.ui_layer.add(self.win)

        self.life = []
        for n in range(3):
            sprite = Sprite("images/life_anim.gif", (20 + 40*n, 20))
            self.ui_layer.add(sprite)
            self.life.append(sprite)

        self.spaceship = Spaceship()
        self.game_layer.add(self.spaceship)
        self.ui_layer.spaceship = self.spaceship

        for i in range(range_asteroids_lvl1):
            rx = random.randint(0, RESOLUTION[0])
            while rx > 200 and rx < 400:
                rx = random.randint(0, RESOLUTION[0])

            ry = random.randint(0, RESOLUTION[1])
            while ry > 200 and ry < 400:
                ry = random.randint(0, RESOLUTION[1])

            asteroid = Asteroid(
                (rx,ry),
                (random.randint(-100,100),
                random.randint(-100,100))
                )
            self.game_layer.add(asteroid)

    def update(self, dt):
        super().update(dt)
        
        for i in range(len(self.life)):
            if i < self.spaceship.lifes:
                self.life[i].opacity = 255
            else:
                self.life[i].opacity = 0
        
        if self.spaceship.lifes == 0:
            self.patch_overlay.opacity = 255
            self.gameover.opacity = 255
            self.text.opacity = 0
            self.posttext.opacity = 255
        else:
            self.patch_overlay.opacity = 0
            self.gameover.opacity = 0
            self.text.opacity = 255
            self.posttext.opacity = 0
        
        if Asteroid.hits == total_asteroids:
            self.game_won = True
            self.win.opacity = 255
            #print("You won.")
        else:
            self.game_won = False
            self.win.opacity = 0
        
        if self.spaceship.lifes == 1:
            self.bg.opacity = 255
            self.criticaltext.opacity = 255
        elif self.spaceship.lifes == 0:
            self.bg.opacity = 255
            self.criticaltext.opacity = 0
        else:
            self.bg.opacity = 0
            self.criticaltext.opacity = 0


class UILayer(Layer):

    def __init__(self):
        super().__init__()
        #self.spaceship = None

class SpaceItem(Sprite):
    def __init__(self, imagepath, position, anchor, speed=(0,0), rotation_speed=0):

        super().__init__(
            imagepath, position, anchor=anchor, collision_shape="circle")
        #anchor=anchor to force the argument to pass from child to parent
        self.speed = speed
        #if nothing is specified the speed will be (0,0) thus a still object
        self.rotation_speed = rotation_speed

    def update(self, dt):
    #dt = delta time/différence de temps (cf le casse-briques)
        super().update(dt)  #la méthode update = un callback
        #Position actuelle
        pos_x = self.position[0]
        pos_y = self.position[1]
        
        #Calcul du déplacement
        move = (self.speed[0] * dt, self.speed[1] * dt)
        
        #Application du déplacement
        pos_x += move[0]
        pos_y += move[1]

        #Correction de la position si on sort de l'écran
        if pos_x > RESOLUTION[0] + 16:
            pos_x = -32
        elif pos_x < -32:
            pos_x = RESOLUTION[0] + 16
        
        if pos_y > RESOLUTION[1] + 16:
            pos_y = -32
        elif pos_y < -32:
            pos_y = RESOLUTION[1] + 16
        
        #On bouge effectivement l'objet
        #self.position = (pos_x + move[0], pos_y + move[1])
        #C’ETAIT ÇA!!!!!!! :ragejoy:
        self.position = (pos_x, pos_y)

        #rotation management
        self.rotation += dt * self.rotation_speed
    
class Spaceship(SpaceItem):
    def __init__(
        self,
        imagepath="images/spaceship_anim.gif",
        position=(
            RESOLUTION[0]/2,
            RESOLUTION[1]/2
            ),
        anchor=(16,20),
        speed=(0,0),
        #rotation_speed=0,
        ):

        super().__init__(imagepath, position, anchor, speed)

        self.velocity = 0
        #self.acceleration = 0.05

        self.invulnerability = False

        self.chrono = 0

        self.lifes = 3
    
    def on_key_press(self, key, modifiers):
        if key == window.key.LEFT:
            self.rotation_speed -= 80
        if key == window.key.RIGHT:
            self.rotation_speed += 80
        
        if key == window.key.UP:
            self.velocity = 3
        if key == window.key.SPACE:
            self.spawn_bullet()
        
    def on_key_release(self, key, modifiers):
        if key == window.key.LEFT and self.rotation_speed < 0:
            self.rotation_speed = -20
        elif key == window.key.RIGHT and self.rotation_speed > 0:
            self.rotation_speed = 20
        elif key == window.key.UP:
            self.velocity = 0
        
    
    def spawn_bullet(self):
        bullet_velocity = 75
        sx = cos(radians(self.rotation)) * bullet_velocity 
        sy = -sin(radians(self.rotation)) * bullet_velocity

        anchor = (5,5)
        rotation_speed = 50

        bullet_speed = (self.speed[0] + sx, self.speed[1] + sy)

        x = cos(radians(self.rotation)) * 40
        y = -sin(radians(self.rotation)) * 40

        bullet_position = (self.position[0] + x, self.position[1])

        bullet = Bullet(bullet_position, anchor, bullet_speed, rotation_speed)
        self.layer.add(bullet)

    def on_collision(self, other):
        if isinstance(other, Asteroid):
            self.destroy()
    
    def destroy(self):
        if self.invulnerability == False:
            self.invulnerability = True
            self.lifes -= 1
            print(self.lifes)

            if self.lifes <= 0:
                print("FUCK YOU!")
                super().destroy()


    def update(self, dt):


        if self.invulnerability == True and self.chrono < 5 and self.lifes > 0:
            self.opacity = 125
            self.imagepath = "images/spaceshipthissmall2.png"
            self.chrono += dt
        else:
            self.opacity = 255
            self.chrono = 0
            self.invulnerability = False
            self.imagepath = "images/spaceship_anim.gif"

        dsx = cos(radians(self.rotation))*self.velocity
        dsy = -sin(radians(self.rotation))*self.velocity

        sx = self.speed[0] + dsx
        sy = self.speed[1] + dsy

        self.speed = (sx, sy)

        super().update(dt)
        #here the super() comes in later since we want to set the speed before starting the frame count

class Bullet(SpaceItem):
    def __init__(self, position, anchor, speed, rotation_speed):
        imagepath = "images/bulletcross_anim.gif"
        super().__init__(imagepath, position, anchor, speed, rotation_speed)
        self.life_time = 0
    
    def on_collision(self, other):
        if isinstance(other, Asteroid):
            self.destroy()
            other.destroy()

    def update(self, dt):
        super().update(dt)
        self.life_time += dt

        if self.life_time >= 4:
            self.destroy()

class Asteroid(SpaceItem):
    asteroid_counter = 0
    hits = 0
    
    def __init__(self, position, speed, level=3):
        Asteroid.asteroid_counter += 1
        
        self.level = level
        if level == 3:
            imagepath="images/brilliantideasanim128-2.gif"
            anchor = (64,64)
        elif level == 2:
            imagepath="images/brilliantideas64.gif"
            anchor = (32,32)
        else:
            imagepath="images/brilliantideas32.gif"
            anchor = (16,16)

        #self.anchor = anchor
        #ne pas faire ça, ça redéfinit anchor en cours de route et affecte la rotation
        
        rotation_speed = random.randint(25,60) #no need to make it an attribute
    
        super().__init__(
            imagepath, position, anchor, speed, rotation_speed)

    def destroy(self):
        if self.level > 1:
            for n in range(range_asteroids_lvl2):
                sx = random.randint(-300,300)
                sy = random.randint(-300,300)
                speed = (sx, sy)

                level = self.level-1

                asteroid = Asteroid(
                    self.position,
                    speed,
                    level=level)

                self.layer.add(asteroid)
            
        super().destroy()
        Asteroid.hits += 1
        if random.randint(1,5) == 1:
            getop = GetLost(self.position)
            self.layer.add(getop)
        # print(f"hit total {Asteroid.hits}.")
        # print(f"asteroids total {Asteroid.asteroid_counter}")
        # print(f"total asteroids {total_asteroids}")

    
    def update(self, dt):
        return super().update(dt)

class PowerUp(SpaceItem):
    def __init__(self,
        position,
        lifetime=3):
        self.lifetime = lifetime
        super().__init__(
            "images/getlost.gif",
            position,
            anchor=(8,8),
            speed=(random.randint(-50, 50), random.randint(-50,50)), rotation_speed=random.randint(80,200))
    
    def on_collision(self, other):
        if isinstance(other, Spaceship):
            self.apply_effect(other)
            self.destroy()

    def apply_effect(self, spaceship):
        pass

    def update(self, dt):
        super().update(dt)
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.destroy()

class GetLost(PowerUp):
    def __init__self(self, position):
        super.init(position, lifetime=10)
    
    def apply_effect(self, spaceship):
        if spaceship.lifes < MAXLIFE:
            spaceship.lifes += 1