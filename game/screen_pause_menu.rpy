screen pause_menu():

    modal True
    zorder 200

    add Solid("#0b0b0b")

    frame:
        xalign 0.5
        yalign 0.5
        padding (3, 3)
        background Solid("#00a8ff")

        frame:
            padding (40, 35)
            background Solid("#1a1a1a")
            xsize 900

            vbox:
                spacing 10
                xalign 0.5

                text "PAUSED" size 50 xalign 0.5

                null height 40

                textbutton "Resume" action SetVariable("paused", False) xalign 0.5
                textbutton "Options" action ShowMenu("preferences") xalign 0.5
                textbutton "Main Menu" action [SetVariable("paused", False), MainMenu()] xalign 0.5

                null height 10

                textbutton "Quit" action Quit(confirm=True) xalign 0.5

    # Teclas dentro do pause
    key "K_ESCAPE" action SetVariable("paused", False)
    key "K_p" action SetVariable("paused", False)