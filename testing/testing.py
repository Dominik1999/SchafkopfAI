import pandas

from csv import DictWriter
from models.training_data.process_data.process_data import get_hands_games_position, translate_cards

"""
Some examples
(['derweudel  sagt weiter.', 'Lino  dad gern.', 'Wack  sagt weiter.', 'Schinterhans  dad gern.', 'Lino hätt an Wenz', 'Schinterhans hätt a Solo', 'Lino lässt den Vortritt.', 'Schinterhans hätt a Solo', ''])
(['mmoorrllee  dad gern.', 'FABL  dad gern.', 'tommy272  sagt weiter.', 'sipp  sagt weiter.', 'mmoorrllee lässt den Vortritt.', 'FABL hätt a Solo', ''])  -> We know that mmoorrllee does have a Rufspiel but we do not know which one 
(['Eckart  sagt weiter.', 'Striezi1  sagt weiter.', 'Sunny291278  sagt weiter.', 'Ruebenkiller  sagt weiter.', ''], '–'), 
(['FredvonBayern  sagt weiter.', 'Greislheiazuakn  dad gern.', 'Lolly11111  sagt weiter.', 'wuide_wuiderer  sagt weiter.', 'Greislheiazuakn hätt a Solo', 'Greislheiazuakn spielt Eichel', ''], 'Gewonnen mit 86 Augen (Normal)'), 
(['Ysis  dad gern.', 'stiftinger  dad gern.', 'stenum  sagt weiter.', 'roland1508  sagt weiter.', 'Ysis hätt a Solo', 'stiftinger lässt den Vortritt.', 'Ysis spielt Herz', ''], 'Gewonnen mit 95 Augen (Schneider)'), 
(['Brumas  dad gern.', 'DaGalli  sagt weiter.', 'zuendung  dad gern.', 'baer13  sagt weiter.', 'Brumas hätt an Farbwenz', 'zuendung hätt a Solo', 'Brumas lässt den Vortritt.', 'zuendung hätt a Solo', 'zuendung spielt Eichel', ''], 'Gewonnen mit 68 Augen (Normal)'), 
(['Ysis  dad gern.', 'stiftinger  dad gern.', 'stenum  sagt weiter.', 'roland1508  sagt weiter.', 'Ysis hätt a Solo', 'stiftinger lässt den Vortritt.', 'Ysis spielt Herz', ''], 'Gewonnen mit 95 Augen (Schneider)'), 
(['funnyharry  dad gern.', 'SB  dad gern.', 'rantanplan14  dad gern.', 'TimeSquare  sagt weiter.', 'funnyharry lässt den Vortritt.', 'SB hätt an Wenz', 'rantanplan14 hätt a Solo', 'SB lässt den Vortritt.', 'rantanplan14 hätt a Solo', 'rantanplan14 spielt Gras', ''], 'Gewonnen mit 111 Augen (Schneider)'), 
(['Zentrifuge  dad gern.', 'weita  sagt weiter.', 'UNIN  sagt weiter.', 'dedade  dad gern.', 'Zentrifuge lässt den Vortritt.', 'dedade hätt a Solo', 'dedade spielt Schelle', ''], 'Gewonnen mit 92 Augen (Schneider)')]
[(['Ex-Sauspieler #11557  sagt weiter.', 'Fettschwein  sagt weiter.', 'da_beste_hans  sagt weiter.', 'Colbico  sagt weiter.', ''], '–'), 
(['st0rm  sagt weiter.', 'ChefeWenz  sagt weiter.', 'Saubritschn  dad gern.', 'm587735  sagt weiter.', 'Saubritschn hätt a Sauspiel', 'Saubritschn spielt auf die Alte', ''], 'Verloren mit 57 Augen (Normal)'), 
(['Bodoline  sagt weiter.', 'moppl  sagt weiter.', 'Thomas666  dad gern.', 'didi1971  dad gern.', 'Thomas666 hätt an Farbwenz', 'didi1971 hätt a Solo', 'Thomas666 lässt den Vortritt.', 'didi1971 hätt a Solo', 'didi1971 spielt Eichel', ''], 'Gewonnen mit 68 Augen (Normal)'), 
(['kalle68  dad gern.', 'vae  sagt weiter.', 'sigi49  sagt weiter.', 'wenz84  dad gern.', 'kalle68 lässt den Vortritt.', 'wenz84 hätt an Wenz', ''], 'Verloren mit 55 Augen (Normal)'), 
(['mikee686  dad gern.', 'wakepro  sagt weiter.', 'bainmartl  sagt weiter.', 'Konerade  dad gern.', 'mikee686 lässt den Vortritt.', 'Konerade hätt a Solo', 'Konerade spielt Gras', ''], 'Gewonnen mit 75 Augen (Normal)'), 
(['jandale  sagt weiter.', 'Iwan2  dad gern.', 'Da_Utzinger_Rudi  dad gern.', 'Landauer12  dad gern.', 'Iwan2 hätt an Geier', 'Da_Utzinger_Rudi hätt an Wenz', 'Landauer12 hätt a Solo', 'Iwan2 lässt den Vortritt.', 'Da_Utzinger_Rudi lässt den Vortritt.', 'Landauer12 hätt a Solo', 'Landauer12 spielt Herz', ''], 'Verloren mit 33 Augen (Normal)'), 
(['Schaafkopf  dad gern.', 'herzzbube  sagt weiter.', 'urschl  sagt weiter.', 'dad-of-dude  dad gern.', 'Schaafkopf lässt den Vortritt.', 'dad-of-dude hätt a Solo', 'dad-of-dude spielt Schelle', ''], 'Gewonnen mit 90 Augen (Normal)')]
"""

