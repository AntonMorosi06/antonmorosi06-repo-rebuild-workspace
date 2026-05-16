from artificial_life_evolution.dna import DNA


def test_random_prey_dna_has_expected_ranges():
    dna = DNA.random_prey()

    assert 0.80 <= dna.speed <= 3.80
    assert 35.0 <= dna.vision <= 230.0
    assert 0.0 <= dna.fertility <= 1.0
    assert 0.0 <= dna.nocturnality <= 1.0


def test_random_predator_dna_has_expected_ranges():
    dna = DNA.random_predator()

    assert 0.80 <= dna.speed <= 3.80
    assert 35.0 <= dna.vision <= 230.0
    assert 0.0 <= dna.aggression <= 1.0
    assert 0.0 <= dna.nocturnality <= 1.0


def test_dna_mutation_preserves_valid_ranges():
    dna = DNA.random_prey()
    mutated = dna.mutate(rate=1.0, strength=0.25)

    assert 0.80 <= mutated.speed <= 3.80
    assert 35.0 <= mutated.vision <= 230.0
    assert 0.0 <= mutated.aggression <= 1.0
    assert 0.0 <= mutated.sociability <= 1.0
    assert 0.0 <= mutated.fertility <= 1.0
    assert 0.35 <= mutated.metabolism <= 2.10
    assert 0.0 <= mutated.nocturnality <= 1.0
    assert 500.0 <= mutated.longevity <= 2600.0
    assert 0.0 <= mutated.hue <= 1.0


def test_dna_crossover_returns_dna():
    a = DNA.random_prey()
    b = DNA.random_prey()
    child = a.crossover(b)

    assert isinstance(child, DNA)
    assert child.speed in (a.speed, b.speed)
