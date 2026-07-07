import pygame as p
from sys import exit
import random

class Player1(p.sprite.Sprite):
    def __init__(self):
        super().__init__()  # just a pygame initialization
        player_walk1 = p.image.load('graphics/player/player_walk_1.png').convert_alpha()
        player_walk2 = p.image.load('graphics/player/player_walk_2.png').convert_alpha()
        player_walk1_imp = p.image.load('graphics/player/player_walk_1_impervious.png').convert_alpha()
        player_walk2_imp = p.image.load('graphics/player/player_walk_2_impervious.png').convert_alpha()
        self.player_walk = [player_walk1, player_walk2]
        self.player_walk_impervious = [player_walk1_imp,player_walk2_imp]
        self.player_index = 0
        self.player_jump = p.image.load('graphics/player/jump.png').convert_alpha()
        self.player_jump_imp = p.image.load('graphics/player/jump_impervious.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (200,300))
        self.gravity = 0
        self.velocity = 0
        self.dash_cooldown = 1.7
        self.impervious_cooldown = 0
        self.dash_right = True
        self.dash_sick = False
        self.is_impervious = False
        self.warning_played = True

        self.jump_sound = p.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.2)
        self.dash_sound = p.mixer.Sound('audio/dash.mp3')
        self.dash_sound.set_volume(0.7)
        self.upgrade_sound = p.mixer.Sound('audio/upgrade.mp3')
        self.upgrade_sound.set_volume(0.4)
        self.warning_sound = p.mixer.Sound('audio/upgrade_warning.mp3')
        self.warning_sound.set_volume(0.25)

    def player_input(self):
        if abs(self.velocity) == 3:
            self.velocity = 0

        keys = p.key.get_pressed()
        if keys[p.K_UP] and self.rect.bottom >= 300:
            self.gravity = -13
            self.jump_sound.play()
        if keys[p.K_LEFT] and self.rect.left >= 0 and self.velocity > -4:
            self.velocity = -3
            self.dash_right = False
            self.dash_sick = False
        if keys[p.K_RIGHT] and self.rect.right <= 800 and self.velocity < 4:
            self.velocity = 3
            self.dash_right = True
            self.dash_sick = False
        if keys[p.K_DOWN] and self.rect.bottom < 300:
            self.gravity += 15
        if keys[p.K_RCTRL] and self.dash_cooldown <= 0:
            self.dash_cooldown = 1.5
            self.dash_sick = True
            self.gravity = 0
            self.dash_sound.play()
            if self.dash_right:
                self.velocity += 10
            else:
                self.velocity -= 10
        if keys[p.K_RALT] and self.impervious_cooldown <= 0:
            self.upgrade_sound.play()
            self.is_impervious = True
            self.warning_played = False
            self.impervious_cooldown = 8
        
        return self.is_impervious

    def apply_gravity(self):
        if self.velocity < 4 and self.velocity > -4:
            self.gravity += 0.55
            self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300
            self.gravity = 0
    def move(self):
        self.rect.x += self.velocity
        if self.rect.left < 0:
            self.velocity = 0
            self.rect.left = 0
        if self.rect.right > 800:
            self.velocity = 0
            self.rect.right = 800

    def slow(self):
        if self.dash_sick and self.velocity != 0:
            if self.velocity > 0:
                self.velocity -= 0.4
            if self.velocity < 0:
                self.velocity += 0.4

        else:
            if self.velocity > 4:
                self.velocity -= 0.4
            if self.velocity < -4:
                self.velocity += 0.4

    def tick_clocks(self):
        self.dash_cooldown -= 0.04
        self.impervious_cooldown -= 1 / 60
        if self.impervious_cooldown <= 6 and not self.warning_played:
            self.warning_sound.play()
            self.warning_played = True
        if self.impervious_cooldown <= 5:
            self.is_impervious = False



        if self.rect.bottom < 300 and not self.is_impervious:
            self.image = self.player_jump
        elif self.rect.bottom < 300:
            self.image = self.player_jump_imp
        else:
            self.player_index += 0.1
            if self.player_index >= 1:
                self.player_index = 0
            if self.is_impervious:
                self.image = self.player_walk_impervious[round(self.player_index)]
            else:
                self.image = self.player_walk[round(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.move()
        self.slow()
        self.tick_clocks()

    def death(self):
        self.rect = self.image.get_rect(midbottom = (200,300))
        self.velocity = 0
        self.gravity = 0
        self.dash_right = True
        self.is_impervious = False
        self.impervious_cooldown = 0
        return self.is_impervious

class Player2(p.sprite.Sprite):
    def __init__(self):
        super().__init__()  # just a pygame initialization
        player_walk1 = p.image.load('graphics/player/player_walk_3.png').convert_alpha()
        player_walk2 = p.image.load('graphics/player/player_walk_4.png').convert_alpha()       
        player_walk1_imp = p.image.load('graphics/player/player_walk_3_impervious.png').convert_alpha()
        player_walk2_imp = p.image.load('graphics/player/player_walk_4_impervious.png').convert_alpha()        
        self.player_walk = [player_walk1, player_walk2]
        self.player_walk_impervious = [player_walk1_imp,player_walk2_imp]
        self.player_index = 0
        self.player_jump = p.image.load('graphics/player/jump2.png').convert_alpha()
        self.player_jump_imp = p.image.load('graphics/player/jump2_impervious.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (300,300))
        self.gravity = 0
        self.velocity = 0
        self.dash_cooldown = 1.7
        self.dash_right = True
        self.dash_sick = False
        self.impervious_cooldown = 0
        self.dash_right = True
        self.dash_sick = False
        self.is_impervious = False
        self.warning_played = True


        self.jump_sound = p.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.2)
        self.dash_sound = p.mixer.Sound('audio/dash.mp3')
        self.dash_sound.set_volume(0.7)
        self.upgrade_sound = p.mixer.Sound('audio/upgrade.mp3')
        self.upgrade_sound.set_volume(0.4)
        self.warning_sound = p.mixer.Sound('audio/upgrade_warning.mp3')
        self.warning_sound.set_volume(0.25)

    def player_input(self):
        if abs(self.velocity) == 3:
            self.velocity = 0

        keys = p.key.get_pressed()
        if keys[p.K_w] and self.rect.bottom >= 300:
            self.gravity = -13
            self.jump_sound.play()
        if keys[p.K_a] and self.rect.left >= 0 and self.velocity > -4:
            self.velocity = -3
            self.dash_right = False
            self.dash_sick = False
        if keys[p.K_d] and self.rect.right <= 800 and self.velocity < 4:
            self.velocity = 3
            self.dash_right = True
            self.dash_sick = False
        if keys[p.K_s] and self.rect.bottom < 300:
            self.gravity += 15
        if keys[p.K_SPACE] and self.dash_cooldown <= 0:
            self.dash_cooldown = 1.5
            self.dash_sick = True
            self.gravity = 0
            self.dash_sound.play()
            if self.dash_right:
                self.velocity += 10
            else:
                self.velocity -= 10
        if keys[p.K_LSHIFT] and self.impervious_cooldown <= 0:
            self.upgrade_sound.play()
            self.is_impervious = True
            self.warning_played = False
            self.impervious_cooldown = 8
        
        return self.is_impervious

    def apply_gravity(self):
        if self.velocity < 4 and self.velocity > -4:
            self.gravity += 0.55
            self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300
            self.gravity = 0
    def move(self):
        self.rect.x += self.velocity
        if self.rect.left < 0:
            self.velocity = 0
            self.rect.left = 0
        if self.rect.right > 800:
            self.velocity = 0
            self.rect.right = 800

    def slow(self):
        if self.dash_sick and self.velocity != 0:
            if self.velocity > 0:
                self.velocity -= 0.4
            if self.velocity < 0:
                self.velocity += 0.4

        else:
            if self.velocity > 4:
                self.velocity -= 0.4
            if self.velocity < -4:
                self.velocity += 0.4

    def tick_clocks(self):
        self.dash_cooldown -= 0.04
        self.impervious_cooldown -= 1 / 60
        if self.impervious_cooldown <= 6 and not self.warning_played:
            self.warning_sound.play()
            self.warning_played = True
        if self.impervious_cooldown <= 5:
            self.is_impervious = False

        if self.rect.bottom < 300 and not self.is_impervious:
            self.image = self.player_jump
        elif self.rect.bottom < 300:
            self.image = self.player_jump_imp
        else:
            self.player_index += 0.1
            if self.player_index >= 1:
                self.player_index = 0
            if self.is_impervious:
                self.image = self.player_walk_impervious[round(self.player_index)]
            else:
                self.image = self.player_walk[round(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.move()
        self.slow()
        self.tick_clocks()
    
    def death(self):
        self.rect = self.image.get_rect(midbottom = (300,300))
        self.velocity = 0
        self.gravity = 0
        self.dash_right = True
        self.is_impervious = False
        self.impervious_cooldown = 0
        return self.is_impervious

class Obstacle(p.sprite.Sprite):
    def __init__(self,type,speed):
        super().__init__()
        
        if type == 'fly':
            self.fly = True
            fly_1 = p.image.load('graphics/fly/fly1.png').convert_alpha()
            fly_2 = p.image.load('graphics/fly/fly2.png').convert_alpha()
            self.frames = [fly_1,fly_2]
            y_pos = 150
        else:
            self.fly = False
            snail_1 = p.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_2 = p.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_1,snail_2]
            y_pos = 300
        
        self.speed = speed
        self.spawn_from_edge = random.randint(900,1200)
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(bottomleft = (self.spawn_from_edge, y_pos))

    def spawning_distance(self):
        self.spawn_from_edge = random.randint(900,1200)

    def animation_state(self):
        if self.fly and self.animation_index < 1:
            self.animation_index +=0.23
        elif not self.fly and self.animation_index < 1:
            self.animation_index += 0.08
        if self.animation_index > 1:
            self.animation_index = 0
        self.image = self.frames[round(self.animation_index)]

    def move_obstacles(self):
        self.rect.x -= self.speed
        self.destroy()

    def update(self):
        self.spawning_distance()
        self.animation_state()
        self.move_obstacles()
    
    def destroy(self):
        if self.rect.right < 0:
            self.kill()


def display_score(high_score):
    current_time = p.time.get_ticks() - start_time

    score = round(current_time / 1000)

    if score > high_score:
        high_score = score

    score_surface = test_font.render(f'Score: {score}',False,(64,64,64))
    score_rectangle = score_surface.get_rect(bottomleft = (20,50))
    win.blit(score_surface,score_rectangle)

    highscore_surface = test_font.render(f'High Score: {high_score}',False,(64,64,64))
    highscore_rectangle = score_surface.get_rect(bottomleft = (20,80))
    win.blit(highscore_surface,highscore_rectangle)
    return score,high_score

def collision_sprite():
    if p.sprite.spritecollide(player1.sprite,obstacle_group,True) and not is_impervious_1:
        obstacle_group.empty()
        return False
    if p.sprite.spritecollide(player2.sprite,obstacle_group,True) and not is_impervious_2:
        obstacle_group.empty()
        return False
    return True
    


p.init() # start up pygame

# create display surface
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 960
GAME_WIDTH = 800
GAME_HEIGHT = 600

screen = p.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT), p.RESIZABLE)
win = p.Surface((GAME_WIDTH,GAME_HEIGHT))
p.display.set_caption('Runner game by Ethan')
clock = p.time.Clock()
test_font = p.font.Font('font/pixeltype.ttf',50)
game_active = 'start'
start_time = 0
high_score = 0
score = 0
bg_music = p.mixer.Sound('audio/music.wav')
bg_music.set_volume(0.1)
bg_music.play(loops = -1)
play_death_sound = True
death_sound = p.mixer.Sound('audio/death_sfx.mp3')
death_sound.set_volume(0.1)
is_impervious_1 = False
is_impervious_2 = False

sky_surface = p.image.load('graphics/sky.png').convert()
ground_surface2 = p.image.load('graphics/ground.png').convert()

text_surface = test_font.render('temporary', False, (64,64,64))
text_rectangle = text_surface.get_rect(midtop = (400,50))

player_surface = p.image.load('graphics/player/player_walk_1.png').convert_alpha()


# Groups
player1 = p.sprite.GroupSingle()
player1.add(Player1())

player2 = p.sprite.GroupSingle()
player2.add(Player2())

obstacle_group = p.sprite.Group()


# Timer
obstacle_timer = p.USEREVENT + 1
p.time.set_timer(obstacle_timer, 1500)


while True:
    win_scaled = p.transform.scale(win, (WINDOW_WIDTH,WINDOW_HEIGHT))
    
    for event in p.event.get():
        if event.type == p.QUIT:
            p.quit()
            exit()
        if game_active == True:
            if event.type == obstacle_timer and random.randint(0,3) >= 1:
                obstacle_group.add(Obstacle('snail',random.uniform(3,4.5)))
            elif event.type == obstacle_timer:
                obstacle_group.add(Obstacle('fly',random.uniform(4,6)))

        else: 
            if event.type == p.KEYDOWN and event.key == p.K_SPACE:  
                game_active = True
                start_time = p.time.get_ticks()
                play_death_sound = True
        if event.type == p.VIDEORESIZE:
            screen = p.display.set_mode((event.w,event.h), p.RESIZABLE)


# Start up prompt    
    if game_active == 'start':
        screen.blit(win_scaled,(0,0))
        win.fill("#357892")
        name_surface = test_font.render('Pixel Runner', False, "#69cfd3")
        name_rectangle = name_surface.get_rect(midtop = (400,75))
        win.blit(name_surface,name_rectangle)

        prompt_surface = test_font.render('Press space to run', False, "#69cfd3")
        prompt_rectangle = prompt_surface.get_rect(midtop = (400,300))
        win.blit(prompt_surface,prompt_rectangle)

        death_player_surface = p.image.load('graphics/player/player_stand.png').convert_alpha()
        death_player_surface = p.transform.rotozoom(death_player_surface,0,2)
        death_player_rectangle = death_player_surface.get_rect(center = (400,200))
        win.blit(death_player_surface,death_player_rectangle)

# Game loop
    elif game_active == True:
    # place surface on surface
        
        screen.blit(win_scaled,(0,0))
        win.blit(sky_surface,(0,0))
        win.blit(ground_surface2,(0,300))

    # Player
        
        player1.draw(win)
        player1.update()
        is_impervious_1 = player1.sprite.player_input()
        print(is_impervious_1)

        player2.draw(win)
        player2.update()
        is_impervious_1 = player1.sprite.player_input()

        obstacle_group.draw(win)
        obstacle_group.update()

        score,high_score = display_score(high_score)
        
        if 1500-3*score > 870 and score % 7 == 0: 
            p.time.set_timer(obstacle_timer, 1500-int(3*score)) 

        game_active = collision_sprite()

# Death screen
    else:
        screen.blit(win_scaled,(0,0))
        
        is_impervious_1 = player1.sprite.death()
        is_impervious_2 = player2.sprite.death()

        if play_death_sound:
            death_sound.play()      
            play_death_sound = False
        obstacle_rect_list = []
        player_rectangle = player_surface.get_rect(midbottom = (120,300))
        player_velocity = 0

        win.fill("#357892")
        name_surface = test_font.render('Pixel Runner', False, "#69cfd3")
        name_rectangle = name_surface.get_rect(midtop = (400,75))
        win.blit(name_surface,name_rectangle)

        prompt_surface = test_font.render('Press space to run', False, "#69cfd3")
        prompt_rectangle = prompt_surface.get_rect(midtop = (400,300))
        win.blit(prompt_surface,prompt_rectangle)

        score_message = test_font.render(f'Your score: {score}',False, "#69cfd3")
        death_score_rectangle = score_message.get_rect(midtop = (400,30))
        win.blit(score_message,death_score_rectangle)

        death_player_surface = p.image.load('graphics/player/player_stand.png').convert_alpha()
        death_player_surface = p.transform.rotozoom(death_player_surface,90,2)
        death_player_rectangle = death_player_surface.get_rect(center = (400,200))
        win.blit(death_player_surface,death_player_rectangle)

    

# update everything
    p.display.update()
    clock.tick(60)