cards = [
    ['Der Rote', 'Gras-Unter', 'Herz-Acht', 'Gras-Neun', 'Gras-Acht', 'Gras-Sieben', 'Schellen-Zehn', 'Schellen-König'],
    ['Eichel-Unter', 'Herz-Unter', 'Herz-Neun', 'Eichel-Zehn', 'Eichel-König', 'Gras-Zehn', 'Schellen-Acht',
     'Schellen-Sieben'],
    ['Der Alte', 'Der Runde', 'Herz-Zehn', 'Herz-König', 'Herz-Sieben', 'Eichel-Sieben', 'Gras-König',
     'Die Hundsgfickte'],
    ['Der Blaue', 'Schellen-Unter', 'Herz-Sau', 'Die Alte', 'Eichel-Neun', 'Eichel-Acht', 'Die Blaue', 'Schellen-Neun'],
]


def create_test_csv():
    # we have to create all 16 possibilities how the game protocols could look like
    # from all players pass to all players want to play
    # then there are several possibilities which player player if more than one wants to

    possible_bidding_rounds_numeric = [
        [0, 0, 0, 0], [1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1],
        [1, 1, 0, 0], [1, 0, 1, 0], [1, 0, 0, 1], [0, 1, 1, 0], [0, 1, 0, 1], [0, 0, 1, 1],
        [1, 1, 1, 0], [1, 1, 0, 1], [1, 0, 1, 1], [0, 1, 1, 1], [1, 1, 1, 1],
    ]

    for i, num_bidding_round in enumerate(possible_bidding_rounds_numeric):
        number = f"Spiel #100.121.12{i}, von X auf Y"
        players = {}
        for j in range(4):
            players[j] = dict(name=f'{j}', cards=cards[j])

        bidding_round = []
        for j, action in enumerate(num_bidding_round):
            if action == 1:
                bidding_round.append(f'{j} dad')
            else:
                bidding_round.append(f'{j} sagt weiter')

        if i == 0:
            game_type = ['Zamgeworfen']

        if 0 < i <= 4:
            game_type = [f'{i-1} auf die Alte']
            bidding_round.append(f"{i-1} hätt a Sauspiel")
            bidding_round.append(f"{i-1} spielt auf die Alte")

        if 4 < i <= 10:
            first_announcer = [0, 0, 0, 1, 1, 2][i-5]
            player = [1,2,3,2,3,3][i-5]

            game_type = [f'{[1,2,3,2,3,3][i-5]} spielt Eichel-Solo'] # always the last person plays a Solo so (#1,2,3,2,3,3)

            bidding_round.append(f"{first_announcer} lässt den Vortritt.")  # the first announcer passes always
            bidding_round.append(f"{player} hätt a Solo")
            bidding_round.append(f"{player} spielt Eichel")

        if 10 < i <= 14:
            first_announcer = [0, 0, 0, 1][i - 11]
            second_announcer = [1, 1, 2, 2][i - 11]
            player = [2,3,3,3][i-11]

            game_type = [f'{player} spielt Eichel-Solo'] # always the last person plays a Solo so (#1,2,3,2,3,3)

            bidding_round.append(f"{first_announcer} lässt den Vortritt.")
            bidding_round.append(f"{second_announcer} hätt an Wenz")
            bidding_round.append(f"{player} hätt a Solo")
            bidding_round.append(f"{second_announcer} lässt den Vortritt.")
            bidding_round.append(f"{player} hätt a Solo")
            bidding_round.append(f"{player} spielt Eichel")

        if i == 15:
            game_type = [f'3 spielt Eichel-Solo'] # here again the last person plays a solo but there is also a Wenz
            bidding_round.append(f"0 lässt den Vortritt.")
            bidding_round.append(f"1 hätt an Farbwenz")
            bidding_round.append(f"2 hätt an Wenz")
            bidding_round.append(f"3 hätt a Solo")
            bidding_round.append(f"1 lässt den Vortritt.")
            bidding_round.append(f"2 lässt den Vortritt.")
            bidding_round.append(f"3 spielt Eichel")

        result = '113 Augen'

        if i == 0:
            result = '-'

        game_protocol = dict(number=number, players=players, bidding=bidding_round, type=game_type, result=result)
        fieldnames = ['number', 'players', 'bidding', 'type', 'result']
        with open("./test_data_processing.csv", 'a', encoding='utf-8', newline='') as f:
            writer = DictWriter(f, fieldnames=fieldnames, delimiter=';')
            #writer.writeheader()
            writer.writerow(game_protocol)


