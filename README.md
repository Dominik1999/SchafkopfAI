# SchafkopfAI

Creating a program that beats me in my favorite game.

> Schafkopf (German: [ˈʃaːfkɔpf]), also called Bavarian Schafkopf to distinguish it from German Schafkopf, is an 18th-century German trick-taking card game of the Ace-Ten family for four players. It is still very popular in Bavaria, where it is their national card game played by around 2 million people, but it also played elsewhere in Germany and in Austria. It is an official cultural asset and important part of the Old Bavarian and Franconian way of life. Schafkopf is a mentally demanding pastime that is considered "the supreme discipline of Bavarian card games".

from https://en.wikipedia.org/wiki/Schafkopf

## Game Theoretical Categorization 
(by A. Sedlmayr)

> Game theoretic classification of Schafkopf
As Schafkopf is always played by four people, it is a multiplayer game. The chance player
only acts in the beginning by dealing the cards, after this a game history is a sequence of
(hidden) game mode proposals first during the bidding phase and played cards afterwards
in the trick playing phase. It is a game of imperfect information, since the cards of the
opponents are hidden, and during the bidding phase, players at first only announce if they
want to declare a game mode, not which game mode they want to declare. At the beginning
of trick play in partner mode the identity of the partner is hidden from three players as
well. Since the losing players total negative reward always equals the positive reward of
the winning players, it is a zero-sum game. It is a finite game, so Nash’s existence theorem
is applicable, hence at least one mixed strategy equilibrium exists.

## Architecture

Monte Carlo Tree Search supported by Neural Nets trying to guess the hidden information by its opponents actions


## To do
There is still a lot to do to create the first agent:
- [ ] add neural net for bidding phase (Bidding-NN)
- [ ] compare Bidding-NN to MonteCarlo-Approach
- [ ] add neural net for estimating opponent's cards based on publicly known history of actions
- [ ] play against agents of https://github.com/tobiasemrich/SchafkopfRL/tree/master/schafkopfrl


## Papers to consider
- https://arxiv.org/abs/1912.02318?fbclid=IwAR2RxzcHCRsahwMgrVola_6QnII5XxFvrJWgJ9x4zJjLebtJAHT8_4p-PtY
- https://arxiv.org/pdf/1906.04439.pdf
