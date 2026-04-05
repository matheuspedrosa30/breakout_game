default persistent.leaderboard = []

init python:

    #limpa o persistent
    def clear_leaderboard():
        persistent.leaderboard = []
        renpy.save_persistent()

    #adiciona dados no persistent
    def add_score(name, score):
        name = (name or "").strip()
        if not name:
            name = "Player"
        name = name.split()[0][:12]

        persistent.leaderboard.append({
            "name": name,
            "score": int(score)
        })

        persistent.leaderboard.sort(
            key=lambda e: e["score"],
            reverse=True
        )

        persistent.leaderboard = persistent.leaderboard[:10]

        renpy.save_persistent()
