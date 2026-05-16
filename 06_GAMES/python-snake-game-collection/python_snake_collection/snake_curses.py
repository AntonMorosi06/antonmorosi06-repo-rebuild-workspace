from __future__ import annotations

import time

from .core import Direction, SnakeGame


def run_curses() -> None:
    try:
        import curses
    except Exception as exc:
        raise RuntimeError("curses is not available on this Python installation. Use --mode text or --mode tkinter.") from exc

    def wrapped(stdscr):
        curses.curs_set(0)
        stdscr.nodelay(True)
        stdscr.timeout(90)

        game = SnakeGame(width=32, height=20, seed=None)

        key_map = {
            curses.KEY_UP: Direction.UP,
            curses.KEY_DOWN: Direction.DOWN,
            curses.KEY_LEFT: Direction.LEFT,
            curses.KEY_RIGHT: Direction.RIGHT,
            ord("w"): Direction.UP,
            ord("s"): Direction.DOWN,
            ord("a"): Direction.LEFT,
            ord("d"): Direction.RIGHT,
        }

        while True:
            key = stdscr.getch()

            if key in (ord("q"), ord("Q")):
                break

            if key in (ord("r"), ord("R")):
                game.reset()

            direction = key_map.get(key)
            if direction:
                game.turn(direction)

            if not game.game_over:
                game.step()

            stdscr.erase()
            stdscr.addstr(0, 0, "Snake curses mode | arrows/WASD move | R reset | Q quit")
            stdscr.addstr(1, 0, f"Score: {game.score} | Steps: {game.steps} | Length: {len(game.snake)}")

            rows = game.board_rows()
            for y, row in enumerate(rows, start=3):
                stdscr.addstr(y, 0, row)

            if game.game_over:
                message = "YOU WIN" if game.win else "GAME OVER"
                stdscr.addstr(game.height + 5, 0, f"{message} - press R to reset or Q to quit")

            stdscr.refresh()
            time.sleep(0.035)

    curses.wrapper(wrapped)
