screen leaderboards():

    tag menu

    add Solid("#0b0b0b")

    default TABLE_W = 820
    default TABLE_H = 180

    frame:
        xalign 0.5
        yalign 0.5
        padding (3, 3)
        background Solid("#00a8ff")

        frame:
            padding (40, 35)
            background Solid("#1a1a1a")
            xsize 900
            ysize 500

            vbox:
                spacing 20
                xalign 0.5

                text "Leaderboards" size 56 xalign 0.5

                null height 10

                #Cabeçalho
                hbox:
                    spacing 30
                    xsize 820
                    xalign 0.5

                    text "Rank":
                        size 28
                        xsize 90
                        text_align 0.5

                    text "Name":
                        size 28
                        xsize 520
                        text_align 0.5

                    text "Score":
                        size 28
                        xsize 200
                        text_align 0.5

                add Solid("#444") xsize 820 ysize 2 xalign 0.5

                #Scroll View
                if not persistent.leaderboard:
                    text "No scores yet." size 28 xalign 0.5
                else:
                    viewport:
                        xsize 820
                        ysize 180
                        xalign 0.5
                        scrollbars "vertical"
                        mousewheel True
                        draggable True

                        vbox:
                            spacing 10
                            for i, e in enumerate(persistent.leaderboard, start=1):
                                hbox:
                                    spacing 30
                                    xsize 180

                                    text "[i]":
                                        size 26
                                        xsize 90
                                        text_align 0.5

                                    text "[e['name']]":
                                        size 26
                                        xsize 520
                                        text_align 0.5

                                    text "[e['score']]":
                                        size 26
                                        xsize 200
                                        text_align 0.5

                # Botões sempre no mesmo lugar
                null height 10

                hbox:
                    spacing 20
                    xalign 0.5
                    textbutton "Back" action Return()
                    textbutton "Clear" action Function(clear_leaderboard)