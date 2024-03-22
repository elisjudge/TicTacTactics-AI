# Tic Tac Tactics

A reinforcement model that is able to learn Tic Tac Toe using Q-Learning.

## Project Aims

* Train two AI players to play Tic Tac Toe competently with reasonable training time.
* Analyse the learning process of the AI and report findings.

## Motivation

Tic Tac Toe is a solved game. This means that the optimal way to play has been discovered such that the outcome is now predetermined. There is no shortage of tic tac toe projects built using the Minimax algorithm that result in perfect play. The minimax algorithm allows the computer to look at the Tic Tac Toe board, analyse all available combinations of moves, and then decide which move will result in an optimal outcome (a win). When two perfect players analyse the most optimal move, the game always ends in a draw.

While this is fine for Tic Tac Toe, the Minimax alogrithm, even with alpha beta pruning, quickly becomes inefficient when the decision space grows expontentially larger. Even games such as chess require enormous computational resources to analyse every future move. As real world problems are often far more complex than simple games, better approaches are needed when it is not possible to analyse every possible decision in real-time.

This is why I decided to explore the effectiveness of teaching an AI to learn Tic Tac Toe without relying on lookahead strategies. I opted for reinforcement learning, a technique that involves enabling an AI to iteratively play Tic Tac Toe against itself or other AI opponents. Through this process, the AI learns from its experiences, remembers successful moves, and adjusts its strategy based on past performance. By rewarding the AI for good play and penalizing bad play, reinforcement learning encourages the development of effective strategies organically.

Reinforcement learning presents several advantages over traditional approaches like Minimax. Unlike Minimax, which requires exhaustive search and analysis of future moves, reinforcement learning adapts and learns dynamically from its interactions, making it more scalable and applicable to real-world problems. Moreover, reinforcement learning is versatile and can be extended to more complex scenarios beyond Tic Tac Toe, such as playing video games or controlling robots. Mastering reinforcement learning techniques is therefore essential for data scientists, as it equips them with the skills needed to tackle a wide range of challenges across various domains.

Besides, who wants to play against a minimax algorithm? It's boring. Tic Tac Toe is an inexpensive game that can be good for teaching children basic problem solving skills. Ensuring that the game remains fun and interesting enough will help keep a childs attention, thus providing them with a learning opportunity. 

## Key Findings

* Total training time was ~20 minutes to play 2,000,000 games of Tic Tac Toe between two AI players.

## Play against the AI

I have coded up a web application where you can play against the AI trained in this project. I also implemented the Minimax algorithm for the sake of it. 

You can find a link to the application [HERE](tictactactics.azurewebsites.net).

## Future Considerations
