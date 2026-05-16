from __future__ import annotations

from .core import Direction, SnakeGame


def run_text_demo(seed: int = 42, steps: int = 18) -> None:
    game = SnakeGame(width=16, height=10, seed=seed)

    scripted_turns = {
        3: Direction.DOWN,
        6: Direction.LEFT,
        9: Direction.UP,
        12: Direction.RIGHT,
    }

    print("Python Snake Game Collection - text demo")
    print("This mode is dependency-free and non-interactive.")
    print("")

    for step in range(steps):
        if step in scripted_turns:
            game.turn(scripted_turns[step])

        game.step()

        print(f"Step {step + 1} | score={game.score} | game_over={game.game_over}")
        print(game.board_text())
        print("")

        if game.game_over:
            break
