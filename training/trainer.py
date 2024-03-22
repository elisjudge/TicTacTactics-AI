from game.tic_tac_toe import TicTacToe
from game.player import Player
from utils.logger import TrainingLogger

import json
import numpy as np

class Trainer:
    def __init__(self, player1:Player, player2:Player, target:str, 
                 num_episodes:int, epoch_length:int, log_directory:str, 
                 log_filename:str):
        """
        Initializes the Trainer.
        :param player1: Instance of the first player's AI.
        :param player2: Instance of the second player's AI.
        :param target: Determines who is the training target (Naughts or Crosses)
        :param num_episodes: Total number of episodes to run.
        :param epoch_length: Number of episodes per epoch.
        :param log_directory: Directory where the log file will be saved.
        :param log_filename: Name of the log file.
        """
        self.player1 = player1
        self.player2 = player2
        self.training_target = target
        self.num_episodes = num_episodes
        self.epoch_length = epoch_length
        self.logger = TrainingLogger(log_directory, log_filename)

    def play_game(self):
        """
        Plays a single game of TicTacToe between player1 and player2.
        """
        game = TicTacToe(self.player1, self.player2)

        while not game.board.is_full():
            current_state = game.board.get_board_state()
            current_move = game.current_player.select_move(valid_moves=game.valid_moves, state=current_state)
            
            game.history.append((np.copy(current_state), current_move, game.current_player))
            
            game.execute_move(game.current_player, current_move)
            game.winner = game.is_winner()
            
            if game.winner:
                return game.current_player, game.board.get_board_state(), game.history
            
            game.update_valid_moves(move=current_move)
            game.switch_turns()
        
        if game.board.is_full() and not game.winner:
            return None, game.board.get_board_state(), game.history
        else:
            raise Exception("Something went wrong with the game")
    
    def train_ai(self):
        """
        Trains the AI by playing a series of games and updating the AI's strategy based on the outcomes.
        """
        epoch_wins, epoch_losses, epoch_draws, epoch_rewards, epoch_q_value_changes = self.reset_epoch_stats()

        for episode in range(1, self.num_episodes + 1):
            try:
                winner, final_state, game_history = self.play_game()
                reward = self.assign_rewards(winner)
                epoch_wins, epoch_losses, epoch_draws = self.update_epoch_win_loss_results(winner, epoch_wins, epoch_losses, epoch_draws)
                epoch_rewards += reward
                move_history = self.filter_moves(game_history)
                epoch_q_value_changes = self.update_epoch_q_value_changes(move_history, final_state, reward, epoch_q_value_changes)

                if episode % self.epoch_length == 0:
                    average_exploration_rate = self.get_exploration_rate()
                    self.log_epoch_results(episode, epoch_wins, epoch_losses, epoch_draws, epoch_rewards, epoch_q_value_changes, average_exploration_rate)
                    epoch_wins, epoch_losses, epoch_draws, epoch_rewards, epoch_q_value_changes = self.reset_epoch_stats()

            except Exception as e:
                self.logger.log_message('error', f'An error occurred during training: {str(e)}')

        self.save_model()
        self.logger.close_logger()

    def assign_rewards(self, winner):
        """
        Assigns rewards based on the game outcome.
        """
        if self.training_target == "Naughts":
            if winner == self.player1:
                return 1  
            elif winner == self.player2:
                return -1  
            else:
                return 0  
        
        elif self.training_target == "Crosses":
            if winner == self.player2:
                return 1  
            elif winner == self.player1:
                return -1 
            else:
                return 0.5 
            
    def update_epoch_win_loss_results(self, winner, epoch_wins, epoch_losses, epoch_draws):
        """
        Keeps track of the game outcomes over the epoch .
        """
        if self.training_target == "Naughts":
            if winner == self.player1:
                epoch_wins += 1
            elif winner == self.player2:
                epoch_losses += 1
            else:
                epoch_draws += 1
        elif self.training_target == "Crosses":
            if winner == self.player2:
                epoch_wins += 1
            elif winner == self.player1:
                epoch_losses += 1
            else:
                epoch_draws += 1
        
        return epoch_wins, epoch_losses, epoch_draws
    
    def update_epoch_q_value_changes(self, move_history, final_state, reward, epoch_q_value_changes):
            game_q_value_change = 0
            for i, (state, action) in enumerate(move_history,):
                next_state = move_history[i + 1][0] if i + 1 < len(move_history) else final_state

                if self.training_target == "Naughts":
                    q_value_change = self.player1.update_q_value(hashed_state=self.player1.hash_state(state), action=str(action), 
                                        reward=reward, hashed_final_state=self.player1.hash_state(next_state))
                elif self.training_target == "Crosses":
                    q_value_change = self.player2.update_q_value(hashed_state=self.player2.hash_state(state), action=str(action), 
                                        reward=reward, hashed_final_state=self.player2.hash_state(next_state))
                
                game_q_value_change += q_value_change
            epoch_q_value_changes.append(game_q_value_change)
            return epoch_q_value_changes
    
    def get_exploration_rate(self):
        if self.training_target == "Naughts":
            total_epoch_explorations, total_epoch_moves = self.player1.exploration_count, self.player1.total_moves_made
            average_exploration_rate = total_epoch_explorations / total_epoch_moves if total_epoch_moves else 0
        elif self.training_target == "Crosses":
            total_epoch_explorations, total_epoch_moves = self.player2.exploration_count, self.player2.total_moves_made
            average_exploration_rate = total_epoch_explorations / total_epoch_moves if total_epoch_moves else 0

        return average_exploration_rate
 
    def reset_epoch_stats(self):
        return 0, 0, 0, 0, [] 
    
    def filter_moves(self, game_history):
        if self.training_target == "Naughts":
            filtered_history = [(state, action) for state, action, player in game_history if player == self.player1]
        elif self.training_target == "Crosses":
            filtered_history = [(state, action) for state, action, player in game_history if player == self.player2]

        return filtered_history


    def log_epoch_results(self, episode, wins, losses, draws, rewards, q_value_changes, average_exploration_rate):
        """
        Logs the results of each training epoch.
        """
        average_reward = rewards / self.epoch_length
        average_q_value_change = sum(q_value_changes) / len(q_value_changes) if q_value_changes else 0
        self.logger.log_message('info', f'Epoch {episode // self.epoch_length}: '
                                        f'Win Rate: {wins / self.epoch_length}, '
                                        f'Loss Rate: {losses / self.epoch_length}, '
                                        f'Draw Rate: {draws / self.epoch_length}, '
                                        f'Average Reward: {average_reward}, '
                                        f'Average Q-Value Change: {average_q_value_change}, '
                                        f'Average Exploration Rate: {average_exploration_rate}, '
        )

    def save_model(self):
        if self.training_target == "Naughts":
            with open(f"./ai/models/naughts/naughts_gen{self.player1.generation}.json", "w", encoding="utf-8") as file:
                json.dump(self.player1.q_table, file, indent=4)
        elif self.training_target == "Crosses":
            with open(f"./ai/models/crosses/crosses_gen{self.player2.generation}.json", "w", encoding="utf-8") as file:
                json.dump(self.player2.q_table, file, indent=4)
        