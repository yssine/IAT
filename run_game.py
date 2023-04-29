import os, glob
from playsound import playsound
from time import sleep, time
from game.SpaceInvaders import SpaceInvaders
from controller.keyboard import KeyboardController
from controller.random_agent import RandomAgent
from controller.qagent import QAgent

from epsilon_profile import EpsilonProfile
import logging


def main():

    hs=open(r"hs","r").read()
    game = SpaceInvaders(display=True, High_score = int(hs))



    gamma = 0.95
    alpha = 1
    eps_profile = EpsilonProfile(0.7, 0.05)
    max_steps = 5000
    n_episodes = 200

    def Train():
        fileName = f"""Q_{"SXY"}_E{n_episodes}_S{max_steps}_G{gamma}_I{eps_profile.initial}_F{eps_profile.final}"""
        controller = QAgent(game, eps_profile, gamma, alpha, fileName)
        startTime = time()
        controller.learn(game, n_episodes, max_steps)
        endTime = time()
        controller.saveQToFile(os.path.join("LearnedQ", fileName))
        print("\n############################################################################")
        print("FINISHED LEARNING")
        print(f"\tn_episodes: {n_episodes}")
        print(f"\tmax_steps: {max_steps}")
        print(f"\tgamma: {gamma}")
        print(f"\teps_profile (initial, final, dec_episode, dec_step): {eps_profile.initial}, {eps_profile.final}, {eps_profile.dec_episode},{eps_profile.dec_step}")
        print(f"\ttime learning: , {endTime - startTime}")
        print("\n############################################################################")

    controller = QAgent(game, eps_profile, gamma, alpha)
    # controller = KeyboardController()

    try:
        controller.loadQFromFile(os.path.join(os.path.abspath("LearnedQ"),f"""Q_{"SXY"}_E{n_episodes}_S{max_steps}_G{gamma}_I{eps_profile.initial}_F{eps_profile.final}.npy"""))
    except Exception:
        Train()
        controller.loadQFromFile(
        os.path.join(os.path.abspath("LearnedQ"),f"""Q_{"SXY"}_E{n_episodes}_S{max_steps}_G{gamma}_I{eps_profile.initial}_F{eps_profile.final}.npy"""))






    state = game.reset()
    isOn,frame=True,0
    while isOn:
        action = controller.select_greedy_action(state)
        # action = controller.select_action(state)
        state, reward, is_done = game.step(action)
        print(f"\r#> Score: {game.score_val}  ", end=" ")
        if is_done:
            isOn=False
            if int(game.score_val) > int(hs):
                _=open(r"hs","w").write(f"{game.score_val}")
            game.close()
        sleep(0.0001)
    print("\nGAME OVER")

    playsound("game/data/sad-trombone.mp3")




if __name__ == '__main__':
    main()
