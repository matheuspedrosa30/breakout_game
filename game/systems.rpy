init python:
    import random
    import math
    
    def start_new_game():
        store.lives = 3
        store.score = 0
        store.game_state = "ready"
        store.ball_speed_mul = 1.0
        store.ball_speed_timer = 0.0
        store.powerups = []
        store.score_submitted = False
        init_level()
        reset_balls_to_paddle()

    def init_level():
        store.score = 0
        generate_bricks()

    def generate_bricks():
        store.bricks = []
        
        cols = 12
        rows = 6
        gap = 4

        total_w = cols * BRICK_W + (cols - 1) * gap
        play_width = store.play_right - store.play_left
        start_x = store.play_left + (play_width - total_w) // 2
        start_y = 80

        last_skin = None

        for r in range(rows):
            #1 cor por linha, evita repetir a cor da linha anterior
            skin = random.randrange(10)
            if last_skin is not None and skin == last_skin:
                skin = (skin + random.randrange(1, 10)) % 10
            last_skin = skin
            for c in range(cols):
                x = start_x + c * (BRICK_W + gap)
                y = start_y + r * (BRICK_H + gap)
                store.bricks.append({"x": x, "y": y, "alive": True, "skin": skin, "breaking": False, "drop": None, "dropped": False, "hit_t": 0.0})

    def make_ball(x, y, vx, vy):
        return {"x": float(x), "y": float(y), "vx": float(vx), "vy": float(vy), "since_hit": 0.0}
    
    def reset_balls_to_paddle():
        # sempre volta com 1 bola
        store.balls = [ make_ball(store.paddle_x + 40 - 8, store.paddle_y - 20, 220, -220) ]
        store.ball_attached = True
    
    def serve_ball():
        if store.game_state != "ready":
            return
        
        if not store.balls:
            reset_balls_to_paddle()
    
        b = store.balls[0]
        b["x"] = store.paddle_x + 40 - 8
        b["y"] = store.paddle_y - 20
        b["vx"] = 220
        b["vy"] = -220
    
        store.ball_attached = False
        store.game_state = "playing"

    def update_balls(dt):
        PADDLE_W = 80
        PADDLE_H = 32

        dt = min(dt, 0.033)

        store.multiball_cooldown = max(0.0, store.multiball_cooldown - dt)

        if store.wave_cleared:
            respawn_wave_keep_balls()

        #congela em game_over
        if store.game_state == "game_over":
            return

        #Atualiza animações de bricks em "breaking"
        for br in store.bricks:
            if br["alive"] and br["breaking"]:
                br["hit_t"] = max(0.0, br["hit_t"] - dt)
                if br["hit_t"] <= 0.0:
                    br["alive"] = False
                    br["breaking"] = False

        #Ready: bola gruda no paddle
        if store.game_state == "ready" or store.ball_attached:
            store.ball_attached = True
            if not store.balls:
                reset_balls_to_paddle()
            b0 = store.balls[0]
            b0["x"] = store.paddle_x + 40 - 8
            b0["y"] = store.paddle_y - 20
            return

        # Atualiza cada bola no jogo
        i = 0
        while i < len(store.balls):
            b = store.balls[i]

            prev_x = b["x"]
            prev_y = b["y"]

            prev_left   = prev_x
            prev_right  = prev_x + BALL_SIZE
            prev_top    = prev_y
            prev_bottom = prev_y + BALL_SIZE

            # Move
            mul = store.ball_speed_mul
            b["x"] += b["vx"] * dt * mul
            b["y"] += b["vy"] * dt * mul
            b["since_hit"] += dt

            #Paredes
            min_x = store.play_left
            max_x = store.play_right - BALL_SIZE
            if b["x"] <= min_x:
                b["x"] = min_x
                b["vx"] *= -1
                clamp_ball_angle(b)
                b["since_hit"] = 0.0
            elif b["x"] >= max_x:
                b["x"] = max_x
                b["vx"] *= -1
                clamp_ball_angle(b)
                b["since_hit"] = 0.0

            if b["y"] <= 0:
                b["y"] = 0
                b["vy"] *= -1
                clamp_ball_angle(b)
                b["since_hit"] = 0.0

            #Bounds atuais
            ball_left   = b["x"]
            ball_right  = b["x"] + BALL_SIZE
            ball_top    = b["y"]
            ball_bottom = b["y"] + BALL_SIZE

            #Blocos
            hit_any_brick = False
            for br in store.bricks:
                if (not br["alive"]) or br["breaking"]:
                    continue

                bx = br["x"]
                by = br["y"]
                brick_left   = bx
                brick_right  = bx + BRICK_W
                brick_top    = by
                brick_bottom = by + BRICK_H

                hit = (
                    ball_right >= brick_left and ball_left <= brick_right and
                    ball_bottom >= brick_top and ball_top <= brick_bottom
                )

                if hit:
                    #lado do impacto pelo prev
                    hit_from_left   = (prev_right <= brick_left)  and (ball_right > brick_left)
                    hit_from_right  = (prev_left >= brick_right)  and (ball_left < brick_right)
                    hit_from_top    = (prev_bottom <= brick_top)  and (ball_bottom > brick_top)

                    if hit_from_left or hit_from_right:
                        if hit_from_left:
                            b["x"] = brick_left - BALL_SIZE
                        else:
                            b["x"] = brick_right
                        b["vx"] *= -1
                        clamp_ball_angle(b)
                        b["since_hit"] = 0.0
                    else:
                        if hit_from_top:
                            b["y"] = brick_top - BALL_SIZE
                        else:
                            b["y"] = brick_bottom
                        b["vy"] *= -1
                        clamp_ball_angle(b)
                        b["since_hit"] = 0.0

                    br["breaking"] = True
                    br["hit_t"] = HIT_ANIM_TIME
                    store.score += 10

                    #Powerup: MULTIBALL
                    if store.multiball_cooldown <= 0 and len(store.balls) < 3 and random.random() < 0.18:
                        spawn_extra_ball_from_brick(br, b)  # b é a bola que acertou o brick
                    
                    if br["drop"] is None:
                        # Size Paddle UP/Down - (chance de dropar: 2%)
                        if random.random() < 0.02:
                            br["drop"] = "paddle_up" if random.random() < 0.5 else "paddle_down"
                        # Velocity UP/DOWN - (chance de dropar: 1,8%)
                        elif random.random() < 0.018:
                            br["drop"] = "speed_up" if random.random() < 0.5 else "speed_down"
                        # Extra Life - (chance de dropar: 1,5%)
                        elif random.random() < 0.015:
                            br["drop"] = "life"
                        else:
                            br["drop"] = None

            
                    if br["drop"] is not None and not br["dropped"]:
                        br["dropped"] = True
                        spawn_powerup(
                            br["drop"],
                            br["x"] + (BRICK_W / 2) - 8,
                            br["y"] + (BRICK_H / 2) - 8
                        )

                    # vitória (passa para o próximo nível)
                    if check_wave_clear():
                        next_wave()

                    hit_any_brick = True
                    break

            # Recalcula bounds após brick
            ball_left   = b["x"]
            ball_right  = b["x"] + BALL_SIZE
            ball_top    = b["y"]
            ball_bottom = b["y"] + BALL_SIZE

            #Paddle
            paddle_left   = store.paddle_x
            paddle_w      = PADDLE_WIDTHS[store.paddle_size]
            paddle_right  = store.paddle_x + paddle_w
            paddle_top    = store.paddle_y
            paddle_bottom = store.paddle_y + PADDLE_H

            hit_paddle = (
                ball_right >= paddle_left and ball_left <= paddle_right and
                ball_bottom >= paddle_top and ball_top <= paddle_bottom
            )

            if hit_paddle:
                overlap_left   = ball_right - paddle_left
                overlap_right  = paddle_right - ball_left
                overlap_top    = ball_bottom - paddle_top
                overlap_bottom = paddle_bottom - ball_top

                min_ox = overlap_left if overlap_left < overlap_right else overlap_right
                min_oy = overlap_top  if overlap_top  < overlap_bottom else overlap_bottom

                if min_ox < min_oy:
                    # lateral
                    if overlap_left < overlap_right:
                        b["x"] = paddle_left - BALL_SIZE
                    else:
                        b["x"] = paddle_right
                    b["vx"] *= -1
                    clamp_ball_angle(b)
                    b["since_hit"] = 0.0
                else:
                    # topo (aqui entra o aiming)
                    if overlap_top < overlap_bottom:
                        b["y"] = paddle_top - BALL_SIZE

                        # Só aplica se a bola estava descendo
                        if b["vy"] > 0:
                            # t: -1 esquerda, +1 direita
                            paddle_w = PADDLE_WIDTHS[store.paddle_size]
                            paddle_center = store.paddle_x + paddle_w * 0.5
                            ball_center = b["x"] + BALL_SIZE * 0.5
                            t = (ball_center - paddle_center) / (paddle_w * 0.5)
                            t = max(-1.0, min(1.0, t))

                            # ângulo entre 25° e 155°
                            angle = 90 - (t * 65)

                            spd = ball_speed(b)
                            set_ball_velocity_from_angle(b, angle, spd)
                            clamp_ball_angle(b)

                    else:
                        #se bater por baixo (raro)
                        b["y"] = paddle_bottom
                        if b["vy"] < 0:
                            b["vy"] *= -1
                            clamp_ball_angle(b)
                
                b["since_hit"] = 0.0

            #Caiu embaixo: remove só a bola que cair
            if b["y"] >= config.screen_height - BALL_SIZE:
                store.balls.pop(i)
                continue

            if b["since_hit"] > 5.0:  # 5 segundos sem bater em nada, aplica o antistuck
                anti_stuck_ball(b)
                b["since_hit"] = 0.0
                
            i += 1
        
        if not store.wave_cleared and check_wave_clear():
            store.wave_cleared = True

        # Se não sobrou nenhuma bola: perde vida e volta pro ready
        if len(store.balls) == 0:
            store.lives -= 1
            if store.lives > 0:
                store.game_state = "ready"
                reset_balls_to_paddle()
            else:
                store.final_score = store.score
                store.game_state = "game_over"
                store.score_submitted = False
                store.ball_attached = True
    
    def ball_speed(b):
        return math.sqrt(b["vx"]*b["vx"] + b["vy"]*b["vy"])

    def set_ball_velocity_from_angle(b, angle_deg, speed):
        rad = math.radians(angle_deg)
        b["vx"] = math.cos(rad) * speed
        b["vy"] = -abs(math.sin(rad) * speed)  #sempre sobe após bater no paddle

    def clamp_ball_angle(b, min_vy_ratio=0.30):
        #evita a bola ficar quase horizontal (vy muito pequeno).
        #mantém magnitude (speed) e corrige vx/vy.
        spd = ball_speed(b)
        if spd < 0.001:
            return

        vx, vy = b["vx"], b["vy"]
        min_vy = spd * min_vy_ratio

        if abs(vy) < min_vy:
            # preserva o sentido vertical atual
            vy = -min_vy if vy < 0 else min_vy
            sign = -1 if vx < 0 else 1
            vx = sign * math.sqrt(max(0.0, spd*spd - vy*vy))

        b["vx"], b["vy"] = vx, vy

    def update_paddle(dt):
        if store.paddle_dir == 0:
            return

        new_x = store.paddle_x + store.paddle_dir * store.paddle_speed * dt

        min_x = store.play_left
        current_w = PADDLE_WIDTHS[store.paddle_size]
        max_x = store.play_right - current_w
        store.paddle_x = int(max(min_x, min(new_x, max_x)))
    
    def spawn_powerup(kind, x, y):
        store.powerups.append({
            "kind": kind,
            "x": float(x),
            "y": float(y),
            "vy": 220.0,
        })

    def spawn_extra_ball_from_brick(br, base_ball):
        #Cria 1 bola extra na posição do brick quebrado, com velocidade baseada
        #na bola que acertou (base_ball), com um desvio para não colar.
        
        #nasce no centro do brick
        x = br["x"] + (BRICK_W / 2) - 8
        y = br["y"] + (BRICK_H / 2) - 8

        spd = ball_speed(base_ball)
        if spd < 0.001:
            spd = 220.0

        angle = 90
        # calcula ângulo aproximado da base
        angle_base = math.degrees(math.atan2(-base_ball["vy"], base_ball["vx"]))
        angle = max(25, min(155, angle_base + random.choice([-20, 20])))

        nb = make_ball(x, y, 0, 0)
        set_ball_velocity_from_angle(nb, angle, spd)
        clamp_ball_angle(nb)

        store.balls.append(nb)

    def update_powerups(dt):
        if store.game_state != "playing":
            return

        PADDLE_W = 80
        PADDLE_H = 32

        i = 0
        while i < len(store.powerups):
            p = store.powerups[i]
            p["y"] += p["vy"] * dt

            # colisão com paddle
            pu_left = p["x"]
            pu_right = p["x"] + PU_W
            pu_top = p["y"]
            pu_bottom = p["y"] + PU_H

            paddle_left = store.paddle_x
            paddle_w = PADDLE_WIDTHS[store.paddle_size]
            paddle_right = store.paddle_x + paddle_w
            paddle_top = store.paddle_y
            paddle_bottom = store.paddle_y + PADDLE_H

            hit = (
                pu_right >= paddle_left and pu_left <= paddle_right and
                pu_bottom >= paddle_top and pu_top <= paddle_bottom
            )

            if hit:
                if p["kind"] == "speed_up":
                    apply_ball_speed(1.8, 8.0)
                elif p["kind"] == "speed_down":
                    apply_ball_speed(0.55, 8.0)
                elif p["kind"] == "paddle_up":
                    apply_paddle_size(5, 8.0)
                elif p["kind"] == "paddle_down":
                    apply_paddle_size(2, 8.0)
                elif p["kind"] == "life":
                    apply_life()
                store.powerups.pop(i)
                continue

            # caiu fora
            if p["y"] > config.screen_height + 40:
                store.powerups.pop(i)
                continue

            i += 1

    def apply_ball_speed(multiplier, duration):
        store.ball_speed_mul = float(multiplier)
        store.ball_speed_timer = float(duration)

    def update_effects(dt):
        if store.ball_speed_timer > 0.0:
            store.ball_speed_timer = max(0.0, store.ball_speed_timer - dt)
            if store.ball_speed_timer <= 0.0:
                store.ball_speed_mul = 1.0
        
        #TIMER DO TAMANHO
        if store.paddle_size_timer > 0:
            store.paddle_size_timer -= dt
            if store.paddle_size_timer <= 0:
                store.paddle_size_timer = 0
                store.paddle_target_size = 4
                store.paddle_animating = True
                store.paddle_anim_timer = 0.10


        #ANIMAÇÃO
        if store.paddle_animating:
            store.paddle_anim_timer -= dt
            if store.paddle_anim_timer <= 0:
            
                if store.paddle_size < store.paddle_target_size:
                    store.paddle_size += 1
                elif store.paddle_size > store.paddle_target_size:
                    store.paddle_size -= 1

                if store.paddle_size == store.paddle_target_size:
                    store.paddle_animating = False

                store.paddle_anim_timer = 0.10
    
    def apply_paddle_size(target_size, duration):
        if target_size not in (2, 5):
            return

        store.paddle_target_size = target_size
        store.paddle_size_timer = float(duration)

        store.paddle_animating = True
        store.paddle_anim_timer = 0.10
    
    def apply_life():
        if store.lives < store.max_lives:
            store.lives += 1
    
    def next_wave():
        store.wave_cleared = True
    
    def check_wave_clear():
        #nenhum brick vivo e não está no meio de animação de quebra
        for br in store.bricks:
            if br["alive"] or br.get("breaking", False):
                return False
        return True

    def anti_stuck_ball(b):
        #Se a bola ficar muito tempo sem colisão relevante,
        #ajusta levemente o ângulo.
        spd = ball_speed(b)
        if spd < 0.001:
            return

        # pequeno ajuste de ângulo
        angle = math.degrees(math.atan2(-b["vy"], b["vx"]))
        angle += random.choice([-15, 15])

        #mantém sempre dentro do range jogável
        angle = max(25, min(155, angle))

        set_ball_velocity_from_angle(b, angle, spd)
        clamp_ball_angle(b)

    def respawn_wave_keep_balls():
        store.wave += 1
        store.wave_cleared = False

        generate_bricks()
        store.powerups = []