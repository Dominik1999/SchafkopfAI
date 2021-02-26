import ast
import pandas as pd

pd.set_option('display.max_colwidth', None)


def translate_cards(cards):
    result = []
    for card in cards:
        if card == 'Der Alte':
            result.append([3, 4])
        elif card == 'Der Blaue':
            result.append([2, 4])
        elif card == 'Der Rote':
            result.append([1, 4])
        elif card == 'Der Runde':
            result.append([0, 4])
        elif card == 'Eichel-Unter':
            result.append([3, 3])
        elif card == 'Gras-Unter':
            result.append([2, 3])
        elif card == 'Herz-Unter':
            result.append([1, 3])
        elif card == 'Schellen-Unter':
            result.append([0, 3])
        elif card == 'Herz-Sau':
            result.append([1, 7])
        elif card == 'Herz-Zehn':
            result.append([1, 6])
        elif card == 'Herz-König':
            result.append([1, 5])
        elif card == 'Herz-Neun':
            result.append([1, 2])
        elif card == 'Herz-Acht':
            result.append([1, 1])
        elif card == 'Herz-Sieben':
            result.append([1, 0])
        elif card == 'Die Alte':
            result.append([3, 7])
        elif card == 'Eichel-Zehn':
            result.append([3, 6])
        elif card == 'Eichel-König':
            result.append([3, 5])
        elif card == 'Eichel-Neun':
            result.append([3, 2])
        elif card == 'Eichel-Acht':
            result.append([3, 1])
        elif card == 'Eichel-Sieben':
            result.append([3, 0])
        elif card == 'Die Blaue':
            result.append([2, 7])
        elif card == 'Gras-Zehn':
            result.append([2, 6])
        elif card == 'Gras-König':
            result.append([2, 5])
        elif card == 'Gras-Neun':
            result.append([2, 2])
        elif card == 'Gras-Acht':
            result.append([2, 1])
        elif card == 'Gras-Sieben':
            result.append([2, 0])
        elif card == 'Die Hundsgfickte':
            result.append([0, 7])
        elif card == 'Schellen-Zehn':
            result.append([0, 6])
        elif card == 'Schellen-König':
            result.append([0, 5])
        elif card == 'Schellen-Neun':
            result.append([0, 2])
        elif card == 'Schellen-Acht':
            result.append([0, 1])
        elif card == 'Schellen-Sieben':
            result.append([0, 0])
    return result


"""
        self.games = [[None, None],                     # no game
                      [0, 0], [2, 0], [3, 0],           # sauspiel
                      [None, 1],                        # wenz
                      [0, 2], [1, 2], [2, 2], [3, 2]]   # solo
                    # schelle # herz # gras # eichel

"""


def translate_action(actions):
    for action in actions:
        if "sagt weiter" in action:
            num_action = [None, None]
        elif "an Wenz" in action:
            num_action = [None, 1]
        else:
            num_action = False
    return num_action


def translate_result(result):
    if "Zamgewor" in result:
        num_result = [None, None]
    elif "auf die Alte" in result:
        num_result = [3, 0]
    elif "auf die Blaue" in result:
        num_result = [2, 0]
    elif "auf die Hund" in result:
        num_result = [0, 0]
    elif "Wenz" in result:
        num_result = [None, 1]
    elif "Herz-Solo" in result:
        num_result = [1, 2]
    elif "Eichel-Solo" in result:
        num_result = [3, 2]
    elif "Gras-Solo" in result:
        num_result = [2, 2]
    elif "Schellen-Solo" in result:
        num_result = [0, 2]
    else:
        breakpoint()
        num_result = False
    return num_result

filename = "/models/data/get_data/games525-527.csv"

games = pd.read_csv(filename, sep=";", header=[0])
games_dict = {}
max = 0
min = 0

# Remove all short_version
games = games.drop(games[games.short_version == True].index)

# Remove all Geier, Farbwenz
searchfor = ['Farbwenz', 'Geier']
games = games[~games.type.str.contains('|'.join(searchfor))]

# now put the games into nice dictionary
for i in range(games.shape[0]):
    game_number = int(games.number.iloc[i][7:17].replace(".", ""))

    if game_number > max:
        max = game_number
    if i == 0:
        min = game_number
    if game_number < min:
        min = game_number

    games_dict[game_number] = ast.literal_eval(games.players.iloc[i])
    games_dict[game_number]["protocol"] = games.bidding.iloc[i].replace("[", "").replace("]", "").split(",")
    games_dict[game_number]["result"] = games.type.iloc[i]
    for j in range(4):
        if games_dict[game_number][j]["name"] in games_dict[game_number]["result"]:
            games_dict[game_number][j]["got_game"] = games_dict[game_number]["result"]

        games_dict[game_number][j]["action"] = [
            action for action in games_dict[game_number]["protocol"] if games_dict[game_number][j]["name"] in action
        ]

        # translate it into num expression
        games_dict[game_number][j]["num_cards"] = translate_cards(games_dict[game_number][j]["cards"])
        games_dict[game_number][j]["num_action"] = translate_action(games_dict[game_number][j]["action"])

        if games_dict[game_number][j]["name"] in games_dict[game_number]["result"]:
            games_dict[game_number][j]["num_action"] = translate_result(games_dict[game_number][j]["got_game"])

data_list = []
# for the first round the position of the players is not taken into account
for game in games_dict:
    for i in range(4):
        if games_dict[game][i]["num_action"] is False:
            continue
        data_list.append((games_dict[game][i]["num_cards"], games_dict[game][i]["num_action"]))

games_data = pd.DataFrame(data=data_list, columns=['cards', 'game'])

store = pd.HDFStore(f'bidding-no-pos-{min}-{max}.h5')
store['games_data'] = games_data
store.close()

"""
numbers = []
for number in games_dict:
    numbers.append(number)

sample = random.sample(numbers, 100)

for number in sample:
    print(games_dict[number])
breakpoint()
"""
"""
        first_state
        (Pdb) state
        {'game_state': <Game_State.PublicGameState object at 0x7f5b6b786c70>, 'current_player_cards': [[3, 4], [1, 3], [3, 5], [0, 0], [1, 6], [1, 7], [2, 1], [0, 3]], 'allowed_actions': [[None, None], [0, 0], [2, 0], [3, 0], [None, 1], [0, 2], [1, 2], [2, 2], [3, 2]]}
        (Pdb) state["game_state"]
        <Game_State.PublicGameState object at 0x7f5b6b786c70>
        (Pdb) state["game_state"].dealer
        1
        (Pdb) state["game_state"].game_type
        [None, None]
        (Pdb) state["game_state"].game_player
        (Pdb) state["game_state"].bidding_round
        [None, None, None, None]
"""
