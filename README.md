# T-RexAIGame
Play against an AI that teaches itself to play a jumping T-Rex game

Using NEAT (NeuroEvolution of Augmenting Topologies), we train an AI to play a jumping T-rex game where the T-rex jumps over cacti (similar to the Google Chrome dinosaur game)

When the program is run, it prompts the user to select the AI difficulty. In the game, we run 1 generation of genomes and change the population size depending on the user selected difficulty (easy = 10, normal = 30, hard = 50). We activate each neural network by giving it data about the y position of the dino and the euclidian distance between the dino and the cactus. The program displays the entire population of genomes in the game-play so we are able to visualize the improvement of the AI as it learns to play the game.

The user is displayed on the top half of the screen.
To jump over cacti, the user presses space.
If the user collides with a cactus, the AI wins the game.
If all genomes of AI collide with a cactus, the user wins the game.
When the game is won by either the user or the AI, the screen displays the result for a few seconds before prompting the user to select the AI difficulty and play again.

Possible future improvements:
- adjust the population size and the number of generations for each level of difficulty. Store the best performing genome in a variable. When the user selects the difficulty of the AI, we only run that genome.
- improve game graphics
- add more features to the T-Rex and more obstacles (Ex: T-rex can duck under obstacles)
- use Sprites to create groups of obstacles and increase difficulty of the game

Please feel free to download the demo video to see how the program works
