from pathlib import Path
import pandas as pd

files = [
    "/home/pirate/PycharmProjects/SchafkopfAI/models/training_data/process_data/bidding-pos-50000002-100983448.h5",
    "/home/pirate/PycharmProjects/SchafkopfAI/models/training_data/process_data/bidding-pos-51479630-52499997.h5",
    "/home/pirate/PycharmProjects/SchafkopfAI/models/training_data/process_data/bidding-pos-52300002-52699996.h5",
    "/home/pirate/PycharmProjects/SchafkopfAI/models/training_data/process_data/bidding-pos-101000001-102000070.h5",
    "/home/pirate/PycharmProjects/SchafkopfAI/models/training_data/process_data/bidding-pos-102000004-102199997.h5",
    "/home/pirate/PycharmProjects/SchafkopfAI/models/training_data/process_data/bidding-pos-102000004-103199999.h5",
    "/home/pirate/PycharmProjects/SchafkopfAI/models/training_data/process_data/bidding-pos-103000001-103999996.h5",
]
store = {}
games_data = []

#for path in Path('/home/pirate/PycharmProjects/SchafkopfAI/models/training_data/process_data/').iterdir():
#    if ".h5" in str(path):
#        files.append(str(path))

for i, path in enumerate(files):
    store[i] = pd.HDFStore(path)

for i in store.keys():
    games_data.append(store[i]['games_data'])
    print(f" Games Data {i} Shape: {games_data[i].shape}")

merged_games_data = pd.concat(games_data)
print(f"Merged Games Data Shape: {merged_games_data.shape}")

#for i in range(merged_games_data.shape[0]):
#    if merged_games_data.result.iloc[i][0] == 1 and merged_games_data.result.iloc[i][1] < 60:
#        merged_games_data.result.iloc[i][1] = merged_games_data.result.iloc[i][1] * 10

store = pd.HDFStore(f'/home/pirate/PycharmProjects/SchafkopfAI/models/training_data/data/Bidding-with-pos.h5')
store['games_data'] = merged_games_data
store.close()

# Merged Games Data Shape: (3349236, 4)