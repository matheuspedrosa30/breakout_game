screen preferences():

    tag menu

    add Solid("#0b0b0b")

    frame:
        xalign 0.5
        yalign 0.5
        padding (3, 3)
        background Solid("#00a8ff")

        frame:
            padding (40, 35)
            background Solid("#1a1a1a")

            vbox:
                spacing 28
                xalign 0.5

                text "Options" size 56 xalign 0.5

                null height 10

                # Fullscreen
                hbox:
                    spacing 20
                    text "Fullscreen"
                    textbutton "[ 'ON' if _preferences.fullscreen else 'OFF' ]" action Preference("display", "toggle")

                # Music Volume
                vbox:
                    spacing 8
                    text "Music Volume"
                    bar value Preference("music volume")

                # SFX Volume
                vbox:
                    spacing 8
                    text "SFX Volume"
                    bar value Preference("sound volume")

                null height 15

                textbutton "Back" action Return() xalign 0.5