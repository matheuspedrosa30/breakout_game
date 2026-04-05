#margem da tela do jogo
default play_left = 210
default play_right = 800

#paddle
default paddle_x = 450
default paddle_y = 950
default paddle_dir = 0
default paddle_speed = 600

#bolinha
default balls = []
default ball_attached = True

#blocos
default bricks = []

#UI
default max_lives = 3
default lives = 3
default score = 0
default final_score = 0
default wave = 1
default wave_cleared = False

default game_state = "ready"   # ready | playing | game_over 
default paused = False

#powerups
default powerups = []

#pausa do frame, para não criar duas bolas no mesmo frame no powerup multiball
default multiball_cooldown = 0.0

#powerup aumenta/diminui velocidade
default ball_speed_mul = 1.0
default ball_speed_timer = 0.0

#powerup aumenta/diminui tamanho paddle
default paddle_size = 4
default paddle_size_timer = 0.0
default paddle_target_size = 4
default paddle_animating = False
default paddle_anim_timer = 0.0

# gameover/leaderboard
default score_submitted = False