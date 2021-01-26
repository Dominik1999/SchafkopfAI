from PIMC_Player import PIMCPlayer
from RandomPlayer import RandomPlayer
from Game_Environment import SchafkopfEnv


def main():
    pimc_player = PIMCPlayer(10, 40, RandomPlayer())

    participants = [pimc_player, RandomPlayer(), RandomPlayer(), RandomPlayer()]

    number_of_games = 1000

    #for i in range(len(participants)):
    #    for j in range(i + 1, len(participants)):
    p1 = participants[0]
    p2 = participants[1]
    p3 = participants[2]
    p4 = participants[3]

    cummulative_reward = [0, 0, 0, 0]
    players = [p1, p2, p3, p4]
            #for k in range(2):  # run the same tournament twice with different positions of players
            #    print(' ')
    schafkopf_env = SchafkopfEnv(seed=1)
            #    if k == 0:
            #        players = [p1, p1, p2, p2]
            #    else:
            #        players = [p2, p2, p1, p1]
            #        cummulative_reward.reverse()

                # tournament loop
    for game_nr in range(1, number_of_games + 1):
        state, reward, terminal = schafkopf_env.reset()
        while not terminal:
            action, prob = players[state["game_state"].current_player].act(state)
            state, reward, terminal = schafkopf_env.step(action, prob)

        cummulative_reward = [cummulative_reward[m] + reward[m] for m in range(4)]

        if game_nr % 100 == 0:
            print('.', end='')
                # schafkopf_env.print_game()

    print(cummulative_reward)
    #print("player " + str(i) + " vs. player " + str(j) + " = " + str(
    #    (cummulative_reward[2] + cummulative_reward[3]) / (2 * 2 * number_of_games)) + " to " + str(
    #    (cummulative_reward[0] + cummulative_reward[1]) / (2 * 2 * number_of_games)))
            # print("--------Episode: " + str(i_episode) + " game simulation (s) = " + str(t1 - t0))
            # print("--------Cummulative reward: " + str(cummulative_reward))
            # print("--------per game reward: " + str([i /i_episode for i in cummulative_reward] ))
            # print("--------MCTS rewards: " + str(((cummulative_reward[1] + cummulative_reward[3]) / i_episode)/2))
            # print("--------MCTS rewards: " + str(((cummulative_reward[1] + cummulative_reward[3]) / i_episode)/2))


if __name__ == '__main__':
    main()
