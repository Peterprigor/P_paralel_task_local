import requests

BASE_URL = "https://lksh-enter.ru"
TOKEN = "7536eb0a1ca9af5a930174bdb83c63533d2a67ec6424751f3991c98874389746"

HEADERS = {
    "Authorization": TOKEN
}

def get_teams():
    r = requests.get(f"{BASE_URL}/teams", headers=HEADERS, timeout=100)
    if r.status_code == 200:
        return r.json()

def get_matches():
    r = requests.get(f"{BASE_URL}/matches", headers=HEADERS, timeout=100)
    if r.status_code == 200:
        return r.json()

def get_team_by_id(team_id):
    r = requests.get(f"{BASE_URL}/teams/{team_id}", headers=HEADERS, timeout=100)
    if r.status_code == 200:
        return r.json()
    else:
        for team in teams:
            if team["id"] == team_id:
                return team
    return None
def get_team_by_id2(team_id):
    for team in teams:
        if team["id"] == team_id:
            return team
    return None

def get_player_by_id(player_id):
    r = requests.get(f"{BASE_URL}/players/{player_id}", headers=HEADERS, timeout=100)
    if r.status_code == 200:
        return r.json()
    else:
        return None

def get_player_by_id2(player_id):
    l = 0
    r = len(players) - 1
    m = (r + l) // 2
    while r > l + 1:
        if players[m]["id"] == player_id:
            return players[m]
        elif players[m]["id"] > player_id:
            r = m
        else:
            l = m
        m = (r + l) // 2
    for player in players:
        if player["id"] == player_id:
            return player
    return None

def find_team_by_name(name):
    for team in teams:
        if team["name"].lower() == name.lower():
            return team
    return None

teams = []
matches = []
players = []
tournament = {
    "": [[]]
}

def f():
    for match in matches:
        print(match["id"])

def preparing():
    global teams
    global matches
    global tournament
    teams = get_teams()
    #print(teams)
    matches = get_matches()
    #print(matches)
    #_team = get_team_by_id(teams[0]["id"])
    #print(_team)
    #player = get_player_by_id(teams[0]["players"][0])
    #print(player)
    tournament.clear()
    for match in matches:
        team1 = get_team_by_id2(match["team1"])
        team2 = get_team_by_id2(match["team2"])
        if team1 == None or team2 == None:
            continue
        try:
            tournament[team1["name"]].append([team2["name"], match["team1_score"], match["team2_score"]])
        except KeyError:
            tournament[team1["name"]] = [[team2["name"], match["team1_score"], match["team2_score"]]]
        try:
            tournament[team2["name"]].append([team1["name"], match["team2_score"], match["team1_score"]])
        except KeyError:
            tournament[team2["name"]] = [[team1["name"], match["team2_score"], match["team1_score"]]]
    #print(tournament)
    for team in teams:
        for player_id in team["players"]:
            player = get_player_by_id(player_id)
            if(player == None):
                continue
            try:
                player["team"].append(team["name"])
            except KeyError:
                player["team"] = [team["name"]]
            try:
                player["team_id"] = team["id"]
            except KeyError:
                player["team_id"] = [team["id"]]
            if player not in players:
                players.append(player)
    return

def sorted_players():
    global players
    sorted_players = sorted(players, key=lambda p: (p['name'], p['surname']))
    sorted_players2 = sorted(players, key=lambda p: (p['id']))
    players = sorted_players2
    for player in sorted_players:
        print(player["name"], player["surname"])
    return

def stats(team_name):
    scored = 0
    missed = 0
    win = 0
    lose = 0
    try:
        for game in tournament[team_name]:
            scored += game[1]
            missed += game[2]
            if game[1] > game[2]:
                win += 1
            if game[1] < game[2]:
                lose += 1
        print(win, lose, scored - missed)
    except KeyError:
        print("0 0 0")

def versus(player1_id, player2_id):

    # Найдем команды игроков

    player1 = get_player_by_id2(player1_id)
    player2 = get_player_by_id2(player2_id)
    player1_teams = player1["team"]
    player2_teams = player2["team"]

    if player1_teams is None or player2_teams is None or player1_teams == player2_teams:
        print("0")
        return

    total_matches = 0
    player1_wins = 0
    player2_wins = 0
    for player1_team in player1_teams:
        for game in tournament[player1_team]:
            if game[0] in player2_teams:
                total_matches += 1
                if game[1] > game[2]:
                    player1_wins += 1
                if game[1] < game[2]:
                    player2_wins += 1

    #if total_matches == 0:
    #    print("0 0 0")
    #    return

    #print(total_matches, player1_wins, player2_wins)
    print(total_matches)
    return

def main():
    preparing()
    #print(get_team_by_id(3))
    questions = []
    while True:
        try:
            line = input().strip()
            if line.startswith("stats?"):
                # stats? "Better"
                _, team_name = line.split("?", 1)
                team_name = team_name.strip().strip('"')
                questions.append(["s", team_name])
                ##stats(team_name)
            elif line.startswith("versus?"):
                # versus? 5 3
                _, players = line.split("?", 1)
                player1_id, player2_id = map(int, players.strip().split())
                questions.append(["v", player1_id, player2_id])
                ##versus(player1_id, player2_id)
            else:
                print("Некорректный запрос")
        except EOFError:
            break
    sorted_players()
    for question in questions:
        if question[0] == "s":
            stats(question[1])
        elif question[0] == "v":
            versus(question[1], question[2])

if __name__ == "__main__":
    main()