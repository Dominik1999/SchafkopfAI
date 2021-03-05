import os
import glob
import pandas as pd

os.chdir("/media/pirate/Samsung_T5/EXTERN/Schafkopf-AI/Spiele")
extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
#combine all files in the list
combined_csv = pd.concat([pd.read_csv(f, sep=";", header=[0]) for f in all_filenames])
combined_csv.drop(columns = 'Unnamed: 0')
#export to csv
combined_csv.to_csv("merged-games.csv", sep=";", columns=combined_csv.columns.to_list(), encoding='utf-8', index=False)
