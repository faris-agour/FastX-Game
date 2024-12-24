import random
import sys
import pygame

# 1- CREATE WINDOW
pygame.init()
# - give or window a name
pygame.display.set_caption("RunX")
# control the framerate
clock = pygame.time.Clock()
# 2- DISPLAY SURFACE
screen = pygame.display.set_mode((900, 500))

pygame.mixer.init()

speed = 5.5

def music():
    pygame.mixer.music.load('songs/Number One 2008.mp3')
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1)


def score_board():
    global sc,speed
    sc = pygame.time.get_ticks() - start_time
    score_surface = pygame.font.Font("fonts/PixieFont.ttf", 40)
    score_surface = score_surface.render(f" Score: {sc // 1000}", False, (64, 64, 64)).convert()
    score_rect = score_surface.get_rect(topleft=(320, 50))
    screen.blit(score_surface, score_rect)
    current_score = sc //1000
    speed = 5.5 + (current_score // 10) *0.25
    return sc // 1000


def game_start(x='RUNX GAME', score=0, played=False):
    text_surface = pygame.font.Font("fonts/PixieFont.ttf", 60)
    text_surface = text_surface.render(x, False, (200, 90, 104)).convert()
    text_rect = text_surface.get_rect(topleft=(250, 40))
    screen.blit(text_surface, text_rect)

    text_surface2 = pygame.font.Font("fonts/PixieFont.ttf", 30)
    text_surface2 = text_surface2.render(" PRESS 'SPACE' TO PLAY", False, (84, 104, 164)).convert()
    text_rect2 = text_surface2.get_rect(topleft=(255, 120))
    screen.blit(text_surface2, text_rect2)

    text_surface3 = pygame.font.Font(None, 30)
    text_surface3 = text_surface3.render(f"Your score is : {score}", False, (44, 84, 64)).convert()
    text_rect3 = text_surface3.get_rect(topleft=(340, 153))
    if played:
        screen.blit(text_surface3, text_rect3)


def stand_board(lose_by_fly=False):
    player_stand = pygame.image.load("images/stand_player.png")
    player_stand_rect = player_stand.get_rect(midtop=(420, 170))
    screen.blit(player_stand, player_stand_rect)

    snail_stand = pygame.image.load("images/stand_snail.png")
    snail_stand_rect = snail_stand.get_rect(midtop=(100, 330))

    if lose_by_fly:
        screen.blit(snail_stand, snail_stand_rect)

    fly_stand = pygame.image.load("images/stand_fly.png")
    fly_stand_rect = fly_stand.get_rect(midtop=(800, 130))

    if not lose_by_fly:
        screen.blit(fly_stand, fly_stand_rect)


# [s1,s2,s3,s4,...]
def obstacle_moves(obstacle_list):
    if obstacle_list:
        for ob_rect in obstacle_list:
            ob_rect.x -= speed
            if ob_rect.bottom == 390:
                screen.blit(snail_surface, ob_rect)
            else:
                screen.blit(fly_surface, ob_rect)
        obstacle_list = [obs for obs in obstacle_list if obs.x > -100]
        return obstacle_list
    else:
        return []


def obstacles_collision(player, obstacle_list):
    for obs_rect in obstacle_list:
        if player.colliderect(obs_rect):
            hit_music.play()
            return False
    return True


def by_fly(player, obstacle_list):
    for obs_rect in obstacle_list:
        if player.colliderect(obs_rect):
            if obs_rect.bottom == 390:
                return True
            return False
        return None
    return None

def player_animation():
    global player_surface, player_index
    if player_rect.bottom < 390:
        player_surface = player_jump
    else:
        player_index += .1
        if player_index >= len(player_walk):
            player_index = 0
        player_surface = player_walk[int(player_index)]
# regular surfaces
full_surface = pygame.image.load("images/full.jpg").convert()

start_time = 0

snail_surface = pygame.image.load("images/snail.png").convert_alpha()
snail_rect = snail_surface.get_rect(bottomright=(800, 390))

fly_surface_1 = pygame.image.load("images/fly.png")
fly_surface_2 = pygame.image.load("images/stand_fly.png")
fly_surface_fly = [fly_surface_1, fly_surface_2]
fly_index = 0
fly_surface = fly_surface_fly[fly_index]
fly_rect = fly_surface.get_rect(bottomleft=(900, 200))

player_surface_1 = pygame.image.load("images/p1.png").convert_alpha()
player_surface_2 = pygame.image.load("images/p3.png").convert_alpha()
player_index = 0
player_walk = [player_surface_1, player_surface_2]
player_jump = pygame.image.load("images/jump.png").convert_alpha()

player_surface = player_walk[player_index]
player_rect = player_surface.get_rect(midbottom=(90, 390))

gravity = 0
score = 0
grounded = True
is_game_active = False
h_msg = True
played = False
lose_fly = True

second_music = pygame.mixer.Sound('songs/music.wav')
second_music.set_volume(.05)
second_music_playing = False

jump_music = pygame.mixer.Sound('songs/jump.mp3')
jump_music.set_volume(.05)

hit_music = pygame.mixer.Sound('songs/mixkit-cartoon-dazzle-hit-and-birds-746.wav')
hit_music.set_volume(.05)

music()

obstacle_list_rect = []
# to generate an event every 900 milliseconds (1.9 seconds).
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1600)

