from black_hole_pygame.simulation import BlackHoleSimulation
from black_hole_pygame.vector import Vec2


def test_simulation_initializes_particles():
    simulation = BlackHoleSimulation(width=640, height=480, seed=1)

    assert simulation.particles
    assert simulation.black_hole.position == Vec2(320, 240)
    assert simulation.stats().particles > 0


def test_spawn_modes_are_accepted():
    simulation = BlackHoleSimulation(width=640, height=480, seed=1)

    for mode in ["edge", "disk", "spiral", "rain", "cluster"]:
        simulation.cycle_spawn_mode(mode)
        particle = simulation.spawn_particle()
        assert particle in simulation.particles


def test_update_advances_frame():
    simulation = BlackHoleSimulation(width=640, height=480, seed=1)
    frame = simulation.frame

    simulation.update(1.0 / 60.0)

    assert simulation.frame == frame + 1


def test_absorbed_particle_generates_shockwave():
    simulation = BlackHoleSimulation(width=640, height=480, seed=1)
    simulation.particles.clear()

    center = simulation.black_hole.position
    particle = simulation.spawn_particle("disk")
    particle.position = center.copy()
    particle.velocity = Vec2(0.0, 0.0)

    simulation.update(1.0 / 60.0)

    assert simulation.absorbed_total >= 1
    assert simulation.shockwaves


def test_burst_adds_particles():
    simulation = BlackHoleSimulation(width=640, height=480, seed=1)
    before = len(simulation.particles)

    simulation.burst(count=10)

    assert len(simulation.particles) == before + 10


def test_stats_contains_expected_values():
    simulation = BlackHoleSimulation(width=640, height=480, seed=1)
    stats = simulation.stats()

    assert stats.particles == len(simulation.particles)
    assert stats.spawn_mode in ["edge", "disk", "spiral", "rain", "cluster"]
    assert stats.average_energy >= 0.0
