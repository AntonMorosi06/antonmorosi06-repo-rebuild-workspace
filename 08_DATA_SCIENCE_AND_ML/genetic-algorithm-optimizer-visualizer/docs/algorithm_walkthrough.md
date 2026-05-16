# Algorithm walkthrough

The reconstructed implementation follows this pipeline.

First, a random population is created inside the landscape bounds.

Second, each genome is evaluated with the selected fitness function.

Third, the best individuals are copied as elites.

Fourth, parents are selected using tournament selection.

Fifth, pairs of parents are recombined using blend crossover.

Sixth, children are mutated with Gaussian noise.

Seventh, mutated genomes are clamped to the valid search bounds.

Eighth, the new population replaces the old one.

Finally, generation metrics are recorded: best fitness, mean fitness, diversity and best coordinates.