def test_get_hands_games_position():
    filename = "/home/pirate/PycharmProjects/SchafkopfAI/testing/test_data_processing.csv"
    games = pandas.read_csv(filename, sep=";", header=[0])
    data_list, _, _ = get_hands_games_position(games)

    """
    Ok, now we expect
    - 4 entries from the first line of the csv - every player passed
    - 1 entry from the second line - the first players announced and then we have to forget the rest
    - 2 entries from the third line
    - 3 entries from the fourth line
    - 4 entries from the fifth line - we can use all the information
    - ...
    """

    # line 2 of the csv
    for i in range(4):
        assert data_list[i] == (translate_cards(cards[i]), i, [[None, None], [None, None], [None, None], [None, None]], None)

    # line 3 of the csv
    assert data_list[4] == (translate_cards(cards[0]), 0, [[3, 0], [None, None], [None, None], [None, None]], 113)

    # line 4 of the csv
    assert data_list[5] == (translate_cards(cards[0]), 0, [[None, None], [3, 0], [None, None], [None, None]], 113)
    assert data_list[6] == (translate_cards(cards[1]), 1, [[None, None], [3, 0], [None, None], [None, None]], 113)

    # line 5 of the csv
    assert data_list[7] == (translate_cards(cards[0]), 0, [[None, None], [None, None], [3, 0], [None, None]], 113)
    assert data_list[8] == (translate_cards(cards[1]), 1, [[None, None], [None, None], [3, 0], [None, None]], 113)
    assert data_list[9] == (translate_cards(cards[2]), 2, [[None, None], [None, None], [3, 0], [None, None]], 113)

    # line 6 of the csv
    assert data_list[10] == (translate_cards(cards[0]), 0, [[None, None], [None, None], [None, None], [3, 0]], 113)
    assert data_list[11] == (translate_cards(cards[1]), 1, [[None, None], [None, None], [None, None], [3, 0]], 113)
    assert data_list[12] == (translate_cards(cards[2]), 2, [[None, None], [None, None], [None, None], [3, 0]], 113)
    assert data_list[13] == (translate_cards(cards[3]), 3, [[None, None], [None, None], [None, None], [3, 0]], 113)

    # line 7 of the csv
    assert data_list[14] == (translate_cards(cards[1]), 1, [False, [3, 2], [None, None], [None, None]], 113)

    # line 8 of the csv
    assert data_list[15] == (translate_cards(cards[2]), 2, [False, [None, None], [3, 2], [None, None]], 113)

    # line 9 of the csv
    assert data_list[16] == (translate_cards(cards[3]), 3, [False, [None, None], [None, None], [3, 2]], 113)

    # line 10 of the csv
    assert data_list[17] == (translate_cards(cards[0]), 0, [[None, None], False, [3, 2], [None, None]], 113)
    assert data_list[18] == (translate_cards(cards[2]), 2, [[None, None], False, [3, 2], [None, None]], 113)

    # line 11 of the csv
    assert data_list[19] == (translate_cards(cards[0]), 0, [[None, None], False, [None, None], [3, 2]], 113)
    assert data_list[20] == (translate_cards(cards[3]), 3, [[None, None], False, [None, None], [3, 2]], 113)

    # line 12 of the csv
    assert data_list[21] == (translate_cards(cards[0]), 0, [[None, None], [None, None], False, [3, 2]], 113)
    assert data_list[22] == (translate_cards(cards[1]), 1, [[None, None], [None, None], False, [3, 2]], 113)
    assert data_list[23] == (translate_cards(cards[3]), 3, [[None, None], [None, None], False, [3, 2]], 113)

    # line 13 of the csv
    assert data_list[24] == (translate_cards(cards[1]), 1, [False, [None, 1], [3, 2], [None, None]], 113)
    assert data_list[25] == (translate_cards(cards[2]), 2, [False, [None, 1], [3, 2], [None, None]], 113)

    # line 14 of the csv
    assert data_list[26] == (translate_cards(cards[1]), 1, [False, [None, 1], [None, None], [3, 2]], 113)
    assert data_list[27] == (translate_cards(cards[3]), 3, [False, [None, 1], [None, None], [3, 2]], 113)

    # line 15 of the csv
    assert data_list[28] == (translate_cards(cards[2]), 2, [False, [None, None], [None, 1], [3, 2]], 113)
    assert data_list[29] == (translate_cards(cards[3]), 3, [False, [None, None], [None, 1], [3, 2]], 113)

    # line 16 of the csv
    assert data_list[30] == (translate_cards(cards[0]), 0, [[None, None], False, [None, 1], [3, 2]], 113)
    assert data_list[31] == (translate_cards(cards[2]), 2, [[None, None], False, [None, 1], [3, 2]], 113)
    assert data_list[32] == (translate_cards(cards[3]), 3, [[None, None], False, [None, 1], [3, 2]], 113)

    # line 17 of the csv
    assert data_list[33] == (translate_cards(cards[2]), 2, [False, False, [None, 1], [3, 2]], 113)
    assert data_list[34] == (translate_cards(cards[3]), 3, [False, False, [None, 1], [3, 2]], 113)

#create_test_csv()
test_get_hands_games_position()