# Tic Tac Tactics

A reinforcement model that is able to learn Tic Tac Toe using Q-Learning.

## Project Aims

* Train two AI players to play Tic Tac Toe competently with reasonable training time.
* Analyse the learning process of the AI and report findings.

## Key Findings

* Total training time was ~20 minutes to play 2,000,000 games of Tic Tac Toe between two AI players.
* Over 1,000,000 training games each:

  * The first-turn AI (Naughts) had a record of 841,514 wins, 65,333 losses and 93,153 draws.
  * The second-turn AI (Crosses) had a record of 754,516 wins, 124,131 losses and 121,353 draws.
* Across each training run of 100,000 games, both players showed rapid improvements within the first 5,000 to 10,000 games before stagnating.
* First-turn AI (Naughts) learned a tendency to open play with bottom centre. Perfect play against this strategy can only result in a draw.
* Second-turn AI generally learned to respond to a corner first-move with a move in the centre of the board.
* Against a perfect playing Minimax algorithm:

  * First-turn AI (Naughts) will consistently play to a draw.
  * Second-turn AI (Crosses) will lose due to an inappropriate forking strategy.

## Motivation

Tic Tac Toe is a solved game. This means that the optimal way to play has been discovered such that the outcome is now predetermined. There is no shortage of tic tac toe projects built using the Minimax algorithm that result in perfect play. The minimax algorithm allows the computer to look at the Tic Tac Toe board, analyse all available combinations of moves, and then decide which move will result in an optimal outcome (a win). When two perfect players analyse the most optimal move, the game always ends in a draw.

While this is fine for Tic Tac Toe, the Minimax alogrithm, even with alpha beta pruning, quickly becomes inefficient when the decision space grows expontentially larger. Even games such as chess require enormous computational resources to analyse every future move. As real world problems are often far more complex than simple games, better approaches are needed when it is not possible to analyse every possible decision in real-time.

This is why I decided to explore the effectiveness of teaching an AI to learn Tic Tac Toe without relying on lookahead strategies. I opted for reinforcement learning, a technique that involves enabling an AI to iteratively play Tic Tac Toe against itself or other AI opponents. Through this process, the AI learns from its experiences, remembers successful moves, and adjusts its strategy based on past performance. By rewarding the AI for good play and penalizing bad play, reinforcement learning encourages the development of effective strategies organically.

Reinforcement learning presents several advantages over traditional approaches like Minimax. Unlike Minimax, which requires exhaustive search and analysis of future moves, reinforcement learning adapts and learns dynamically from its interactions, making it more scalable and applicable to real-world problems. Moreover, reinforcement learning is versatile and can be extended to more complex scenarios beyond Tic Tac Toe, such as playing video games or controlling robots. Mastering reinforcement learning techniques is therefore essential for data scientists, as it equips them with the skills needed to tackle a wide range of challenges across various domains.

Besides, who wants to play against a minimax algorithm? It's boring. Tic Tac Toe remains a simple and inexpensive game that is excellent for teaching children basic problem solving skills and strategical thinking. Providing just the right amount of challenge to ensure that the game remains fun and interesting enough is important for maintaining a child's attention and providing them with learning opportunities.

## Training Methodology

Each AI was set with a learning rate of 0.1, a discount factor of 0.9. and an epsilon of 0.1. First, the second-turn AI (Crosses) was trained for 100,000 games against a random moving opponent. Then the first-turn AI (Naughts) was trained against the previously trained Crosses for 100,000 games. This would complete a single training run. For the next run, the Crosses AI would be trained against the previously trained Naughts AI and vice-versa. Ten training runs were performed of a total of 2,000,000 games of Tic Tac Toe.

## Play against the AI

I have coded up a web application where you can play against the AI trained in this project. You can also  play the minimax algorithm if you want to either lose or draw.

You can find a link to the application [HERE](tictactactics.azurewebsites.net).

## Future Considerations

Were I to do this project again, or a similar project in the future implementing Q-learning I would seek to explore the following:

- Simulaneous training of AI where they learn from each other during training. This may result in more competitive training runs.
- Exploration of hyper-parameter tuning, explore/exploit rates and the
- Implementing board symmetries and inversions into the learning algorithm. This theoretically may speed up the learning process, saving time and resource costs.
- Implementing a mechanism where the AI will raise or lower its own level of play to match the skill level of its opponent.

## Conclusions

Tic Tac Toe is such a simple game that it is unsurprising that it took very little time and resources to train a competent (but not completely perfect) AI. From a random moving opponent, the AI was able to demonstrate known strategies in Tic Tac Toe, such that most of the time you will end up playing to a draw.
