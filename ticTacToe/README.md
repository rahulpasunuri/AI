This folder has two implementations of a Tic-Tac-Toe player.

Implementation -1 :
This implementation is in the ticTacToe.py. Some of the base knowledge required to play the game is incorporated directly into the code, and the computer will play based on this rules.


Implementation -2 :
This implementation is based on Reinforcement learning. Here, just the reward functions are incorporated into the game (0 for losing, and 1 for winning, 0.5 for a draw). The player plays against itself thousands of times, and learns the dynamics of the game on it's own. It used this knowledge to play against the humans.

train_TicTacToe.py - The reinforcement learning part is in here. 
play__TicTacToe.py - The agent plays against the human, based on the knowledge it learns about the environment.
policy.pickle - All the learnt knowlege is saved in this pickle file after training.
