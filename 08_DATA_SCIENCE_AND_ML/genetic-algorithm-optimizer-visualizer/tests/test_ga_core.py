from genetic_algorithm_visualizer.ga import GAConfig, GeneticAlgorithm
from genetic_algorithm_visualizer.genome import Individual, clamp_genome
from genetic_algorithm_visualizer.landscapes import get_landscape, landscape_names
from genetic_algorithm_visualizer.metrics import best_individual, diversity, mean_fitness


def test_landscape_names_include_expected_values():
    names = landscape_names()

    assert "sphere" in names
    assert "rastrigin" in names
    assert "himmelblau" in names
    assert "ridge" in names
    assert "multi_peak" in names


def test_clamp_genome_limits_values():
    assert clamp_genome([-10.0, 10.0], (-5.0, 5.0)) == [-5.0, 5.0]


def test_sphere_landscape_optimum_is_center():
    sphere = get_landscape("sphere")

    assert sphere.fitness([0.0, 0.0]) > sphere.fitness([2.0, 2.0])


def test_ga_initializes_population():
    ga = GeneticAlgorithm(landscape_name="sphere", config=GAConfig(population_size=20), seed=1)

    assert len(ga.population) == 20
    assert ga.generation == 0
    assert ga.history


def test_ga_step_advances_generation():
    ga = GeneticAlgorithm(landscape_name="sphere", config=GAConfig(population_size=30), seed=1)
    old_generation = ga.generation

    ga.step()

    assert ga.generation == old_generation + 1
    assert len(ga.population) == 30
    assert len(ga.history) >= 2


def test_best_individual_has_highest_fitness():
    population = [
        Individual([0.0, 0.0], fitness=1.0),
        Individual([1.0, 1.0], fitness=3.0),
        Individual([2.0, 2.0], fitness=2.0),
    ]

    best = best_individual(population)

    assert best.fitness == 3.0


def test_mean_fitness_and_diversity():
    population = [
        Individual([0.0, 0.0], fitness=1.0),
        Individual([3.0, 4.0], fitness=3.0),
    ]

    assert mean_fitness(population) == 2.0
    assert diversity(population) == 5.0


def test_ga_on_sphere_improves_over_generations():
    ga = GeneticAlgorithm(landscape_name="sphere", config=GAConfig(population_size=50), seed=2)
    start_best = ga.best().fitness

    for _ in range(25):
        ga.step()

    end_best = ga.best().fitness

    assert end_best >= start_best


def test_set_landscape_resets_population():
    ga = GeneticAlgorithm(landscape_name="sphere", config=GAConfig(population_size=20), seed=3)
    ga.step()
    ga.set_landscape("multi_peak")

    assert ga.landscape_name == "multi_peak"
    assert ga.generation == 0
    assert len(ga.population) == 20
