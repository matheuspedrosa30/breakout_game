screen sprite_test():
    tag test

    add Solid("#111")

    add Solid("#ffff") xpos play_left ypos 0 xsize 2 ysize config.screen_height
    add Solid("#ffff") xpos play_right ypos 0 xsize 2 ysize config.screen_height

    timer 0.016 repeat True action If(paused, NullAction(), [
        Function(update_paddle, 0.016),
        Function(update_balls, 0.016),
        Function(update_powerups, 0.016),
        Function(update_effects, 0.016)
    ])

    key "K_LEFT"  action SetVariable("paddle_dir", -1)
    key "K_a"  action SetVariable("paddle_dir", -1)
    key "K_RIGHT" action SetVariable("paddle_dir", 1)
    key "K_d"  action SetVariable("paddle_dir", 1)

    key "keyup_K_LEFT"  action If(paddle_dir == -1, SetVariable("paddle_dir", 0), NullAction())
    key "keyup_K_a" action If(paddle_dir == -1,  SetVariable("paddle_dir", 0), NullAction())
    key "keyup_K_RIGHT" action If(paddle_dir == 1,  SetVariable("paddle_dir", 0), NullAction())
    key "keyup_K_d" action If(paddle_dir == 1,  SetVariable("paddle_dir", 0), NullAction())
    

    key "K_UP" action Function(serve_ball)
    key "K_w" action Function(serve_ball)
    key "K_SPACE" action Function(serve_ball)

    key "game_menu" action NullAction()

    key "K_ESCAPE" action ToggleVariable("paused")
    key "K_p" action ToggleVariable("paused")

    add ("spr_paddle_%d" % paddle_size) xpos int(paddle_x) ypos paddle_y

    for b in balls:
        add "spr_ball" xpos int(b["x"]) ypos int(b["y"])

    for b in bricks:
        if b["alive"]:
            $ frame = 0
            if b["breaking"]:
                $ progress = (HIT_ANIM_TIME - b["hit_t"])
                $ frame = int(progress / (HIT_ANIM_TIME / BRICK_FRAMES))
                if frame < 0:
                    $ frame = 0
                if frame >= BRICK_FRAMES:
                    $ frame = BRICK_FRAMES - 1

            add ("spr_brick_%d_%d" % (b["skin"], frame)) xpos b["x"] ypos b["y"]
    
    for p in powerups:
        if p["kind"] in ("paddle_up", "paddle_down"):
            add "pu_blue" xpos int(p["x"]) ypos int(p["y"])
        elif p["kind"] in ("speed_up", "speed_down"):
            add "pu_red" xpos int(p["x"]) ypos int(p["y"])
        elif p["kind"] == "life":
            add "pu_green" xpos int(p["x"]) ypos int(p["y"])

    vbox:
        xpos 20
        ypos 50
        spacing 10
        text "Score"
        text "[store.score]"
    
    #HUD - Vidas
    $ hud_x = 20
    $ hud_y = 110
    $ spacing = 6

    for i in range(max_lives):
        if i < lives:
            add "spr_heart_full" xpos (hud_x + i * (HEART_W + spacing)) ypos hud_y
        else:
            add "spr_heart_empty" xpos (hud_x + i * (HEART_W + spacing)) ypos hud_y

    if game_state == "ready":
        text "Press ↑ to launch" xalign 0.5 yalign 0.5
    
    if game_state == "game_over":
        frame:
            xalign 0.5
            yalign 0.5
            padding (30, 25)
            background Solid("#1a1a1a")

            vbox:
                spacing 10
                xalign 0.5

                text "GAME OVER" size 50 xalign 0.5
                null height 40
                text "Score: [store.final_score]" size 30 xalign 0.5
                
                null height 40

                textbutton "Submit Score" action ShowMenu("submit_score") xalign 0.5 sensitive (not score_submitted)
                textbutton "Play Again" action Function(start_new_game) xalign 0.5
                textbutton "Main Menu" action MainMenu() xalign 0.5
    
    if paused:
        use pause_menu