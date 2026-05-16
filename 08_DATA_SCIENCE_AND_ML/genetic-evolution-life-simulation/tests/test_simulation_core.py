from genetic_evolution_life.genome import Genome
from genetic_evolution_life.simulation import LifeSimulation
from genetic_evolution_life.vector import Vec2
from genetic_evolution_life.world import PRESETS


def test_presets_exist():
    assert "balanced" in PRESETS
    assert "scarce" in PRESETS
    assert "abundant" in PRESETS
    assert "high_mutation" in PRESETS
    assert "drift" in PRESETS


def test_simulation_initializes_agents_and_food():
    simulation = LifeSimulation(preset_name="balanced", seed=1)

    assert simulation.agents
    assert simulation.food
    assert simulation.tick == 0
    assert simulation.metrics()["population"] > 0


def test_step_advances_tick():
    simulation = LifeSimulation(preset_name="balanced", seed=1)
    old_tick = simulation.tick

    simulation.step()

    assert simulation.tick == old_tick + 1


def test_food_collision_increases_energy():
    simulation = LifeSimulation(preset_name="balanced", seed=1)
    simulation.food.clear()
    agent = simulation.agents[0]
    agent.energy = 20.0
    simulation.spawn_food(position=agent.position.copy())
    before = agent.energy

    simulation.handle_food_collision(agent)

    assert agent.energy > before
    assert agent.eaten == 1


def test_genome_mutation_changes_or_preserves_valid_bounds():
    simulation = LifeSimulation(preset_name="balanced", seed=1)
    genome = Genome.random(simulation.rng)
    mutated = genome.mutated(simulation.rng)

    assert 0.65 <= mutated.speed <= 5.2
    assert 18.0 <= mutated.perception <= 220.0
    assert 0.004 <= mutated.metabolism <= 0.080
    assert 2.0 <= mutated.size <= 9.5
    assert 0.20 <= mutated.fertility <= 0.95
    assert 0.01 <= mutated.mutation_intensity <= 0.35


def test_reproduction_adds_child_when_forced():
    simulation = LifeSimulation(preset_name="balanced", seed=1)
    parent = simulation.agents[0]
    parent.age = 100
    parent.energy = parent.genome.reproduction_threshold() + 80.0
    before = len(simulation.agents)

    child = simulation.reproduce(parent)

    assert child is not None
    assert len(simulation.agents) == before + 1
    assert child.generation == parent.generation + 1
    assert child.lineage_id == parent.lineage_id


def test_add_food_and_agent_bursts():
    simulation = LifeSimulation(preset_name="balanced", seed=1)
    food_before = len(simulation.food)
    agents_before = len(simulation.agents)

    simulation.add_food_burst(count=5)
    simulation.add_agent_burst(count=5)

    assert len(simulation.food) >= food_before
    assert len(simulation.agents) >= agents_before


def test_metrics_have_expected_keys():
    simulation = LifeSimulation(preset_name="balanced", seed=1)
    metrics = simulation.metrics()

    assert "population" in metrics
    assert "average_energy" in metrics
    assert "average_speed" in metrics
    assert "average_generation" in metrics
