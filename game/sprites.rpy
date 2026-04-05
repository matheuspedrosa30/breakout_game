init python:  
    SPRITESHEET = "images/spritesheets/breakout_assets_x2.png"

    def sprite(x,y,w,h):
        return Crop((x, y, w, h), SPRITESHEET)
  
    BRICK_FRAMES = 6

    BRICK_SKIN_Y = [0, 16, 32, 48, 64, 80, 96, 112, 128, 144]

    def _brick_sprite_name(skin, frame):
        return "spr_brick_%d_%d" % (skin, frame)

    for skin in range(10):
        y = BRICK_SKIN_Y[skin]
        for f in range(BRICK_FRAMES):
            x = f * BRICK_W
            renpy.image(_brick_sprite_name(skin, f), sprite(x, y, BRICK_W, BRICK_H))


#powerups item drop vermelho
image pu_red_0 = sprite(450, 480, 12, 16)
image pu_red_1 = sprite(466, 480, 12, 16)
image pu_red_2 = sprite(482, 477, 12, 16)
image pu_red_3 = sprite(498, 480, 12, 16)

image pu_red = Animation(
    "pu_red_0", 0.08,
    "pu_red_1", 0.08,
    "pu_red_2", 0.08,
    "pu_red_3", 0.08,
)

#powerups item drop azul
image pu_blue_0 = sprite(450, 448, 12, 16)
image pu_blue_1 = sprite(466, 448, 12, 16)
image pu_blue_2 = sprite(482, 445, 12, 16)
image pu_blue_3 = sprite(498, 448, 12, 16)

image pu_blue = Animation(
    "pu_blue_0", 0.08,
    "pu_blue_1", 0.08,
    "pu_blue_2", 0.08,
    "pu_blue_3", 0.08,
)

#powerups item drop verde
image pu_green_0 = sprite(450, 496, 12, 16)
image pu_green_1 = sprite(466, 496, 12, 16)
image pu_green_2 = sprite(482, 493, 12, 16)
image pu_green_3 = sprite(498, 496, 12, 16)

image pu_green = Animation(
    "pu_green_0", 0.08,
    "pu_green_1", 0.08,
    "pu_green_2", 0.08,
    "pu_green_3", 0.08,
)

image spr_brick = sprite(0, 0, 32, 16)

image spr_ball  = sprite(384, 384, 16, 16)

image spr_paddle_2 = sprite(40, 384, 48, 32)
image spr_paddle_3 = sprite(96, 384, 64, 32)
image spr_paddle_4 = sprite(168, 384, 80, 32)
image spr_paddle_5 = sprite(256, 384, 96, 32)

image spr_heart_full  = sprite(704, 354, 31, 30)
image spr_heart_empty = sprite(704, 418, 31, 30)