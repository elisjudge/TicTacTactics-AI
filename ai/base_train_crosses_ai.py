import json
import logging
import numpy as np
import time

from ai.base_ai import BaseAI
from ai.trained_ai import TrainedAI
from game.tic_tac_toe import TicTacToe

# Training Parameters
N_EPISODES = 100000
EPOCH_LENGTH = 1000

# # Metrics
# total_wins = 0
# total_losses = 0
# total_draws = 0
# total_q_value_changes = []
# total_rewards = []

# Logger
logging.basicConfig(filename='ai/data/training_metrics.log',
                    level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

def play_game(player1: BaseAI, player2: TrainedAI):
    game = TicTacToe(player1=player1, player2=player2)
    history = []  # Initialize a list to keep track of the game history
    
    while not game.board.is_full():
        current_state = game.board.get_board_state()
        current_move = game.current_player.select_move(valid_moves=game.valid_moves, state=current_state)
        
        # Record the state and action in the game history
        history.append((np.copy(current_state), current_move, game.current_player)) 
        
        game.execute_move(player=game.current_player, move=current_move)
        game.winner = game.is_winner()
        
        if game.winner:
            return game.current_player, game.board.get_board_state(), history
        
        game.update_valid_moves(move=current_move)
        game.switch_turns()
    
    if game.board.is_full() and not game.winner:
        return None, game.board.get_board_state(), history
    else:
        raise Exception("Something went wrong with the game")

def save_model(player:TrainedAI):
    with open("./ai/models/crosses.json", "w", encoding="utf-8", ) as file:
        json.dump(player.q_table, file, indent=4)

def train_crosses_ai(num_episodes=N_EPISODES, epoch_length=EPOCH_LENGTH):
    player1 = BaseAI("BaseAI", 1)
    player2 = TrainedAI("CrossesAI", 2)

    epoch_wins = 0
    epoch_losses = 0
    epoch_draws = 0
    epoch_rewards = 0 
    epoch_q_value_changes = []

    
    for episode in range(1, num_episodes + 1):
        game_q_value_change = 0

        try:
            winner, final_state, history = play_game(player1, player2)

            if winner == player2:
                reward = 1
                epoch_wins += 1
            elif winner == player1:
                reward = -1
                epoch_losses += 1
            else: 
                reward = 0.5
                epoch_draws +=1
            
            epoch_rewards += reward

            # Filter out the moves made by the CrossesAI
            crosses_moves = [(state, action) for state, action, player in history if player == player2]


            for i, (state, action) in enumerate(crosses_moves):
                next_state = crosses_moves[i + 1][0] if i + 1 < len(crosses_moves) else final_state
                q_value_change = player2.update_q_value(hashed_state=player2.hash_state(state), action=str(action), 
                                       reward=reward, hashed_final_state=player2.hash_state(next_state))
                game_q_value_change += q_value_change

            epoch_q_value_changes.append(game_q_value_change)

            if episode % epoch_length == 0:
                total_epoch_explorations, total_epoch_moves = player2.exploration_count, player2.total_moves_made
                average_exploration_rate = total_epoch_explorations / total_epoch_moves if total_epoch_moves else 0
                average_q_value_change = sum(epoch_q_value_changes) / len(epoch_q_value_changes)
                logging.info(f'Epoch {episode // epoch_length}: Win Rate: {epoch_wins / epoch_length}, Loss Rate: {epoch_losses / epoch_length}, Draw Rate: {epoch_draws / epoch_length}, '
                             f'Average Reward: {epoch_rewards / epoch_length}, Average Q-Value Change: {average_q_value_change}, '
                             f'Average Exploration Rate: {average_exploration_rate}')
                
                epoch_wins, epoch_losses, epoch_draws, epoch_rewards = 0, 0, 0, 0
                epoch_q_value_changes.clear() 
                total_epoch_explorations, total_epoch_moves = 0, 0
                player2.exploration_count, player2.total_moves_made = 0, 0 
                    
        except Exception as e:
            logging.exception("An error occurred during training.") 
    
    save_model(player=player2)

if __name__ == "__main__":
    start_time = time.time()
    train_crosses_ai()

    end_time = time.time()
    print(f"Total execution time: {end_time - start_time} seconds")