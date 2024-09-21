import pygame
import time
import random

# Inicijalizacija PyGame-a
pygame.init()

# Postavljanje veličine prozora
window_x = 1020
window_y = 680
# Kreiranje prozora
game_window = pygame.display.set_mode((window_x, window_y))

# Postavljanje naslova prozora
pygame.display.set_caption('SnakeGame')

# Definisanje boja
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)
orange = pygame.Color(255, 105, 0)  # Boja za zidove

# Učitavanje pozadinske slike
background_img = pygame.image.load('background_image.jpg')
background_img = pygame.transform.scale(background_img, (window_x, window_y))

# Tekstura za zidove
wall_texture = pygame.image.load('wall_texture.jpg')
wall_texture = pygame.transform.scale(wall_texture, (10, 10))

# Tekstura za zmiju
snake_texture = pygame.image.load('snake_texture.jpg')
snake_texture = pygame.transform.scale(snake_texture, (10, 10))

# Muzika u pozadini
pygame.mixer.music.load('background_sound.mp3')
pygame.mixer.music.set_volume(0.5)  # Postavljanje jačine na 50%
pygame.mixer.music.play(-1)  # -1 označava ponavljanje beskonačno

# Učitavanje zvuka kada zmija pojede voće
eat_sound = pygame.mixer.Sound('ra.wav')
# Učitavanje zvuka za kraj igre
game_over_sound = pygame.mixer.Sound('15960.mp3')

# Kontroler broja frejmova u sekundi (FPS)
fps = pygame.time.Clock()

# Početna pozicija zmije
snake_position = [100, 50]

# Početna veličina zmije
snake_body = [[100, 50],
            [90, 50],
            [80, 50],
            [70, 50]
            ]

