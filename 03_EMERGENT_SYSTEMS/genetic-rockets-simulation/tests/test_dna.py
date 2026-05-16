from genetic_rockets.dna import DNA


def test_random_dna_has_requested_lifespan():
    dna = DNA.random(lifespan=25, max_force=0.3)

    assert dna.lifespan == 25
    assert len(dna.genes) == 25


def test_crossover_preserves_lifespan():
    parent_a = DNA.random(lifespan=30, max_force=0.3)
    parent_b = DNA.random(lifespan=30, max_force=0.3)

    child = parent_a.crossover(parent_b)

    assert child.lifespan == 30
    assert len(child.genes) == 30


def test_mutation_preserves_lifespan():
    dna = DNA.random(lifespan=40, max_force=0.3)

    mutated = dna.mutate(mutation_rate=0.5)

    assert mutated.lifespan == 40
    assert len(mutated.genes) == 40


def test_invalid_lifespan_is_rejected():
    try:
        DNA.random(lifespan=0, max_force=0.3)
    except ValueError as exc:
        assert "lifespan" in str(exc)
    else:
        raise AssertionError("DNA.random should reject lifespan < 1")
