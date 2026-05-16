from __future__ import annotations

from pathlib import Path
import time

from .palette import AGENT, AGENT_FAST, AGENT_MUTANT, BACKGROUND, BEST, DANGER, FOOD, GRID, MUTED, PANEL, TEXT, TRAIL
from .simulation import LifeSimulation


WIDTH = 1280
HEIGHT = 820
PANEL_WIDTH = 370
WORLD_WIDTH = WIDTH - PANEL_WIDTH
WORLD_HEIGHT = HEIGHT


class GeneticEvolutionLifeApp:
    def __init__(self) -> None:
        try:
            import pygame
        except Exception as exc:
            raise RuntimeError("pygame is not installed. Install it with: pip install -r requirements.txt") from exc

        self.pygame = pygame
        pygame.init()
        pygame.display.set_caption("Genetic Evolution Life Simulation - Reconstructed Skeleton")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 24, bold=True)
        self.small = pygame.font.SysFont("Arial", 16)
        self.tiny = pygame.font.SysFont("Arial", 13)

        self.simulation = LifeSimulation(preset_name="balanced", seed=42)
        self.running = True
        self.show_trails = True
        self.show_debug = True

    def set_preset_by_index(self, index: int) -> None:
        names = ["balanced", "scarce", "abundant", "high_mutation", "drift"]
        if 0 <= index < len(names):
            self.simulation.set_preset(names[index])

    def save_screenshot(self) -> None:
        screenshots = Path(__file__).resolve().parents[1] / "screenshots"
        screenshots.mkdir(parents=True, exist_ok=True)
        stamp = time.strftime("%Y%m%d_%H%M%S")
        path = screenshots / f"genetic_evolution_life_{self.simulation.preset_name}_{stamp}.png"
        self.pygame.image.save(self.screen, str(path))
        print("[OK] Screenshot saved:", path)

    def handle_key(self, key: int) -> None:
        pygame = self.pygame

        if key in (pygame.K_ESCAPE, pygame.K_q):
            self.running = False
        elif key == pygame.K_SPACE:
            self.simulation.paused = not self.simulation.paused
        elif key == pygame.K_n:
            paused = self.simulation.paused
            self.simulation.paused = False
            self.simulation.step()
            self.simulation.paused = paused
        elif key == pygame.K_r:
            self.simulation.reset()
        elif key == pygame.K_f:
            self.simulation.add_food_burst()
        elif key == pygame.K_a:
            self.simulation.add_agent_burst()
        elif key == pygame.K_1:
            self.set_preset_by_index(0)
        elif key == pygame.K_2:
            self.set_preset_by_index(1)
        elif key == pygame.K_3:
            self.set_preset_by_index(2)
        elif key == pygame.K_4:
            self.set_preset_by_index(3)
        elif key == pygame.K_5:
            self.set_preset_by_index(4)
        elif key == pygame.K_t:
            self.show_trails = not self.show_trails
        elif key == pygame.K_d:
            self.show_debug = not self.show_debug
        elif key == pygame.K_s:
            self.save_screenshot()

    def world_to_screen(self, x: float, y: float) -> tuple[int, int]:
        sx = int(x / self.simulation.config.width * WORLD_WIDTH)
        sy = int(y / self.simulation.config.height * WORLD_HEIGHT)
        return sx, sy

    def draw_background(self) -> None:
        pygame = self.pygame
        self.screen.fill(BACKGROUND)

        for x in range(0, WORLD_WIDTH, 48):
            pygame.draw.line(self.screen, GRID, (x, 0), (x, HEIGHT), 1)
        for y in range(0, HEIGHT, 48):
            pygame.draw.line(self.screen, GRID, (0, y), (WORLD_WIDTH, y), 1)

        pygame.draw.rect(self.screen, PANEL, (WORLD_WIDTH, 0, PANEL_WIDTH, HEIGHT))

    def draw_food(self) -> None:
        pygame = self.pygame

        for item in self.simulation.food:
            sx, sy = self.world_to_screen(item.position.x, item.position.y)
            pygame.draw.circle(self.screen, FOOD, (sx, sy), max(2, int(item.radius)))

    def agent_color(self, agent) -> tuple[int, int, int]:
        if agent.genome.mutation_intensity > 0.22:
            return AGENT_MUTANT
        if agent.genome.speed > 3.7:
            return AGENT_FAST
        return AGENT

    def draw_trails(self) -> None:
        if not self.show_trails:
            return

        pygame = self.pygame
        surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

        for agent in self.simulation.agents:
            if len(agent.trail) < 2:
                continue

            for index in range(1, len(agent.trail)):
                a = self.world_to_screen(agent.trail[index - 1].x, agent.trail[index - 1].y)
                b = self.world_to_screen(agent.trail[index].x, agent.trail[index].y)
                alpha = int(18 + 82 * index / len(agent.trail))
                pygame.draw.line(surface, (*TRAIL, alpha), a, b, 1)

        self.screen.blit(surface, (0, 0))

    def draw_agents(self) -> None:
        pygame = self.pygame
        best = None
        if self.simulation.agents:
            best = max(self.simulation.agents, key=lambda agent: agent.fitness_proxy())

        for agent in self.simulation.agents:
            sx, sy = self.world_to_screen(agent.position.x, agent.position.y)
            color = self.agent_color(agent)
            radius = max(3, int(agent.radius))

            pygame.draw.circle(self.screen, color, (sx, sy), radius)
            pygame.draw.circle(self.screen, (237, 243, 255), (sx, sy), radius + 1, width=1)

            if self.show_debug:
                perception_radius = int(agent.genome.perception / self.simulation.config.width * WORLD_WIDTH)
                if agent is best:
                    pygame.draw.circle(self.screen, BEST, (sx, sy), radius + 8, width=2)
                    pygame.draw.circle(self.screen, (*BEST,), (sx, sy), radius + 2, width=1)
                elif agent.age % 37 == 0:
                    pygame.draw.circle(self.screen, (90, 168, 255), (sx, sy), perception_radius, width=1)

    def draw_history_chart(self, x: int, y: int, width: int, height: int, key: str, color: tuple[int, int, int]) -> None:
        pygame = self.pygame
        history = self.simulation.history[-110:]
        if len(history) < 2:
            return

        values = [float(entry.get(key, 0.0)) for entry in history]
        min_v = min(values)
        max_v = max(values)

        pygame.draw.rect(self.screen, (8, 13, 22), (x, y, width, height), border_radius=8)
        pygame.draw.rect(self.screen, GRID, (x, y, width, height), width=1, border_radius=8)

        points = []
        for index, value in enumerate(values):
            nx = index / max(1, len(values) - 1)
            ny = 0.5 if max_v <= min_v else (value - min_v) / (max_v - min_v)
            points.append((int(x + nx * width), int(y + height - ny * height)))

        if len(points) >= 2:
            pygame.draw.lines(self.screen, color, False, points, 2)

    def text(self, value: str, x: int, y: int, color=TEXT, font=None) -> None:
        chosen = font or self.small
        rendered = chosen.render(value, True, color)
        self.screen.blit(rendered, (x, y))

    def draw_panel(self) -> None:
        metrics = self.simulation.metrics()
        x = WORLD_WIDTH + 22
        y = 24

        self.text("Evolution Life", x, y, TEXT, self.font)
        y += 34
        self.text("Artificial life simulation", x, y, MUTED)
        y += 36

        lines = [
            f"Preset: {metrics['preset']}",
            f"Tick: {metrics['tick']}",
            f"Population: {metrics['population']}",
            f"Food: {metrics['food']}",
            f"Avg energy: {metrics['average_energy']:.2f}",
            f"Avg speed: {metrics['average_speed']:.2f}",
            f"Avg perception: {metrics['average_perception']:.2f}",
            f"Avg metabolism: {metrics['average_metabolism']:.4f}",
            f"Avg mutation: {metrics['average_mutation']:.3f}",
            f"Avg generation: {metrics['average_generation']:.2f}",
            f"Oldest age: {metrics['oldest_age']}",
            f"State: {'paused' if self.simulation.paused else 'running'}",
        ]

        for line in lines:
            self.text(line, x, y, TEXT)
            y += 23

        y += 10
        self.text("Population history", x, y, FOOD)
        y += 24
        self.draw_history_chart(x, y, PANEL_WIDTH - 44, 74, "population", FOOD)
        y += 92

        self.text("Energy history", x, y, BEST)
        y += 24
        self.draw_history_chart(x, y, PANEL_WIDTH - 44, 74, "average_energy", BEST)
        y += 92

        self.text("Controls", x, y, BEST)
        y += 24

        controls = [
            "Space pause/resume",
            "N step if paused",
            "R reset",
            "F add food",
            "A add agents",
            "1 balanced",
            "2 scarce food",
            "3 abundant food",
            "4 high mutation",
            "5 drift",
            "T trails",
            "D debug",
            "S screenshot",
            "Q/Esc quit",
        ]

        for line in controls:
            self.text(line, x, y, MUTED, self.tiny)
            y += 17

    def draw_debug_footer(self) -> None:
        if not self.show_debug:
            return

        message = (
            "Core loop: food seeking -> movement -> energy cost -> eating -> reproduction -> mutation -> death | "
            "Traits: speed, perception, metabolism, size, fertility, mutation intensity"
        )
        self.text(message, 18, HEIGHT - 28, TEXT, self.tiny)

    def draw(self) -> None:
        self.draw_background()
        self.draw_food()
        self.draw_trails()
        self.draw_agents()
        self.draw_panel()
        self.draw_debug_footer()
        self.pygame.display.flip()

    def run(self) -> None:
        pygame = self.pygame

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    self.handle_key(event.key)

            self.simulation.step()
            self.draw()
            self.clock.tick(60)

        pygame.quit()


def run_app() -> None:
    GeneticEvolutionLifeApp().run()
