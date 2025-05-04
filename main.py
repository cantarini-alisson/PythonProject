import pgzrun
from random import randint
from pygame import Rect

WIDTH = 800
HEIGHT = 480

# Estados
game_started = False
sound_on = True
gravity = 1
jump_strength = -22
on_ground = True
lives = 3
max_lives = 3
fade_alpha = 255

# Sprites
idle_frames = ['idle0', 'idle1', 'idle2', 'idle3']
run_frames = ['run0', 'run1', 'run2', 'run3']
jump_frame = 'jump0'
heart_img = 'heart'
enemy_img = 'enemy'
current_frame = 0
frame_delay = 5
frame_count = 0

# Heroi
hero = Actor(idle_frames[0], pos=(100, 380))
hero.vy = 0

# Inimigo único
enemy = Actor(enemy_img, pos=(600, 380))
enemy.vx = 2

# Plataformas
platforms = [Rect((300, 300), (200, 20)), Rect((600, 200), (150, 20))]

# Botões
buttons = {
    'start': Rect((WIDTH // 2 - 60, 200), (120, 40)),
    'sound': Rect((WIDTH // 2 - 60, 260), (120, 40)),
    'exit': Rect((WIDTH // 2 - 60, 320), (120, 40))
}

def draw():
    screen.clear()
    screen.blit('background', (0, 0))

    if game_started:
        for p in platforms:
            screen.draw.filled_rect(p, "brown")

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
    for i in range(lives):
        screen.blit(heart_img, (10 + i * 40, 10))

def update():
    global frame_count, current_frame, on_ground, fade_alpha, lives

    if not game_started:
        return

    if fade_alpha > 0:
        fade_alpha -= 5

    hero.vy += gravity
    hero.y += hero.vy

    on_ground = False
    if hero.y >= 380:
        hero.y = 380
        hero.vy = 0
        on_ground = True

    for p in platforms:
        if hero.colliderect(p) and hero.vy > 0 and hero.y < p.y:
            hero.y = p.y
            hero.vy = 0
            on_ground = True

    if keyboard.left:
        hero.x -= 5
        hero.flip_h = True
    if keyboard.right:
        hero.x += 5
        hero.flip_h = False

    frame_count += 1
    if frame_count >= frame_delay:
        frame_count = 0
        current_frame = (current_frame + 1) % len(idle_frames)

    if not on_ground:
        hero.image = jump_frame
    elif keyboard.left or keyboard.right:
        hero.image = run_frames[current_frame]
    else:
        hero.image = idle_frames[current_frame]

    # Movimento do inimigo
    enemy.x += enemy.vx
    if enemy.left < 0 or enemy.right > WIDTH:
        enemy.vx *= -1

    if hero.colliderect(enemy):
        hero.x, hero.y = 100, 380
        hero.vy = 0
        lives -= 1
        if lives <= 0:
            reset_game()

def reset_game():
    global game_started, lives, fade_alpha
    game_started = False
    lives = max_lives
    fade_alpha = 255
    music.stop()

def on_key_down(key):
    if key == keys.SPACE and on_ground:
        hero.vy = jump_strength

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

pgzrun.go()