fly_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(fly_animation_timer, 200)

# 3- make the window working till we exit it
while True:
    # 4- when we exit our window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and grounded:
            gravity = -20
            jump_music.play()

        if event.type == pygame.KEYDOWN and grounded:
            if event.key == pygame.K_SPACE:
                gravity = -20
                jump_music.play()

        if not is_game_active:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                is_game_active = True
                start_time = pygame.time.get_ticks()

        if is_game_active:
            if event.type == obstacle_timer:
                if random.randint(0, 2):
                    obstacle_list_rect.append(snail_surface.get_rect(bottomleft=(random.randint(900, 1100), 390)))
                else:
                    obstacle_list_rect.append(fly_surface.get_rect(bottomleft=(random.randint(900, 1100), 200)))
                # [snail1,snail2,snail3,...]
            if event.type == fly_animation_timer:
                if fly_index == 0:
                    fly_index = 1
                else:
                    fly_index = 0
                fly_surface = fly_surface_fly[fly_index]
    if is_game_active:

        screen.blit(full_surface, (0, 0))
        screen.blit(fly_surface, fly_rect)

        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play(-1)

        if second_music_playing:
            second_music.stop()
            second_music_playing = False

        score_board()
        score = score_board()

        # fly
        # if fly_rect.right <= 0:
        #     fly_rect.left = random.randint(1000, 1500)
        # fly_rect.x -= 5
        # screen.blit(fly_surface, fly_rect)

        # snail-levels
        obs_list_rect = obstacle_moves(obstacle_list_rect)

        # if snail_rect.right <= 0:
        #     snail_rect.left = random.randint(900, 1500)
        # snail_rect.x -= 6
        # screen.blit(snail_surface, snail_rect)

        # player
        gravity += 0.80 + (speed - 5.5) * 0.05
        player_rect.y += gravity
        if player_rect.bottom < 390:
            grounded = False
        else:
            grounded = True
        if player_rect.bottom >= 390: player_rect.bottom = 390
        player_animation()
        screen.blit(player_surface, player_rect)

        # collision between rect
        # obstacles_collision(player_rect, obs_list_rect)
        is_game_active = obstacles_collision(player_rect, obs_list_rect)
        h_msg = obstacles_collision(player_rect, obs_list_rect)
        by_fly(player_rect, obs_list_rect)
        played = True
        lose_fly = by_fly(player_rect, obs_list_rect)

        # collision using mouse
        # mouse_pos = pygame.mouse.get_pos()
        # if player_rect.collidepoint(mouse_pos):
        #     print("mouse")

        # keys = pygame.key.get_pressed()
        # if keys[pygame.K_SPACE]:
        #     print("jump")

    else:
        pygame.mixer.music.stop()
        if not second_music_playing:
            second_music.play()
            second_music_playing = True

        obstacle_list_rect.clear()
        player_rect.bottom = 390
        gravity = 0
        screen.blit(full_surface, (0, 0))
        if not h_msg:
            game_start("GAME OVER", score, played)
        else:
            game_start()  # msg init
        stand_board(lose_fly)  # stand surfaces

    # 5- update our window
    pygame.display.update()
    # - the framerate of the game is 60
    clock.tick(70)
