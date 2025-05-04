import pgzrun
from random import randint
from pygame import Rect

WIDTH = 800
HEIGHT = 480

# Estados do jogo
game_started = False
sound_on = True
fade_alpha = 255
gravity = 1
jump_strength = -22
max_lives = 3

# Sprites
idle_frames = ['idle0', 'idle1', 'idle2', 'idle3']
run_frames = ['run0', 'run1', 'run2', 'run3']
jump_frame = 'jump0'
heart_img = 'heart'
enemy_img = 'enemy'

# Plataformas
platforms = [Rect((300, 300), (200, 20)), Rect((600, 200), (150, 20))]

# Botões do menu
buttons = {
    'start': Rect((WIDTH // 2 - 60, 200), (120, 40)),
    'sound': Rect((WIDTH // 2 - 60, 260), (120, 40)),
    'exit': Rect((WIDTH // 2 - 60, 320), (120, 40))
}

class Hero:
    def __init__(self):
        self.actor = Actor(idle_frames[0], pos=(100, 380))
        self.velocity_y = 0
        self.on_ground = True
        self.frame_count = 0
        self.frame_index = 0
        self.frame_delay = 5
        self.lives = max_lives

    def update(self):
        self.velocity_y += gravity
        self.actor.y += self.velocity_y
        self.on_ground = False

        # Piso
        if self.actor.y >= 380:
            self.actor.y = 380
            self.velocity_y = 0
            self.on_ground = True

        # Plataformas
        for platform in platforms:
            if self.actor.colliderect(platform) and self.velocity_y > 0 and self.actor.y < platform.y:
                self.actor.y = platform.y
                self.velocity_y = 0
                self.on_ground = True

        # Movimento lateral
        if keyboard.left:
            self.actor.x -= 5
            self.actor.flip_h = True
        if keyboard.right:
            self.actor.x += 5
            self.actor.flip_h = False

        # Animação
        self.frame_count += 1
        if self.frame_count >= self.frame_delay:
            self.frame_count = 0
            self.frame_index = (self.frame_index + 1) % len(idle_frames)

        if not self.on_ground:
            self.actor.image = jump_frame
        elif keyboard.left or keyboard.right:
            self.actor.image = run_frames[self.frame_index]
        else:
            self.actor.image = idle_frames[self.frame_index]

    def draw(self):
        self.actor.draw()

    def jump(self):
        if self.on_ground:
            self.velocity_y = jump_strength

    def reset_position(self):
        self.actor.pos = (100, 380)
        self.velocity_y = 0

class Enemy:
    def __init__(self, pos, speed):
        self.actor = Actor(enemy_img, pos=pos)
        self.speed = speed

    def update(self):
        self.actor.x += self.speed
        if self.actor.left < 0 or self.actor.right > WIDTH:
            self.speed *= -1

    def draw(self):
        self.actor.draw()

# Instâncias
hero = Hero()
enemies = [Enemy((600, 380), 2), Enemy((400, 300), -1.5)]

def draw():
    screen.clear()
    screen.blit('background', (0, 0))

    if game_started:
        for platform in platforms:
            screen.draw.filled_rect(platform, "brown")

        for enemy in enemies:
            enemy.draw()

        hero.draw()
        draw_hearts()

        if fade_alpha > 0:
            screen.surface.set_alpha(fade_alpha)
            screen.blit('background', (0, 0))
            screen.surface.set_alpha(None)
    else:
        screen.draw.text("MEU JOGO", center=(WIDTH // 2, 100), fontsize=60, color="white")
        screen.draw.filled_rect(buttons['start'], "blue")
        screen.draw.text("Iniciar", center=buttons['start'].center, fontsize=30, color="white")
        screen.draw.filled_rect(buttons['sound'], "green")
        screen.draw.text("Som: " + ("On" if sound_on else "Off"), center=buttons['sound'].center, fontsize=30, color="white")
        screen.draw.filled_rect(buttons['exit'], "red")
        screen.draw.text("Sair", center=buttons['exit'].center, fontsize=30, color="white")

def draw_hearts():
    for i in range(hero.lives):
        screen.blit(heart_img, (10 + i * 40, 10))

def update():
    global fade_alpha, game_started

    if not game_started:
        return

    if fade_alpha > 0:
        fade_alpha -= 5

    hero.update()
    for enemy in enemies:
        enemy.update()

        if hero.actor.colliderect(enemy.actor):
            hero.reset_position()
            hero.lives -= 1
            if hero.lives <= 0:
                reset_game()

def on_key_down(key):
    if key == keys.SPACE:
        hero.jump()

def on_mouse_down(pos):
    global game_started, sound_on, fade_alpha
    if not game_started:
        if buttons['start'].collidepoint(pos):
            game_started = True
            fade_alpha = 255
            if sound_on:
                music.play('bgm')
        elif buttons['sound'].collidepoint(pos):
            sound_on = not sound_on
            if not sound_on:
                music.stop()
            else:
                music.play('bgm')
        elif buttons['exit'].collidepoint(pos):
            exit()

def reset_game():
    global game_started, fade_alpha
    game_started = False
    hero.lives = max_lives
    fade_alpha = 255
    music.stop()

pgzrun.go()
