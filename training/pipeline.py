from ai.base_ai import BaseAI
from ai.trained_ai import TrainedAI
from training.trainer import Trainer

import config as c
import json
import time

class Pipeline():
    def __init__(self) -> None:
        self.target = "Crosses"
    
    def load_player(self, generation):
        if self.target == "Naughts":
            name = f"naughts_gen{generation}"
            symbol = c.NAUGHTS
            player = TrainedAI(name=name, symbol=symbol, generation=generation)

            if generation > 1:
                filepath = f"./ai/models/naughts/naughts_gen{generation-1}.json"
                with open(filepath, "r", encoding="utf-8") as brain_file:
                    q_table = json.load(brain_file)
                player.q_table = q_table

        elif self.target == "Crosses":
            name = f"crosses_gen{generation}"
            symbol = c.CROSSES
            player = TrainedAI(name=name, symbol=symbol, generation=generation)

            if generation > 1:
                filepath = f"./ai/models/crosses/crosses_gen{generation-1}.json"
                with open(filepath, "r", encoding="utf-8") as brain_file:
                    q_table = json.load(brain_file)
                player.q_table = q_table
        
        return player        

    def load_opponent(self, generation):
        if self.target == "Naughts":
            name = f"crosses_gen{generation}"
            symbol = c.CROSSES
            opponent = TrainedAI(name=name, symbol=symbol, generation=generation)
            
            filepath = f"./ai/models/crosses/crosses_gen{generation}.json"
            with open(filepath, "r", encoding="utf-8") as brain_file:
                q_table = json.load(brain_file)
            opponent.q_table = q_table

        elif self.target == "Crosses":
            if generation == 1:
                name = f"Base_AI"
                symbol = c.NAUGHTS
                opponent = BaseAI(name=name, symbol=symbol)

            elif generation > 1:
                name = f"naughts_gen{generation-1}"
                symbol = c.NAUGHTS
                opponent = TrainedAI(name=name, symbol=symbol, generation=generation)

                filepath = f"./ai/models/naughts/naughts_gen{generation-1}.json"
                with open(filepath, "r", encoding="utf-8") as brain_file:
                    q_table = json.load(brain_file)
                opponent.q_table = q_table
        
        return opponent        
    
    def get_log_directory(self):
       if self.target == "Naughts":
           return "./ai/data/naughts/"
       elif self.target == "Crosses":   
           return "./ai/data/crosses/"

    def generate_log_filename(self, generation):
        if self.target == "Naughts":
           return f"naughts_gen{generation}"
        elif self.target == "Crosses":   
           return f"crosses_gen{generation}"

    def switch_targets(self):
        self.target = "Naughts" if self.target == "Crosses" else "Crosses"

    
    def run_pipeline(self):
        for run in range(c.N_GENERATIONS):
            generation = run+1
            # Run two pair training sessions, beginning with Crosses
            pair_session = 1
            while pair_session <= 2:
                training_target = self.load_player(generation=generation)
                training_partner = self.load_opponent(generation=generation)

                if self.target == "Crosses":
                    print(f"Training Crosses Generation {generation}")
                    trainer = Trainer(player1=training_partner,
                                    player2=training_target,
                                    target=self.target,
                                    num_episodes=c.N_EPISODES,
                                    epoch_length=c.EPOCH_LENGTH,
                                    log_directory= self.get_log_directory(),
                                    log_filename=self.generate_log_filename(generation=generation))
                elif self.target == "Naughts":
                    print(f"Training Naughts Generation {generation}")
                    trainer = Trainer(player1=training_target,
                                    player2=training_partner,
                                    target=self.target,
                                    num_episodes=c.N_EPISODES,
                                    epoch_length=c.EPOCH_LENGTH,
                                    log_directory= self.get_log_directory(),
                                    log_filename=self.generate_log_filename(generation=generation))
                start_time = time.time()
                trainer.train_ai()
                end_time = time.time()
                execution_time = end_time - start_time
                print("Training time:", execution_time, "seconds")
                self.switch_targets()
                pair_session += 1