import pygame, random
from sys import exit


def display_score():
    current_time = int((pygame.time.get_ticks() - start_time) / 100)
    score_surf = test_font.render(f'{current_time}', False, (64,64,64))
    score_rect = score_surf.get_rect(center = (400, 60))
    screen.blit(score_surf, score_rect)
    return current_time

# def slow_down_enemies():
#     for i in range(20):
#         clock.tick(30)



def obstacle_movement(obstacle_list, obstacle_surf):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 12

            screen.blit(obstacle_surf, obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
        return obstacle_list
    else:
        return []
    
def collision(player, obstacles, obstacle_surf):
    if obstacles:
        for obstacle_rect in obstacles:
            obstacle_mask = pygame.mask.from_surface(obstacle_surf)
            if obstacle_mask.overlap(player_mask, (player_rect.x - obstacle_rect.x, player_rect.y - obstacle_rect.y)):
                return False
    return True

def player_walking():
    global player_surf, player_index
    if player_rect.bottom < 300:
        player_surf = player_jump
    else:
        player_index += 0.13
        if player_index > len(player_walk):
            player_index = 0
        player_surf = player_walk[int(player_index)]

def fly_walking():
    global fly_surf, fly_index
    if True:
        fly_index += 0.13
        if fly_index > len(fly_walk):
            fly_index = 0
        fly_surf = fly_walk[int(fly_index)]
        


#setup screen
pygame.init()
pygame.joystick.init()
screen = pygame.display.set_mode((800,400))
clock = pygame.time.Clock()
pygame.display.set_caption("Running Boy")
pygame.display.set_icon(pygame.image.load('graphics/Player/platformChar_happy.png'))
test_font = pygame.font.Font(None, 50)
running = False
start_time = 0
score = 0

joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]


#Setting up Sprites :)
sky_surf = pygame.image.load('graphics/Sky.png').convert()
ground_surf = pygame.image.load('graphics/ground.png').convert()

# score_surf =  test_font.render(f'Your Score: {score}', False, (64,64,64))
# score_rect = score_surf.get_rect(center = (400, 50))



first_surf = test_font.render('Running Boy', False, 'White')
first_rect = first_surf.get_rect(center = (400, 70))
died_surf = test_font.render('YOU DIED', False, 'Red')
died_rect = died_surf.get_rect(midtop = (400, 50))
play_surf = test_font.render('Press Space to Play',False, 'White')
play_rect = play_surf.get_rect(midbottom = (400, 370))

#Enemies
slime_surf = pygame.image.load('graphics/Enemy/slimeWalk1.png').convert_alpha()
slime_rect = slime_surf.get_rect(midbottom = (650, 300))
# slime_mask = pygame.mask.from_surface(slime_surf)

fly_walk_1 = pygame.image.load('graphics/Enemy/flyFly1.png')
fly_walk_2 = pygame.image.load('graphics/Enemy/flyFly2.png')
fly_walk = [fly_walk_1, fly_walk_2]
fly_index = 0
fly_surf = fly_walk[fly_index]

fly_rect = fly_surf.get_rect(midbottom = (650, 200))
# fly_mask = pygame.mask.from_surface(fly_surf)

obstacle_slime_list = []
obstacle_fly_list = []


slime_speed = 9

player_walk_1 = pygame.image.load('graphics/Player/platformChar_walk1.png').convert_alpha()
player_walk_2 = pygame.image.load('graphics/Player/platformChar_walk2.png').convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0
player_jump = pygame.image.load('graphics/Player/platformChar_jump.png').convert_alpha()

player_surf = player_walk[player_index]



player_rect = player_surf.get_rect(midbottom = (80, 300))
player_mask = pygame.mask.from_surface(player_surf)
player_died_surf = pygame.image.load('graphics/Player/platformChar_duck.png').convert_alpha()
player_died_scaled = pygame.transform.rotozoom(player_died_surf, 0 , 2)
player_died_rect = player_died_scaled.get_rect(center = (400, 300))

player_start_surf = pygame.image.load('graphics/Player/platformChar_jump.png')
player_start_rect = player_start_surf.get_rect(center = (400, 200))

player_gravity = 0

#Timer
slime_timer = pygame.USEREVENT + 1
fly_timer = pygame.USEREVENT + 2
pygame.time.set_timer(slime_timer, 800)
pygame.time.set_timer(fly_timer, 2200)

#Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if running:    
            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     slow_down_enemies()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                    player_gravity = -20
                elif event.key == pygame.K_SPACE and player_rect.bottom < 300:
                    for ticks in range(20):
                        player_gravity += 1
            if event.type == pygame.JOYBUTTONDOWN:
                if  event.button == 0 and player_rect.bottom >= 300:
                    player_gravity = -20
                elif event.button == 0 and player_rect.bottom < 300:
                    for ticks in range(20):
                        player_gravity += 1
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    slime_rect.left = 800
                    running = True
            if event.type == pygame.JOYBUTTONDOWN:
                if  event.button == 0:
                    slime_rect.left = 800
                    running = True
        if event.type == slime_timer and running:
            obstacle_slime_list.append(slime_surf.get_rect(midbottom = (random.randint(800, 1400), 300)))
            # obstacle_fly_list.append(fly_surf.get_rect(midbottom = (random.randint(800, 2000), 200)))
        if event.type == fly_timer and running:
            obstacle_fly_list.append(fly_surf.get_rect(midbottom = (random.randint(800, 2000), 200)))

    # screen.blit(player_start_surf, player_start_rect)
    # screen.blit(play_surf, play_rect)
    
    if running:
        #Background
        screen.blit(sky_surf, (0, 0))
        screen.blit(ground_surf, (0, 300))

        #Text
        # pygame.draw.rect(screen, '#c0e8ec', score_rect)
        # pygame.draw.rect(screen, '#c0e8ec', score_rect, 10, 10)
        # screen.blit(score_surf, score_rect)
        score = display_score()

        #Enemy
        # slime_rect.left -= slime_speed
        # if(slime_rect.left <= -90):
        #     slime_rect.left = 800
        #     slime_speed = random.randint(9, 18)
        # screen.blit(slime_surf, slime_rect)

        #Character

        player_gravity += 1
        player_rect.y += player_gravity
        player_walking()
        fly_walking()
        screen.blit(player_surf, player_rect)

        if player_rect.bottom >= 300: 
            player_rect.bottom = 300
            player_gravity = 0

        #Enemy Movement
        obstacle_slime_list = obstacle_movement(obstacle_slime_list, slime_surf)
        obstacle_fly_list = obstacle_movement(obstacle_fly_list, fly_surf)



        #Enemy collision
        # if slime_mask.overlap(player_mask, (player_rect.x - slime_rect.x, player_rect.y - slime_rect.y)):
        #     running = False
        running = collision(player_rect, obstacle_slime_list, slime_surf) and collision(player_rect, obstacle_fly_list, fly_surf)
    else:
        screen.fill('Black')
        score_message = test_font.render(f'Your Score: {score}', False, 'White')
        score_message_rect = score_message.get_rect(center = (400, 200))
        slime_speed = 9
        start_time = pygame.time.get_ticks()

        if score == 0:
            screen.blit(player_start_surf, player_start_rect)
            screen.blit(first_surf, first_rect)
            screen.blit(play_surf, play_rect)
        else:
            screen.blit(player_died_scaled, player_died_rect)
            screen.blit(died_surf, died_rect)
            screen.blit(score_message, score_message_rect)
            obstacle_slime_list =[]
            obstacle_fly_list = []
        

    pygame.display.update()

    clock.tick(60)