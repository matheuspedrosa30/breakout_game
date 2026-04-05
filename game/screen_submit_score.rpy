default player_name_input = ""

screen submit_score():

    modal True
    tag menu

    add Solid("#0008")

    frame:
        xalign 0.5
        yalign 0.5
        padding (3, 3)
        background Solid("#00a8ff")

        frame:
            padding (35, 30)
            background Solid("#1a1a1a")
            xsize 700

            vbox:
                spacing 18
                xsize 700
                xalign 0.5

                text "Submit Score" size 48 xalign 0.5
                text "Score: [store.final_score]" size 32 xalign 0.5

                text "Your name (first name):" size 26 xalign 0.5

                input:
                    value VariableInputValue("player_name_input")
                    length 12
                    allow "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_ -"
                    pixel_width 500
                    xalign 0.5

                hbox:
                    spacing 20
                    xalign 0.5

                    textbutton "Confirm" action [
                        Function(add_score, player_name_input, store.final_score),
                        SetVariable("score_submitted", True),
                        SetVariable("player_name_input", ""),
                        ShowMenu("leaderboards")
                    ]

                    textbutton "Cancel" action [
                        SetVariable("player_name_input", ""),
                        Return()
                    ]