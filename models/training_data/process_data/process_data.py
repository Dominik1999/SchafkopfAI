import ast
import pandas as pd
import re

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


def translate_actions(action):
    if "sagt weiter" in action:
        num_action = [None, None]
    elif "an Wenz" in action:
        num_action = [None, 1]
    else:
        num_action = False
    return num_action


def translate_type(result):
    if "Zamgewor" in result:
        num_type = [None, None]
    elif "auf die Alte" in result:
        num_type = [3, 0]
    elif "auf die Blaue" in result:
        num_type = [2, 0]
    elif "auf die Hund" in result:
        num_type = [0, 0]
    elif "Wenz" in result:
        num_type = [None, 1]
    elif "Herz-Solo" in result:
        num_type = [1, 2]
    elif "Eichel-Solo" in result:
        num_type = [3, 2]
    elif "Gras-Solo" in result:
        num_type = [2, 2]
    elif "Schellen-Solo" in result:
        num_type = [0, 2]
    else:
        breakpoint()
        num_type = False
    return num_type


def translate_result(result):
    if len(result) == 1:
        return None
    return int(re.search(r'\d+', result).group())


"""
        self.games = [[None, None],                     # no game
                      [0, 0], [2, 0], [3, 0],           # sauspiel
                      [None, 1],                        # wenz
                      [0, 2], [1, 2], [2, 2], [3, 2]]   # solo
                    # schelle # herz # gras # eichel

"""


def remove_short_version(games):
    return games.drop(games[games.short_version == True].index)


def remove_farbwenz_geier(games):
    game_types_to_remove = ['Farbwenz', 'Geier']
    return games[~games.type.str.contains('|'.join(game_types_to_remove))]


def get_hands_games_position(games): # this ignores the result so far for Saupiele ToDo calculate which players won the game
    games_dict = {}
    max = 0
    min = 0

    # now put the games into nice dictionary
    for i in range(games.shape[0]):

        game_number = int(re.search('#(.*?),', games.number.iloc[i])[0].replace(".", "").replace("#", "").replace(",", ""))

        if game_number > max:
            max = game_number
        if i == 0:
            min = game_number
        if game_number < min:
            min = game_number

        games_dict[game_number] = ast.literal_eval(games.players.iloc[i])
        games_dict[game_number]["protocol"] = ast.literal_eval(games.bidding.iloc[i])
        games_dict[game_number]["num_protocol"] = [False, False, False, False]
        games_dict[game_number]["type"] = games.type.iloc[i]
        games_dict[game_number]["result"] = translate_result(games.result.iloc[i])
        for j in range(4):

            for action in games_dict[game_number]["protocol"]:
                if games_dict[game_number][j]["name"] in action:
                    if games_dict[game_number]["num_protocol"][j] == [None, 1]:
                        continue
                    games_dict[game_number]["num_protocol"][j] = translate_actions(action)

            if games_dict[game_number][j]["name"] in games_dict[game_number]["type"]:
                games_dict[game_number]["num_protocol"][j] = translate_type(games_dict[game_number]["type"])

            games_dict[game_number][j]["cards"] = translate_cards(games_dict[game_number][j]["cards"])

    # So this is rather complicated but I cannot wrap my head around it. Basically,
    # - (1) when a player passes before somebody before announced something the cards are too bad for a Rufspiel
    # - (2) when a player passes after somebody before announced something we don't get info out of the cards
    # because a Rufspiel is not possible anymore for this player
    # Furthermore, if two players want to play a Solo-Game, we only know the actual game if it is a Wenz then Solo
    # announcement, because only the actual result is logged by the website. So we do not know what the other
    # potential Solo-Player might have wanted to play, we drop the cards.

    data_list = []
    columns = ['cards', 'position', 'protocol', 'result']
    for game in games_dict:
        a_player_announces_something = False
        for i, action in enumerate(games_dict[game]["num_protocol"]):
            if action != [None, None]:
                a_player_announces_something = True
                if not action:
                    continue
                data_list.append((
                    games_dict[game][i]["cards"],
                    i,
                    games_dict[game]["num_protocol"],
                    games_dict[game]["result"]          # result is only to be interpreted at certain games
                ))
                continue
            if a_player_announces_something and action == [None, None]:
                continue
            data_list.append((
                games_dict[game][i]["cards"],
                i,
                games_dict[game]["num_protocol"],
                games_dict[game]["result"]
            ))

    return data_list, columns, (min, max)


def get_all_type_of_games_with_pos_win_or_lose(games, game_type):

    games_dict = {}
    max = 0
    min = 0

    games = games[games.type.str.contains(game_type)]

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
        games_dict[game_number]["type"] = games.type.iloc[i]
        games_dict[game_number]["result"] = translate_result(games.result.iloc[i])

        for j in range(4):
            if games_dict[game_number][j]["name"] in games_dict[game_number]["type"]:
                games_dict[game_number]["position"] = j
                games_dict[game_number]["cards"] = translate_cards(games_dict[game_number][j]["cards"])

    data_list = []
    # here the position of the players is not taken into account
    for game in games_dict:
        data_list.append((games_dict[game]["cards"], games_dict[game]["position"], games_dict[game]["result"]))

    games_data = pd.DataFrame(data=data_list, columns=['cards', 'position', 'result'])
    store = pd.HDFStore(f'{game_type}-hands-with-pos-{min}-{max}.h5')
    store['games_data'] = games_data
    store.close()


# pd.set_option('display.max_colwidth', None)
# pd.set_option('display.max_columns', None)
filename = "/media/pirate/Samsung_T5/EXTERN/Schafkopf-AI/Spiele/merged/games-101m-new.csv"
games = pd.read_csv(filename, sep=";", header=[0])

games = remove_short_version(games)
games = remove_farbwenz_geier(games)

data_list, columns, (min,max) = get_hands_games_position(games)
#get_all_type_of_games_with_pos_win_or_lose(games, "Wenz")

games_data = pd.DataFrame(data=data_list, columns=columns)

store = pd.HDFStore(f'bidding-pos-{(min,max)[0]}-{(min,max)[1]}.h5')
store['games_data'] = games_data
store.close()