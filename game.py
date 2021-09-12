import pygame, sys , random
# ham san chay 
def draw_floor():
    screen.blit(floor,(floor_x_pos,325))
    screen.blit(floor,(floor_x_pos + 216,325))
# ham cac ong 
def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bot_pipe = pipe_surface.get_rect(midtop = (250, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midtop = (250, random_pipe_pos -350))
    return bot_pipe , top_pipe
# ham di chuyen ong
def move_pipe(pipes):
    for pipe in pipes :
        pipe.centerx -= 1.25
    return pipes
def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= 300 :
            screen.blit(pipe_surface,pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface,False,True)
            screen.blit(flip_pipe,pipe)
def check_collosion(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            hit_sound.play()
            return False
    if bird_rect.top <= -75 or bird_rect.bottom >= 325:
        hit_sound.play()
        return False
    return True
def rotate_bird(bird1):
    new_bird = pygame.transform.rotozoom(bird1,-bird_movement*3,1)
    return new_bird
def bird_animation():
    new_bird = bird_list[bird_index]
    new_bird_rect = new_bird.get_rect(center = (50,bird_rect.centery))
    return new_bird , new_bird_rect
def score_display(game_state):
    if game_state == 'main game':
        score_surface = game_font.render(str(int(score)),True,(255,255,255))
        score_rect = score_surface.get_rect(center = (120,50))
        screen.blit(score_surface,score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}',True,(255,255,255))
        score_rect = score_surface.get_rect(center = (120,50))
        screen.blit(score_surface,score_rect)
        
        high_score_surface = game_font.render(f'High_score: {int(high_score)}',True,(255,255,255))
        high_score_rect = score_surface.get_rect(center = (100,310))
        screen.blit(high_score_surface,high_score_rect)
def update_score(score,high_score):
    if score > high_score:
        high_score = score
    return high_score
pygame.mixer.pre_init(frequency=44100, size=-16,channels=2,buffer=512)
pygame.init()
gravity = 0.2
bird_movement = 0
game_active = True 
score = 0
high_score = 0
# man hinh game
screen = pygame.display.set_mode((216,384))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.ttf',20)
# chen backgroud
bg = pygame.image.load('background-night.png')
# chen san
floor = pygame.image.load('floor.png')
floor_x_pos = 0
# tao chim
bird_down = pygame.image.load('yellowbird-downflap.png').convert_alpha()
bird_mid = pygame.image.load('yellowbird-midflap.png').convert_alpha()
bird_up = pygame.image.load('yellowbird-upflap.png').convert_alpha()
bird_list = [bird_down,bird_mid,bird_up]
bird_index = 0
bird = bird_list[bird_index]
# bird = transfrom.scalex2(bg) tang kich thuoc cua bbrid len 2 lan
bird_rect = bird.get_rect(center = (50,192))
birdflap = pygame.USEREVENT + 1
pygame.time.set_timer(birdflap, 200)
# tao ong
pipe_surface = pygame.image.load("pipe-green.png")
pipe_list = []
# tao timer
spawnpipe = pygame.USEREVENT
pygame.time.set_timer(spawnpipe, 1200)
pipe_height = [100,125,150]
game_over_surface = pygame.image.load('message.png').convert_alpha()
game_over_rect = game_over_surface.get_rect(center=(108,192))
#chen am thanh
flap_sound = pygame.mixer.Sound('sfx_wing.wav')
hit_sound = pygame.mixer.Sound('sfx_hit.wav')
score_sound = pygame.mixer.Sound('sfx_point.wav')
score_sound_countdown = 100
while True:
    # vong lap giao dien game 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if  event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement = -4.5
                flap_sound.play()
            if  event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (50,192)
                bird_movement = 0
                score = 0
        if event.type == spawnpipe:
            pipe_list.extend(create_pipe())
        if event.type == birdflap:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird, bird_rect = bird_animation()
        
    screen.blit(bg,(0,0))
    if game_active:
        bird_movement += gravity
        rotated_bird = rotate_bird(bird)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird,(bird_rect))
        game_active = check_collosion(pipe_list)
        pipe_list = move_pipe(pipe_list)
        draw_pipe(pipe_list)
        score += 0.01
        score_display('main game')
        score_sound_countdown -= 1
        if score_sound_countdown <= 0:
            score_sound.play()
            score_sound_countdown = 100
    else:
        screen.blit(game_over_surface,game_over_rect)
        high_score = update_score(score,high_score)
        score_display('game_over')
        
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -216:
        floor_x_pos = 0
    pygame.display.update()
    clock.tick(120)