# Pozicija hrane
fruit_position = [random.randrange(1, (window_x // 10)) * 10, 
                random.randrange(1, (window_y // 10)) * 10]

# Funkcija za generisanje pozicije voća van zidova
def generate_fruit_position():
    while True:
        # Generiše nasumičnu poziciju voća
        new_fruit_position = [random.randrange(1, (window_x // 10)) * 10,
                              random.randrange(1, (window_y // 10)) * 10]

        # Proverava da li je voće unutar zidova
        if (new_fruit_position[0] >= wall_thickness and
            new_fruit_position[0] <= window_x - wall_thickness - 10 and
            new_fruit_position[1] >= wall_thickness and
            new_fruit_position[1] <= window_y - wall_thickness - 10):
            return new_fruit_position  # Vraća validnu poziciju


fruit_spawn = True

# Početno kretanje zmije
direction = 'RIGHT'
change_to = direction

# Brzina zmije
snake_speed = 10
# Inkrement
increase_speed_by = 5

# Širina zidova
wall_thickness = 10

# Rezultat
score = 0

# Funkcija za prikaz rezultata
def show_score(color, font, size):
    # Kreiranje font objekta
    score_font = pygame.font.SysFont(font, size)
    
    # Kreiranje prozora za prikaz rezultata 
    score_surface = score_font.render('Score: ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    
    # Postavljanje pozicije rezultata na desnom gornjem delu ekrana
    score_rect.topright = (window_x - 20, 20)
    
    # Prikaz
    game_window.blit(score_surface, score_rect)

# Funkcija za kraj igre
def game_over():
    pygame.mixer.music.pause()  # Stopira muziku u pozadini
    # Kreiranje font objekta
    my_font = pygame.font.SysFont('times new roman', 50)
    
    # Kreiranje prozora za prikaz rezultata 
    game_over_surface = my_font.render(
        'Your Score is : ' + str(score), True, red)
    
    game_over_rect = game_over_surface.get_rect()
    
    # Pozicija teksta
    game_over_rect.midtop = (window_x / 2, window_y / 4)
    
    # Prikaz
    game_window.blit(game_over_surface, game_over_rect)
    pygame.display.flip()

    # Efekat fading-a
    fade_out_effect()
    
    # 1,9 sekundi čekanja
    time.sleep(1.9)
    
    # Kraj programa
    pygame.quit()
    quit()

# Funkcija za fading efekat na kraju igre
def fade_out_effect():
    fade = pygame.Surface((window_x, window_y))
    fade.fill(black)
    for alpha in range(0, 300):
        fade.set_alpha(alpha)
        game_window.blit(fade, (0, 0))
        pygame.display.update()
        time.sleep(0.005)

paused = False

# Funkcija za pauzu
def pause_game_message():
    pygame.mixer.music.pause()  # Stopira muziku u pozadini
    # Kreiranje font objekta
    font = pygame.font.SysFont('times new roman', 50)
    # Kreiranje poruke za pauziranje
    pause_message = font.render('Game Paused', True, white)
    # Pozicija poruke
    message_rect = pause_message.get_rect(center=(window_x // 2, window_y // 2))
    # Prikazivanje poruke na ekranu
    game_window.blit(pause_message, message_rect)
    # Ažuriranje ekrana
    pygame.display.update()

# Funkcija za crtanje ivica zidova sa teksturom
def draw_walls():
    # Crtanje gornjeg, donjeg, levog i desnog zida sa teksturom
    for i in range(0, window_x, wall_thickness):
        game_window.blit(wall_texture, (i, 0))  # Gornji zid
        game_window.blit(wall_texture, (i, window_y - wall_thickness))  # Donji zid
    for i in range(0, window_y, wall_thickness):
        game_window.blit(wall_texture, (0, i))  # Levi zid
        game_window.blit(wall_texture, (window_x - wall_thickness, i))  # Desni zid

# Funkcija za animaciju voća (menjanje boja)
def draw_fruit():
    fruit_colors = [white, red, blue]
    current_color = random.choice(fruit_colors)
    pygame.draw.rect(game_window, current_color, pygame.Rect(fruit_position[0], fruit_position[1], 10, 10))

# Funkcija za crtanje dodatnih zidova sa teksturom
def draw_additional_walls_with_texture():
    if score >= 50:  # Na svakih 50 poena dodaj prepreke
        # Horizontalni dodatni zid
        for x in range(200, 300, wall_thickness):  # Od 200 do 300 piksela sa korakom od wall_thickness
            game_window.blit(wall_texture, (x, 200))

        # Vertikalni dodatni zid
        for y in range(400, 500, wall_thickness):  # Od 400 do 500 piksela sa korakom od wall_thickness
            game_window.blit(wall_texture, (500, y))


# Funkcija za proveru kolizije sa zidovima
def check_wall_collision(snake_pos):
    if (snake_pos[0] < wall_thickness or 
        snake_pos[0] > window_x - wall_thickness - 10 or 
        snake_pos[1] < wall_thickness or 
        snake_pos[1] > window_y - wall_thickness - 10):
        return True
    return False

# Funkcija za simulaciju vibracije ekrana
def screen_shake():
    for _ in range(10):
        offset = random.randint(-10, 10)
        game_window.scroll(offset, offset)
        pygame.display.update()
        time.sleep(0.05)

# Glavna funkcija (petlja)
while True:
    # Pomeranje zmije
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                change_to = 'UP'
            if event.key == pygame.K_DOWN:
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT:
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT:
                change_to = 'RIGHT'
            if event.key == pygame.K_p:  # Pauziranje
                paused = not paused
                if paused:
                    pause_game_message()  # Pozivamo funkciju kada igra pauzira

    if not paused:
        pygame.mixer.music.unpause()  # Ponovo se pušta muzika u pozadini
        
        # Ako su istovremeno aktivne dve strelice
        if change_to == 'UP' and direction != 'DOWN':
            direction = 'UP'
        if change_to == 'DOWN' and direction != 'UP':
            direction = 'DOWN'
        if change_to == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        if change_to == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'

        # Kretanje zmije
        if direction == 'UP':
            snake_position[1] -= 10
        if direction == 'DOWN':
            snake_position[1] += 10
        if direction == 'LEFT':
            snake_position[0] -= 10
        if direction == 'RIGHT':
            snake_position[0] += 10

        # Rast zmije kada pojede voće
        snake_body.insert(0, list(snake_position))
        if snake_position == fruit_position:
            score += 10
            eat_sound.play()  # Pusti zvuk kada zmija pojede voće
            snake_speed += increase_speed_by  # Povećanje brzine
            fruit_spawn = False
        else:
            snake_body.pop()

        if not fruit_spawn:
            fruit_position = generate_fruit_position()  # Generiše novu poziciju van zidova
            fruit_spawn = True


        # Pozadinska slika
        game_window.blit(background_img, (0, 0))

        # Crtanje zidova
        draw_walls()
        # Crtanje dodatnih zidova na osnovu rezultata
        draw_additional_walls_with_texture()

        # Crtanje zmije
        for pos in snake_body:
            game_window.blit(snake_texture, (pos[0], pos[1]))

        # Crtanje voća
        draw_fruit()

        # Provera kolizije sa zidovima
        if check_wall_collision(snake_position):
            game_over_sound.play()
            screen_shake()  # Vibracija ekrana pre kraja igre
            game_over()

        # Provera kolizije sa sopstvenim telom
        for block in snake_body[1:]:
            if snake_position == block:
                game_over_sound.play()
                screen_shake()  # Vibracija ekrana pre kraja igre
                game_over()

        # Prikaz rezultata
        show_score(white, 'times new roman', 30)

        # Ažuriranje ekrana
        pygame.display.update()

        # Kontroler broja frejmova
        fps.tick(snake_speed)
