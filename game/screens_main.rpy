screen main_menu():

    tag menu

    add Solid("#0b0b0b")

    # Caixa com borda (frame externo = borda, frame interno = fundo)
    frame:
        xalign 0.5
        yalign 0.5
        padding (3, 3)                 # espessura da borda
        background Solid("#00a8ff")    # cor da borda (ajuste)

        frame:
            padding (40, 35)
            background Solid("#1a1a1a")

            vbox:
                spacing 22
                xalign 0.5

                text "OppaiMan Breakout" size 56 xalign 0.5

                null height 8

                textbutton "New Game" action Start() xalign 0.5
                textbutton "Leaderboards" action ShowMenu("leaderboards") xalign 0.5
                textbutton "Options" action ShowMenu("preferences") xalign 0.5
                textbutton "Quit" action Quit(confirm=True) xalign 0.5
        