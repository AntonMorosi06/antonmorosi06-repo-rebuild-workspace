from __future__ import annotations

from .core import Direction, SnakeGame, direction_from_key


CELL = 24
TICK_MS = 95


class TkinterSnakeApp:
    def __init__(self) -> None:
        import tkinter as tk

        self.tk = tk
        self.root = tk.Tk()
        self.root.title("Python Snake Game Collection - Tkinter")
        self.game = SnakeGame(width=28, height=20, seed=None)

        self.canvas = tk.Canvas(
            self.root,
            width=self.game.width * CELL,
            height=self.game.height * CELL,
            bg="#080d16",
            highlightthickness=0,
        )
        self.canvas.pack(padx=14, pady=(14, 8))

        self.label = tk.Label(
            self.root,
            text="Arrows/WASD move | R reset | Esc quit",
            font=("Arial", 13),
        )
        self.label.pack(pady=(0, 14))

        self.root.bind("<Key>", self.on_key)
        self.running = True

    def on_key(self, event) -> None:
        if event.keysym == "Escape":
            self.running = False
            self.root.destroy()
            return

        if event.keysym.lower() == "r":
            self.game.reset()
            return

        direction = direction_from_key(event.keysym)
        if direction:
            self.game.turn(direction)

    def draw(self) -> None:
        self.canvas.delete("all")

        for y in range(self.game.height):
            for x in range(self.game.width):
                px = x * CELL
                py = y * CELL
                self.canvas.create_rectangle(
                    px,
                    py,
                    px + CELL,
                    py + CELL,
                    outline="#111827",
                    fill="#080d16",
                )

        food = self.game.food
        self.canvas.create_oval(
            food.x * CELL + 5,
            food.y * CELL + 5,
            food.x * CELL + CELL - 5,
            food.y * CELL + CELL - 5,
            fill="#ff4d5f",
            outline="#ffd1d6",
        )

        for index, point in enumerate(self.game.snake):
            color = "#7cffb2" if index == 0 else "#67d7ff"
            self.canvas.create_rectangle(
                point.x * CELL + 3,
                point.y * CELL + 3,
                point.x * CELL + CELL - 3,
                point.y * CELL + CELL - 3,
                fill=color,
                outline="#edf3ff",
            )

        status = f"Score: {self.game.score} | Steps: {self.game.steps} | Length: {len(self.game.snake)}"
        if self.game.game_over:
            status += " | GAME OVER - press R"

        self.label.configure(text=status)

    def tick(self) -> None:
        if not self.running:
            return

        if not self.game.game_over:
            self.game.step()

        self.draw()
        self.root.after(TICK_MS, self.tick)

    def run(self) -> None:
        self.tick()
        self.root.mainloop()


def run_tkinter() -> None:
    TkinterSnakeApp().run()
